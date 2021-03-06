import asyncio
import logging
import os
import threading
import serial  # type: ignore
from queue import Queue
try:
    import select
except ModuleNotFoundError:
    select = None  # type: ignore
from time import sleep
from collections import deque
from typing import Callable, Optional, Mapping, Tuple, Deque, TYPE_CHECKING
from serial.serialutil import SerialException  # type: ignore
from opentrons.drivers import utils, serial_communication
from opentrons.drivers.serial_communication import SerialNoResponse
from serial.tools import list_ports
from constants import RUNNING_APP_FOR_REAL, THERMOCYCLER_CONNECTED
import os

if TYPE_CHECKING:
    # avoid an issue where Queue doesn't support generics at runtime
    CommandQueue = Queue[Tuple[str, Callable[[str], None]]]
else:
    CommandQueue = Queue

import sys


log = logging.getLogger(__name__)

GCODES = {
    'OPEN_LID': 'M126',
    'CLOSE_LID': 'M127',
    'GET_LID_STATUS': 'M119',
    'SET_LID_TEMP': 'M140',
    'GET_LID_TEMP': 'M141',
    'EDIT_PID_PARAMS': 'M301',
    'SET_PLATE_TEMP': 'M104',
    'GET_PLATE_TEMP': 'M105',
    'SET_RAMP_RATE': 'M566',
    'DEACTIVATE_ALL': 'M18',
    'DEACTIVATE_LID': 'M108',
    'DEACTIVATE_BLOCK': 'M14',
    'DEVICE_INFO': 'M115'
}
LID_TARGET_DEFAULT = 105.0    # Degree celsius (floats)
LID_TARGET_MIN = 37.0
LID_TARGET_MAX = 110.0
BLOCK_TARGET_MIN = 0.0
BLOCK_TARGET_MAX = 99.0
TEMP_UPDATE_RETRIES = 50
TEMP_BUFFER_MAX_LEN = 10


def _build_temp_code(temp: float,
                     hold_time: Optional[float],
                     volume: Optional[float]):
    if float(temp) < BLOCK_TARGET_MIN:
        temp = BLOCK_TARGET_MIN
    if float(temp) > BLOCK_TARGET_MAX:
        temp = BLOCK_TARGET_MAX
    cmd = f"{GCODES['SET_PLATE_TEMP']} S{temp}"
    if hold_time:
        cmd += f' H{hold_time}'
        # print(f"Hold time _build_temp_code: {hold_time} minutes")
    if volume:
        cmd += f' V{volume}'
    return cmd, temp


TC_BAUDRATE = 115200
TC_BOOTLOADER_BAUDRATE = 1200
# TODO (Laura 20190327) increased the thermocycler command timeout
# temporarily until we can change the firmware to asynchronously handle
# the lid being open and closed
SERIAL_ACK = '\r\n'
TC_COMMAND_TERMINATOR = SERIAL_ACK
TC_ACK = 'ok' + SERIAL_ACK + 'ok' + SERIAL_ACK
ERROR_KEYWORD = 'error'
DEFAULT_TC_TIMEOUT = 40
DEFAULT_COMMAND_RETRIES = 3
DEFAULT_STABILIZE_DELAY = 0.1
DEFAULT_POLLER_WAIT_SECONDS = 0.1
POLLING_FREQUENCY_MS = 1000
HOLD_TIME_FUZZY_SECONDS = POLLING_FREQUENCY_MS / 1000 * 5
TEMP_THRESHOLD = 0.3

WINDOWS_TC_PORT = 'COM5'
WINDOWS_TC_SER = 'B71546CF50533336372E3120FF12202C'
LINUX_TC_PORT = '/dev/ttyACM0'
LINUX_OS = 'posix'
WINDOWS_OS = 'nt'
MACBOOK_TC_PORT = '/dev/cu.usbmodem142101'

class ThermocyclerError(Exception):
    pass

class Thermocycler:
    def __init__(self, interrupt_callback):
        self._port = None
        self._connection = None
        if RUNNING_APP_FOR_REAL and THERMOCYCLER_CONNECTED:
            print("Attempting to connect to TC")
            self._connection = self._connect_to_port()
        else:
            print("Not connected to the TC port")
        self._update_thread = None
        self._current_temp = None
        self._target_temp = None
        self._ramp_rate = None
        self._hold_time = None
        self._lid_status = None
        self._interrupt_cb = interrupt_callback
        self._lid_target = 37
        self._lid_temp = 37
        self.simulating = True
        # to store previous _current_temp values:
        self._block_temp_buffer: Deque = deque(maxlen=TEMP_BUFFER_MAX_LEN)

    async def connect(self, port: str) -> 'Thermocycler':
        self.disconnect()
        self._connect_to_port(port)
        # Check initial device lid state
        # _lid_status_res = await self._write_and_wait(GCODES['GET_LID_STATUS'])
        # if _lid_status_res:
        #     self._lid_status = utils.parse_string_value_from_substring(
        #         _lid_status_res.split()[-1])
        return self

    def disconnect(self) -> 'Thermocycler':
        if self.is_connected():
            self._connection.close()  # type: ignore
        self._connection = None
        self.simulating = True

    def is_connected(self) -> bool:
        if not self._connection:
            return False
        return self._connection.is_open

    def _connect_to_port(self):
        self.find_port()
        try:
            return serial_communication.connect(port=self._port,
                                                baudrate=TC_BAUDRATE)
        except SerialException:
            raise SerialException(
                "Thermocycler device not found on {}".format(self._port))

    def _wait_for_ack(self):
        """
        This method writes a sequence of newline characters, which will
        guarantee the device responds with 'ok\r\nok\r\n' within 1 second
        """
        self._send_command(SERIAL_ACK, timeout=DEFAULT_TC_TIMEOUT)

    def _send_command(self, command, timeout=DEFAULT_TC_TIMEOUT):
        command_line = command + ' ' + TC_COMMAND_TERMINATOR
        ret_code = self._recursive_write_and_return(
            command_line, timeout, DEFAULT_COMMAND_RETRIES)
        if ERROR_KEYWORD in ret_code.lower():
            log.error('Received error message from Thermocycler: {}'.format(
                ret_code))
            raise ThermocyclerError(ret_code)
        return ret_code.strip()

    def _recursive_write_and_return(self, cmd, timeout, retries):
        try:
            return serial_communication.write_and_return(
                cmd, TC_ACK, self._connection, timeout,
                tag=f'thermocycler {id(self)}')
        except SerialNoResponse as e:
            retries -= 1
            if retries <= 0:
                raise e
            sleep(DEFAULT_STABILIZE_DELAY)
            if self._connection:
                self._connection.close()
                self._connection.open()
            return self._recursive_write_and_return(
                cmd, timeout, retries)

    def set_temps(self):
        res = self._send_command(GCODES['GET_PLATE_TEMP'])
        self._temp_status_update_callback(res)
        res = self._send_command(GCODES['GET_LID_STATUS'])
        self._lid_status_update_callback(res)
        res = self._send_command(GCODES['GET_LID_TEMP'])
        self._lid_temp_status_callback(res)
    
    def get_lid_temp(self):
        self.set_temps()
        # print(self._lid_temp)
        return self._lid_temp

    def get_block_temp(self):
        self.set_temps()
        # print(self._current_temp)
        return self._current_temp

    async def deactivate_all(self):
        await self._write_and_wait(GCODES['DEACTIVATE_ALL'])

    async def deactivate_lid(self) -> None:
        await self._write_and_wait(GCODES['DEACTIVATE_LID'])

    async def deactivate_block(self):
        await self._write_and_wait(GCODES['DEACTIVATE_BLOCK'])

    async def open(self):
        await self._write_and_wait(GCODES['OPEN_LID'])
        self.lid_status = 'open'
        return self.lid_status

    async def close(self):
        await self._write_and_wait(GCODES['CLOSE_LID'])
        self.lid_status = 'closed'
        return self.lid_status

    def hold_time_probably_set(self, new_hold_time: Optional[float]) -> bool:
        """
        Since we can only get hold time *remaining* from TC, by the time we
        read hold_time after a set_temperature, the hold_time in TC could have
        started counting down. So instead of checking for equality, we will
        have to check if the hold_time returned from TC is within a few seconds
        of the new hold time. The number of seconds is determined by status
        polling frequency.
        """
        if new_hold_time is None:
            return True
        if self._hold_time is None:
            return False
        lower_bound = max(0.0, new_hold_time - HOLD_TIME_FUZZY_SECONDS)
        return lower_bound <= self._hold_time <= new_hold_time

    async def set_temperature(self,
                              temp: float,
                              hold_time: float = None,
                              ramp_rate: float = None,
                              volume: float = None) -> None:
        # print(f"Setting temp to: {temp}")
        if ramp_rate:
            ramp_cmd = f"{GCODES['SET_RAMP_RATE']} S{ramp_rate}"
            await self._write_and_wait(ramp_cmd)
        temp_cmd, temp = _build_temp_code(temp=temp,
                                          hold_time=hold_time,
                                          volume=volume)
        # print(f"temo comd: {temp_cmd}")
        await self._write_and_wait(temp_cmd)
        retries = 0
        # while self._target_temp != temp or \
        #         not self.hold_time_probably_set(hold_time):
        #     # Wait for the poller to update
        #     await asyncio.sleep(DEFAULT_POLLER_WAIT_SECONDS)
        #     retries += 1
        #     print(f"retries = {retries}")
        #     if retries > TEMP_UPDATE_RETRIES:
        #         raise ThermocyclerError(f'Thermocycler driver set the block '
        #                                 f'temp to T={temp} & H={hold_time} '
        #                                 f'but status reads '
        #                                 f'T={self._target_temp} & '
        #                                 f'H={self._hold_time}')

    async def set_lid_temperature(self, temp: float) -> None:
        # print(f"Setting lid temp to: {temp}")
        if temp is None:
            _lid_target = LID_TARGET_DEFAULT
        else:
            if temp < LID_TARGET_MIN:
                _lid_target = LID_TARGET_MIN
            elif temp > LID_TARGET_MAX:
                _lid_target = LID_TARGET_MAX
            else:
                _lid_target = temp

        lid_temp_cmd = '{} S{}'.format(GCODES['SET_LID_TEMP'], _lid_target)
        await self._write_and_wait(lid_temp_cmd)
        retries = 0
        # while self._lid_target != _lid_target:
        #     print(f"retries = {retries}")
        #     # Wait for the poller to update
        #     await asyncio.sleep(DEFAULT_POLLER_WAIT_SECONDS)
        #     retries += 1
        #     if retries > TEMP_UPDATE_RETRIES:
        #         raise ThermocyclerError(f'Thermocycler driver set lid temp to'
        #                                 f' {_lid_target} but self._lid_target'
        #                                 f' reads {self._lid_target}')

    def _lid_status_update_callback(self, lid_response):
        if lid_response:
            self._lid_status = utils.parse_string_value_from_substring(
                lid_response.split()[-1])

    def _temp_status_update_callback(self, temperature_response):
        # Payload is shaped like `T:95.0 C:77.4 H:600` where T is the
        # target temperature, C is the current temperature, and H is the
        # hold time remaining
        temp = utils.parse_plate_temperature_response(
            temperature_string=temperature_response,
            rounding_val=utils.TC_GCODE_ROUNDING_PRECISION
        )
        self._current_temp = temp.current
        self._target_temp = temp.target
        self._hold_time = temp.hold
        self._block_temp_buffer.append(self._current_temp)

    def _lid_temp_status_callback(self, lid_temp_res):
        # Payload is shaped like `T:95.0 C:77.4` where T is the
        # target temperature, C is the current temperature
        temp = utils.parse_temperature_response(
            temperature_string=lid_temp_res,
            rounding_val=utils.TC_GCODE_ROUNDING_PRECISION
        )
        self._lid_temp = temp.current
        self._lid_target = temp.target

    def _interrupt_callback(self, interrupt_response):
        # TODO sanitize response and then call the callback
        parsed_response = interrupt_response
        self._interrupt_cb(parsed_response)

    @property
    def temperature(self):
        return self._current_temp

    @property
    def target(self):
        return self._target_temp

    @property
    def hold_time(self):
        return self._hold_time

    @property
    def ramp_rate(self):
        return self._ramp_rate

    @property
    def lid_temp_status(self):
        if self.lid_temp is None:
            _status = 'error'
        if self.lid_target is None:
            _status = 'idle'
        else:
            diff = self.lid_target - self.lid_temp
            if abs(diff) < TEMP_THRESHOLD:
                _status = 'holding at target'
            elif diff < 0:
                _status = 'idle'  # TC lid can't actively cool
            else:
                _status = 'heating'
        return _status

    @property
    def status(self):
        if self.temperature is None:
            _status = 'error'
        elif self.target is None:
            _status = 'idle'
        else:
            diff = self.target - self.temperature
            if self._is_holding_at_target():
                _status = 'holding at target'
            elif diff < 0:
                _status = 'cooling'
            else:
                _status = 'heating'
        return _status

    def _is_holding_at_target(self) -> bool:
        """
        Checks block temp history to determine if block temp has stabilized at
        the target temperature. Returns true only if all values in history are
        within threshold range of target temperature.
        """
        if len(self._block_temp_buffer) < TEMP_BUFFER_MAX_LEN:
            # Not enough temp history
            return False
        else:
            return all(abs(self.target - t) < TEMP_THRESHOLD
                       for t in self._block_temp_buffer)

    @property
    def port(self) -> Optional[str]:
        if not self._poller:
            return None
        return self._poller.port

    @property
    def lid_status(self):
        return self._lid_status

    @lid_status.setter
    def lid_status(self, status):
        self._lid_status = status

    @property
    def lid_temp(self):
        return self._lid_temp

    @property
    def lid_target(self):
        return self._lid_target

    async def get_device_info(self) -> Mapping[str, str]:
        _device_info_res = await self._write_and_wait(GCODES['DEVICE_INFO'])
        if _device_info_res:
            return utils.parse_device_information(_device_info_res)
        else:
            raise ThermocyclerError("Thermocycler did not return device info")

    async def _write_and_wait(self, command):
        self._send_command(command=command)

    async def enter_programming_mode(self):
        trigger_connection = serial.Serial(
            self.port, TC_BOOTLOADER_BAUDRATE, timeout=1)
        await asyncio.sleep(0.05)
        trigger_connection.close()
        self.disconnect()

    def find_port(self):
        ports = list_ports.comports()
        operating_system = os.name
        for p in ports:
            # print(p)
            if operating_system == WINDOWS_OS and p.serial_number == WINDOWS_TC_SER:
                self._port = p.device
                print(f"Thermocycler connected to: {p}")
            elif operating_system == LINUX_OS:
                if p == LINUX_TC_PORT or p.device == MACBOOK_TC_PORT:
                    self._port = p.device
                    # print(self._port)
                    print(f"Thermocycler connected to: {p}")
                else: 
                    # print(f"Port not found: {p.device}")
                    pass
            # else:
            #     print(f"No operating system recognized: {operating_system}")
                

async def testing():
    tc_portname = '/dev/ttyACM0'
    tc_portname_windows = 'COM5' 
    TC = Thermocycler(interrupt_callback=interrupt_callback)
    # await TC.close()
    await TC.set_temperature(4, 30)
    # await TC.deactivate_all()
    # await TC.close()
    # await TC.set_temperature(60, 60)
    # await TC.set_lid_temperature(40)

async def interrupt_callback(res):
    sys.stderr.write(res)

if __name__ == "__main__":
    asyncio.run(testing())
