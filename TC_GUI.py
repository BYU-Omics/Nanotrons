#!/usr/bin/env python3
# 
# Name: ot_thermocycler_standalone
# Description: A small python script to operate the Thermocycler Module WITHOUT OT-2 Robot.
# Repository: https://github.com/mtoutai/ot_thermocycler_standalone.git
# Author: Mitsuyama Toutai, Ph.D. https://orcid.org/0000-0002-1110-6375
# License: Apache-2.0
# 

import PySimpleGUI as sg
import asyncio
import os
import sys
import time
from collections import deque
from TCdriver import Thermocycler
import statistics

delay_start = None
gra_ids = deque()

async def connect(tc: Thermocycler):
    await tc.connect(port='/dev/ttyACM1')

async def open_lid(tc: Thermocycler):
    await tc.open()

async def close_lid(tc: Thermocycler):
    await tc.close()

async def deactivate_all(tc: Thermocycler):
    await tc.deactivate_all()

def prep_job_func(job, hold_time_str, temp_str, lid_temp_str):
    # print(f"prep_job_func(job={job},hold_time_str={hold_time_str},temp_str={temp_str},lid_temp_str={lid_temp_str})")
    init_time = time.time() + 1.0
    begin_at = init_time
    if len(job) > 0:
        begin_at = job[-1][0]
        if job[-1][1] != None:
            begin_at = begin_at + job[-1][1]
    # sys.stderr.write('prep_job_func: begin_at=%f\n' % begin_at)
    hold_time = None
    temp = None
    lid_temp = None
    try:
        hold_time = min(3600, max(1, float(hold_time_str)))
    except ValueError:
        pass
    try:
        temp = min(100, max(4, float(temp_str)))
    except ValueError:
        passhold_time  = {hold_time}
    try:
        lid_temp = min(110, max(4, float(lid_temp_str)))
    except ValueError:
        pass
    if temp != None or lid_temp != None:
        job.append([begin_at, hold_time, temp, lid_temp])
        print(f"job={job}")

def add_waiting(tc: Thermocycler, job):
    # print(f"add_waiting(job={job}")
    job_new = []
    for i in range(len(job)):
        d1 = 0
        d2 = 0
        begin_at = job[i][0]
        if i == 0:
            d1 = abs(job[0][2] - tc._current_temp)
            d2 = abs(job[0][3] - tc._lid_temp)
        else:
            d1 = abs(job[i][2] - job[i-1][2])
            d2 = abs(job[i][3] - job[i-1][3])
            if len(job_new) > 0:
                begin_at = job_new[-1][0] + job_new[-1][1]
        if d1 > 10 or d2 > 10:
            d = max(d1, d2) / 10
            delay = d * d * 5
            job_new.append([begin_at, delay, job[i][2], job[i][3]])
            job_new.append([begin_at + delay, job[i][1], job[i][2], job[i][3]])
    return job_new

def debug_print_job(job):
    # print(f"debug_print_job(job={job}")
    for j in job:
        s0 = '-'
        s1 = '-'
        s2 = '-'
        s3 = '-'
        try:
            s0 = time.asctime(time.localtime(j[0]))
        except ValueError:
            pass
        try:
            s1 = '%d' % j[1]
        except TypeError:
            pass
        try:
            s2 = '%g' % j[2]
        except TypeError:
            pass
        try:
            s3 = '%g' % j[3]
        except TypeError:
            pass
        sys.stderr.write('%s %s %s %s\n' % (s0, s1, s2, s3))

def prep_job(window, tc: Thermocycler, save_value, job):
    # print(f"prep_job(save_value={save_value}, prep_job(job={job})")
    for a in range(5):
        k1 = 'c%d' % (a+1)
        if window[k1].Get() != '':
            s0 = window[k1].Get()
            v0 = int(s0)
            save_value[k1] = s0
            for c in range(v0):
                for b in range(5):
                    k2 = 'c%d%d' % (a+1, b+1)
                    k21 = '%s_time' % k2
                    k22 = '%s_btemp' % k2
                    k23 = '%s_ltemp' % k2
                    v1 = window[k21].Get()
                    v2 = window[k22].Get()
                    v3 = window[k23].Get()
                    if v1 != None:
                        save_value[k21] = v1
                    if v2 != None:
                        save_value[k22] = v2
                    if v3 != None:
                        save_value[k23] = v3
                    prep_job_func(job, v1, v2, v3)
    # job = add_waiting(tc, job)
    # debug_print_job(job)

def mean(list):
    # print(f"mean(list={list})")
    if len(list) == 0:
        return 0
    sum = 0
    for i in list:
        sum = sum + i
    return sum / len(list)

def is_block_stabilized(temp):
    # print(f"is_block_stabilized(temp={temp})")
    if temp == None:
        return False
    e = len(log)
    if e < 30:
        return False
    s = max(0, e - 30)
    d = 1
    v = []
    for i in range(s, e):
        v.append(log[i][2])
    d = abs(statistics.mean(v) - temp)
    if d < 1:
        return True
    return False

def is_lid_stabilized(temp):
    # print(f"is_lid_stabilized(temp={temp})")
    if temp == None:
        return False
    e = len(log)
    if e < 30:
        return False
    s = max(0, e - 30)
    d = 30
    v = []
    for i in range(s, e):
        v.append(log[i][3])
    d = abs(statistics.mean(v) - temp)
    if temp >= 90 and d < 10:
        return True
    if temp < 90:
        return True
    return False

def delay_schedule(job, delay):
    for i in range(len(job)):
        job[i][0] = job[i][0] + delay

def load_job(window, job_file='pcr_gui.value'):
    jv = None
    try:
        jv = open(job_file, 'r')
    except IOError:
        sys.stderr.write('load_job: \'%s\' is not found.\n' % job_file)
        return
    for row in jv.readlines():
        key, value = row[:-1].split('\t')
        try:
            window[key].Update(value)
        except ValueError:
            sys.stderr.write('load_job: \'%s\' widget is not found.\n' % key)
    jv.close()

def save_job(job_value):
    # print(f"save_job(job_value={job_value})")
    jv = open('pcr_gui.value', 'w')
    for key in job_value.keys():
        jv.write('%s\t%s\n' % (key, job_value[key]))
    jv.close()

def run(window, tc: Thermocycler, job):
    # print(f"run(job={job})")
    global delay_start
    ct = time.time()
    if len(job) == 0:
        # print(f"run if 1")
        job_value = {}
        prep_job(window, tc, job_value, job)
        save_job(job_value)
    elif tc._target_temp != None and not is_block_stabilized(tc._target_temp):
        # print(f"run elif 2")
        if delay_start == None:
            delay_start = ct
    else:
        # print(f"run else 3")
        if delay_start != None:
            delay = ct - delay_start
            delay_schedule(job, delay)
            delay_start = None
        # print(f"job[{0}]: {job[0]}")
        begin_at, hold_time, temp, lid_temp = job[0]
        # print(f"hold_time  = {hold_time}")
        # sys.stderr.write('time=%f begin_at=%f\n' % (time.time(), begin_at))
        if time.time() > begin_at:
            # print(f"hold_time  = {hold_time}")
            temp_str = '-'
            hold_time_str = '-'
            if temp != None:
                temp_str = '%g' % temp
                if hold_time != None:
                    hold_time_str = '%d' % hold_time
                print(f"Set temp")
                asyncio.run(tc.set_temperature(temp, hold_time))
            else:
                print(f"deactivate block")
                asyncio.run(tc.deactivate_block())
            lid_temp_str = '-'
            if lid_temp != None:
                lid_temp_str = '%g' % lid_temp
                asyncio.run(tc.set_lid_temperature(lid_temp))
            else:
                asyncio.run(tc.deactivate_lid())
            sys.stderr.write('run: %s %s %s %s\n' % (time.asctime(time.localtime(begin_at)), hold_time_str, temp_str, lid_temp_str))
            job.popleft()
            if len(job) == 0:
                return False
        etc = time.asctime(time.localtime(job[-1][0]))
        window['ETC'].Update(value=etc)
    return True

def update_graph(window, tc: Thermocycler, log, plot_span):
    global gra_ids
    temp = deque()
    lid_temp = deque()
    i = len(log) - 1
    while i >= 0 and log[-1][0] - log[i][0] <= 1:
        lid_temp.append(log[i][1])
        temp.append(log[i][2])
        i = i - 1
        # sys.stderr.write('update_graph: i=%d\n' % i)
    if len(lid_temp) > 5 and len(temp) > 5:
        if lid_temp[0] == None:
            pass
        else:
            plot_span.append([statistics.mean(lid_temp), statistics.mean(temp)])
    # sys.stderr.write('update_graph: len(plot_span)=%d\n' % len(plot_span))
    x = len(plot_span)
    if x == 0:
        for temp in range(10, 120, 10):
            gra_ids.append(window['graph'].DrawLine(point_from=(0, temp), point_to=(900, temp), color='#888888'))
            gra_ids.append(window['graph'].DrawText('%2d' % temp, location=(20, temp), color='#555555'))
    elif x == 1:
        y1 = plot_span[-1][0]
        y2 = plot_span[-1][1]
        window['graph'].DrawPoint(point=(x, y1), size=5, color='#ffff00')
        window['graph'].DrawPoint(point=(x, y2), size=5, color='#ff00ff')
    elif x > 1:
        y11 = plot_span[-1][0]
        y12 = plot_span[-2][0]
        y21 = plot_span[-1][1]
        y22 = plot_span[-2][1]
        window['graph'].DrawLine(point_from=(x, y11), point_to=(x-1, y12), width=2, color='#ffff00')
        window['graph'].DrawLine(point_from=(x, y21), point_to=(x-1, y22), width=2, color='#ff00ff')
        if x == 900:
            plot_span.popleft()
            window['graph'].Move(-1, 0)
            for id in gra_ids:
                window['graph'].MoveFigure(id, 1, 0)
    window['CT'].Update(value=time.asctime())

def save_log(log):
    t = time.time()
    ct = time.localtime(t)
    millisec = t - int(t)
    time_str = '%04d%02d%02d_%02d%02d%02d.%02d' % (ct.tm_year, ct.tm_mon, ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec, round(millisec*100))
    log_fname = 'tc-%s.log' % time_str
    log_file = open(log_fname, 'w')
    for i in log:
        time_time, lid_temp, block_temp = i
        time_msec = round(time_time - int(time_time) * 100)
        time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time_time)) + '.%02d' % time_msec
        log_file.write('%s\t%g\t%g\n' % (time_str, lid_temp, block_temp))
    log_file.close()

async def interrupt_callback(res):
    sys.stderr.write(res)

if __name__=='__main__':
    sg.theme('DarkAmber')
    layout = [ [sg.Text('Incubation #1 cycles'), sg.InputText(size=(3,1), key='c1')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c11_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c11_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c11_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c12_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c12_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c12_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c13_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c13_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c13_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c14_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c14_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c14_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c15_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c15_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c15_ltemp')],
               [sg.Text('Incubation #2 cycles'), sg.InputText(size=(3,1), key='c2')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c21_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c21_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c21_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c22_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c22_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c22_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c23_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c23_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c23_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c24_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c24_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c24_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c25_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c25_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c25_ltemp')],
               [sg.Text('Incubation #3 cycles'), sg.InputText(size=(3,1), key='c3')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c31_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c31_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c31_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c32_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c32_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c32_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c33_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c33_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c33_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c34_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c34_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c34_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c35_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c35_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c35_ltemp')],
               [sg.Text('Incubation #4 cycles'), sg.InputText(size=(3,1), key='c4')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c41_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c41_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c41_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c42_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c42_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c42_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c43_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c43_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c43_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c44_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c44_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c44_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c45_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c45_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c45_ltemp')],
               [sg.Text('Incubation #5 cycles'), sg.InputText(size=(3,1), key='c5')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c51_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c51_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c51_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c52_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c52_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c52_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c53_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c53_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c53_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c54_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c54_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c54_ltemp')],
               [sg.Text('Time [sec]'), sg.InputText(size=(5,1), key='c55_time'), sg.Text('Block Temp. [Celsius]'), sg.InputText(size=(4,1), key='c55_btemp'), sg.Text('Lid Temp. [Celsius]'), sg.InputText(size=(4,1), key='c55_ltemp')],
               [sg.Button('Open'), sg.Button('Close'), sg.Button('Run'), sg.Button('Stop'), sg.Button('Deactivate'), sg.Button('Save Log')],
               [sg.Button('F1'), sg.Button('F2'), sg.Button('F3'), sg.Button('F4'), sg.Button('F5'), sg.Button('F6'), sg.Button('F7'), sg.Button('F8')],
               [sg.Text('Estimated Time of Completion'), sg.InputText(size=(23,1), key='ETC'), sg.Text('Current Time'), sg.InputText(size=(23,1), key='CT')],
               [sg.Graph(canvas_size=(640, 480), graph_bottom_left=(0,0), graph_top_right=(900,120), key='graph', background_color='#000000')] ]
    window = sg.Window('Opentrons Thermocycler', layout)
    tc = Thermocycler(interrupt_callback)
    asyncio.run(connect(tc))
    run_flag = False
    log = deque()
    plot_span = deque()
    ten_count = 0
    job = deque()
    while True:
        event, values = window.read(timeout=100)
        if event == 'Open':
            run_flag = False
            asyncio.run(deactivate_all(tc))
            asyncio.run(open_lid(tc))
        if event == 'Close':
            run_flag = False
            asyncio.run(deactivate_all(tc))
            asyncio.run(close_lid(tc))
        if event == 'Stop':
            run_flag = False
            asyncio.run(deactivate_all(tc))
        if event == 'Deactivate' or event == None:
            run_flag = False
            asyncio.run(deactivate_all(tc))
            save_log(log)
            break
        if event == 'Save Log':
            save_log(log)
            pass
        if event == 'Run':
            run_flag = True
            job = deque()
        if event == 'F1':
            if os.path.exists('F1.value'):
                load_job(window, job_file='F1.value')
        if event == 'F2':
            if os.path.exists('F2.value'):
                load_job(window, job_file='F2.value')
        if event == 'F3':
            if os.path.exists('F3.value'):
                load_job(window, job_file='F3.value')
        if event == 'F4':
            if os.path.exists('F4.value'):
                load_job(window, job_file='F4.value')
        if event == 'F5':
            if os.path.exists('F5.value'):
                load_job(window, job_file='F5.value')
        if event == 'F6':
            if os.path.exists('F6.value'):
                load_job(window, job_file='F6.value')
        if event == 'F7':
            if os.path.exists('F7.value'):
                load_job(window, job_file='F7.value')
        if event == 'F8':
            if os.path.exists('F8.value'):
                load_job(window, job_file='F8.value')
        if run_flag:
            run_flag = run(window, tc, job)
        if ten_count == 0:
            load_job(window)
            update_graph(window, tc, log, plot_span)
        if ten_count == 10:
            update_graph(window, tc, log, plot_span)
            ten_count = 1
        ten_count = ten_count + 1
        log.append([time.time(), tc._lid_temp, tc._current_temp])
        # sys.stderr.write('ten_count=%d\n' % ten_count)
    if tc.is_connected():
        tc.disconnect()
    window.close()

