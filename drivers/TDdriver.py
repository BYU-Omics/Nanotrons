from os import environ
import logging
import asyncio
from threading import Event, Thread, Lock
from time import sleep
from typing import Any, Optional, Mapping, Dict, Tuple, Union
from serial.serialutil import SerialException  # type: ignore

from opentrons.drivers import serial_communication, utils
from opentrons.drivers.serial_communication import SerialNoResponse

from serial.tools import list_ports
import os

from constants import RUNNING_APP_FOR_REAL, TEMPDECK_CONNECTED

'''
- Driver is responsible for providing an interface for the temp-deck
- Driver is the only system component that knows about the temp-deck's GCODES
  or how the temp-deck communications

- Driver is NOT responsible interpreting the temperatures or states in any way
  or knowing anything about what the device is being used for
'''

log = logging.getLogger(__name__)

ERROR_KEYWORD = 'error'
ALARM_KEYWORD = 'alarm'

DEFAULT_TEMP_DECK_TIMEOUT = 1

DEFAULT_STABILIZE_DELAY = 0.1
DEFAULT_COMMAND_RETRIES = 3

GCODES = {
    'GET_TEMP': 'M105',
    'SET_TEMP': 'M104',
    'DEVICE_INFO': 'M115',
    'DISENGAGE': 'M18',
    'PROGRAMMING_MODE': 'dfu'
}

TEMP_DECK_BAUDRATE = 115200

WINDOWS_TD_SER = '7&322D9725&0&1'
LINUX_TD_PORT = '/dev/ttyACM0'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
MACBOOK_TD_PORT = '/dev/cu.usbmodem142301'


TEMP_DECK_COMMAND_TERMINATOR = '\r\n\r\n'
TEMP_DECK_ACK = 'ok\r\nok\r\n'

TEMP_DECK_MODELS = {
    'temperatureModuleV1': 'temp_deck_v1.1',
    'temperatureModuleV2': 'temp_deck_v20'
}

temp_locks: Dict[str, Tuple[Lock, 'TempDeck']] = {}


class TempDeckError(Exception):
    pass

class TempDeck:
    def __init__(self):
        self.run_flag = Event()
        self.run_flag.set()

        self._connection = None
        self._temperature = {'current': 25, 'target': 10}
        self._update_thread = None
        self._port = None
        self.find_port()
        if RUNNING_APP_FOR_REAL and TEMPDECK_CONNECTED:
            self.connect(self._port)
        else:
            print("Not connected to the TD port")

    def connect(self, port=None) -> Optional[str]:
        try:
            self.disconnect(port)
            self._connect_to_port(port)
            self._wait_for_ack()  # verify the device is there
            self._port = port

        except (SerialException, SerialNoResponse) as e:
            return str(e)
        return ''

    def disconnect(self, port=None):
        if self._port and self.is_connected():
            self._connection.close()  # type: ignore
            # del temp_locks[self._port]
        elif self.is_connected():
            self._connection.close()  # type: ignore

        self._connection = None

    def is_connected(self) -> bool:
        if not self._connection:
            return False
        return self._connection.is_open

    @property
    def port(self) -> Optional[str]:
        if not self._connection:
            return None
        return self._connection.port

    def deactivate(self) -> str:
        self.run_flag.wait()
        try:
            self._send_command(GCODES['DISENGAGE'])
        except (TempDeckError, SerialException, SerialNoResponse) as e:
            return str(e)
        return ''

    async def set_temperature(self, celsius) -> str:
        self.run_flag.wait()
        celsius = round(float(celsius),
                        utils.TEMPDECK_GCODE_ROUNDING_PRECISION)
        try:
            self._send_command(
                '{0} S{1}'.format(GCODES['SET_TEMP'], celsius))
        except (TempDeckError, SerialException, SerialNoResponse) as e:
            return str(e)
        self._temperature.update({'target': celsius})
        while self.status != 'holding at target':
            await asyncio.sleep(0.1)
        return ''

    def start_set_temperature(self, celsius) -> str:
        self.run_flag.wait()
        celsius = round(float(celsius),
                        utils.TEMPDECK_GCODE_ROUNDING_PRECISION)
        self._send_command(
                '{0} S{1}'.format(GCODES['SET_TEMP'], celsius))
        self._temperature.update({'target': celsius})
        return ''

    # NOTE: only present to support apiV1 non-blocking by default behavior
    def legacy_set_temperature(self, celsius) -> str:
        self.run_flag.wait()
        celsius = round(float(celsius),
                        utils.TEMPDECK_GCODE_ROUNDING_PRECISION)
        try:
            self._send_command(
                '{0} S{1}'.format(GCODES['SET_TEMP'], celsius))
        except (TempDeckError, SerialException, SerialNoResponse) as e:
            return str(e)
        self._temperature.update({'target': celsius})
        return ''

    def update_temperature(self, default=None) -> str:
        if self._update_thread and self._update_thread.is_alive():
            updated_temperature = default or self._temperature.copy()
            self._temperature.update(updated_temperature)
        else:
            # comment
            try:
                self._update_thread = Thread(
                    target=self._recursive_update_temperature,
                    args=[DEFAULT_COMMAND_RETRIES],
                    name='Tempdeck recursive update temperature')
                self._update_thread.start()
            except (TempDeckError, SerialException, SerialNoResponse) as e:
                return str(e)
        return ''

    @property
    def target(self) -> Optional[int]:
        return self._temperature.get('target')

    @property
    def temperature(self) -> int:
        return self._temperature['current']  # type: ignore

    def _get_status(self) -> str:
        # Separate function for testability
        current = float(self._temperature['current'])
        target = self._temperature.get('target')
        if target != 'none':
            target = float(target)
            delta = 0.7
            if target != 'none':
                diff = target - current  # type: ignore
                if abs(diff) < delta:   # To avoid status fluctuation near target
                    return 'holding at target'
                elif diff < 0:
                    return 'cooling'
                else:
                    return 'heating'
            else:
                return 'idle'
        else:
            print(f"Target is: {self._temperature.get('target')}")

    @property
    def status(self) -> str:
        return self._get_status()

    def get_device_info(self) -> Mapping[str, str]:
        '''
        Queries Temp-Deck for its build version, model, and serial number

        returns: dict
            Where keys are the strings 'version', 'model', and 'serial',
            and each value is a string identifier

            {
                'serial': '1aa11bb22',
                'model': '1aa11bb22',
                'version': '1aa11bb22'
            }

        Example input from Temp-Deck's serial response:
            "serial:aa11bb22 model:aa11bb22 version:aa11bb22"
        '''
        return self._get_info(DEFAULT_COMMAND_RETRIES)

    def pause(self):
        self.run_flag.clear()

    def resume(self):
        self.run_flag.set()

    def enter_programming_mode(self) -> str:
        try:
            self._send_command(GCODES['PROGRAMMING_MODE'])
        except (TempDeckError, SerialException, SerialNoResponse) as e:
            return str(e)
        if self._port:
            del temp_locks[self._port]
        return ''

    def _connect_to_port(self, port=None):
        try:
            temp_deck = environ.get('OT_TEMP_DECK_ID', None)
            self._connection = serial_communication.connect(
                device_name=temp_deck,
                port=port,
                baudrate=TEMP_DECK_BAUDRATE
            )
            
        except SerialException:
            # if another process is using the port, pyserial raises an
            # exception that describes a "readiness to read" which is confusing
            error_msg = 'Unable to access Serial port to Temp-Deck. This is '
            error_msg += 'because another process is currently using it, or '
            error_msg += 'the Serial port is disabled on this device (OS)'
            raise SerialException(error_msg)

    def _wait_for_ack(self):
        '''
        This methods writes a sequence of newline characters, which will
        guarantee temp-deck responds with 'ok\r\nok\r\n' within 1 seconds
        '''
        self._send_command('\r\n', timeout=DEFAULT_TEMP_DECK_TIMEOUT)

    # Potential place for command optimization (buffering, flushing, etc)
    def _send_command(
            self, command, timeout=DEFAULT_TEMP_DECK_TIMEOUT, tag=None):
        """

        """
        command_line = command + ' ' + TEMP_DECK_COMMAND_TERMINATOR
        ret_code = self._recursive_write_and_return(
            command_line, timeout, DEFAULT_COMMAND_RETRIES)

        # Smoothieware returns error state if a switch was hit while moving
        if (ERROR_KEYWORD in ret_code.lower()) or \
                (ALARM_KEYWORD in ret_code.lower()):
            log.error(f'Received error message from Temp-Deck: {ret_code}')
            raise TempDeckError(ret_code)

        return ret_code.strip()

    def _recursive_write_and_return(self, cmd, timeout, retries, tag=None):
        if not tag:
            tag = f'tempdeck {id(self)}'
        try:
            return serial_communication.write_and_return(
                cmd,
                TEMP_DECK_ACK,
                self._connection,
                timeout,
                tag=tag)
        except SerialNoResponse as e:
            retries -= 1
            if retries <= 0:
                raise e
            sleep(DEFAULT_STABILIZE_DELAY)
            if self._connection:
                self._connection.close()
                self._connection.open()
            return self._recursive_write_and_return(
                cmd, timeout, retries, tag=tag)

    def _recursive_update_temperature(self, retries):
        try:
            res = self._send_command(
                GCODES['GET_TEMP'],
                tag=f'tempdeck {id(self)} rut')
            data = utils.parse_key_values(res)
            res = utils.parse_temperature_response(
                res, utils.TEMPDECK_GCODE_ROUNDING_PRECISION)
            # print(data['C'])
            self._temperature.update({'current': data['C'], 'target':  data['T']})
            print(f"Temp updated to: {self._temperature}")
            return None
        except utils.ParseError as e:
            retries -= 1
            if retries <= 0:
                raise TempDeckError(e)
            sleep(DEFAULT_STABILIZE_DELAY)
            return self._recursive_update_temperature(retries)

    def _get_info(self, retries) -> Mapping[str, str]:
        last_e: Any = None
        for _ in range(retries):
            try:
                device_info = self._send_command(GCODES['DEVICE_INFO'])
                return utils.parse_device_information(device_info)
            except utils.ParseError as e:
                log.exception("tempdeck device information parse failure")
                last_e = e
                sleep(DEFAULT_STABILIZE_DELAY)
        if last_e:
            raise last_e
        else:
            raise TempDeckError('Unknown error in temperature module')

    def find_port(self):
        ports = list_ports.comports()
        operating_system = os.name
        for p in ports:
            # print(p.serial_number)
            if operating_system == WINDOWS_OS and p.serial_number == WINDOWS_TD_SER:
                self._port = p.device
                print(f"Tempdeck connected to: {p}")
            elif operating_system == LINUX_OS:
                if p == LINUX_TD_PORT or p.device == MACBOOK_TD_PORT:
                    self._port = p.device
                    # print(self._port)
                    print(f"Tempdeck connected to: {p}")
                else: 
                    # print(f"Port not found: {p.device}")
                    pass
            # else:
            #     print(f"No operating system recognized: {operating_system}")
                

def test():
    TD = TempDeck()
    # await TD.set_temperature(4)
    # TD.deactivate()
    # TD.pause()
    # TD.resume()
    # TD.update_temperature()
    # TD.start_set_temperature(10)
    # # TD.legacy_set_temperature(4)
    # print("updating temp")
    # TD.update_temperature()
    # sleep(0.01)
    # print(TD.temperature)
    # print(TD.status)
    # print(TD.get_device_info()) # RETURNS: {'model': 'temp_deck_v3.0', 'version': 'v2.0.1', 'serial': 'TDV03P20181008A06'}


if __name__ == "__main__":
    test()
