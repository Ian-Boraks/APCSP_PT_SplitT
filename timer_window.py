"""
This file is a heavily modified version of https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_Timer.py

The original code is licensed under the GNU Lesser General Public License v3.0 (https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt).
This means that we can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the original code, as long as we include the original License and copyright notice, Disclose source, State changes, and the project is licensed under the Same license.
"""

import PySimpleGUI as sg
import time


user_times = []

def time_as_int():
    return int(round(time.time() * 100))
def format_time():
    return window['-TIMER-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))

# ----------------  Create Form  ----------------
sg.theme('Black')

layout = [[sg.Text('')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 20),
                justification='center', key='-TIMER-TEXT-'),
           sg.Text('', size=(8, 2), font=('Helvetica', 20), 
                justification='center', key='-SPLIT-TEXT-')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
           sg.Exit(button_color=('white', 'firebrick4'), key='Exit'), 
           sg.Button('Split', key='-SPLIT-TIMER-', button_color=('white', '#ff0000'))]]

window = sg.Window('Running Timer', layout,
                   no_titlebar=False,
                   auto_size_buttons=True,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   finalize=True,
                   element_justification='c',
                   right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT,
                   size = (500, 500),
                   resizable = True)

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

while True:
    def format_time():
        return window['-TIMER-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))
    # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
        # print(event, values)
    else:
        event, values = window.read()
        # print(event, values)
    # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
    if event == '-RESET-':
        paused_time = start_time = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
    elif event == '-SPLIT-TIMER-':
        user_times.append(current_time)
        runNumber = 2
        currentF = open('current_run.csv', 'a+')
        time_list = [1, 2, 3, 4, 5,]

        # currentF.writelines("run " + str(runNumber) + "\n")
        for i in time_list:
            currentF.writelines(str(i) + ", run"  + str(runNumber) + "\n") 
        window['-SPLIT-TEXT-'].update(user_times)
        # Change button's text
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    # --------- Display timer in window --------
    format_time()


window.close()
