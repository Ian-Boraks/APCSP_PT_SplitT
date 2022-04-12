"""
This file is a heavily modified version of https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_Timer.py

The original code is licensed under the GNU Lesser General Public License v3.0 (https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt).
This means that we can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the original code, as long as we include the original License and copyright notice, Disclose source, State changes, and the project is licensed under the Same license.
"""

import _thread
import asyncio
import split_watcher as sw
import PySimpleGUI as sg
import time


user_times = []
splitNumber = 0

def time_as_int():
    return int(round(time.time() * 100))
def format_time():
    return window['-TIMER-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))

def callOnSplit():
  user_times.append(current_time)
  currentF = open('current_run.csv', 'a+')
#   currentF.writelines(str(splitNumber) + ", " + str(user_times[-1]) + "\n")
  currentF.writelines(str(splitNumber) + ", " + str(current_time) + "\n")

  currentF.close()

def endSplitWatch():
  print("endSplitWatch")
#   splitWatch.exit_program = True
#   splitWatchThread.join()
  exit()

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

splitWatch = sw.splitWatcher(callOnSplit, endSplitWatch, window)

def startSplitWatch():
  asyncio.run(splitWatch.start())

_thread.start_new_thread(startSplitWatch, ())

current_time, paused_time, paused = 0, 0, True
start_time = time_as_int()

def format_time():
    return window['-TIMER-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                    (current_time // 100) % 60,
                                                    current_time % 100))

def doEventWindows(event):
    global paused_time
    global current_time
    global paused
    global start_time
    global splitNumber

    match event:
        case sg.WIN_CLOSED | 'Exit':
            splitWatch.exit_program = True
            del splitWatch
            print('Exit')
            return True
        case '-RESET-':
            paused_time = start_time = time_as_int()
            current_time = 0
            splitNumber = 0
            window['-SPLIT-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                            (current_time // 100) % 60,
                                                            current_time % 100))
            format_time()
            print('Reset')
            if not paused: 
                doEventWindows('-RUN-PAUSE-')
            return False
        case '-RUN-PAUSE-':
            paused = not paused
            if paused:
                paused_time = time_as_int()
            else:
                start_time = start_time + time_as_int() - paused_time
            print('Run or Pause')
            return False
        case '-SPLIT-TIMER-':
            if (splitNumber == 0 and paused):
                doEventWindows('-RUN-PAUSE-')
                return False
            elif (paused):
                return False
            else:    
                callOnSplit()
                splitNumber += 1
                window['-SPLIT-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                            (current_time // 100) % 60,
                                                            current_time % 100))
                # Change button's text
                window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
                print('Split')
            return False

def main():
  global paused_time
  global current_time
  global paused
  global start_time
  global splitNumber
  doEventWindows('-RESET-')

  while True:
  # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
        # print(event, values)
    else:
        event, values = window.read()
        print(event, values)
    # --------- Do Button Operations --------
   
    if doEventWindows(event):
        break
            
    # if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
    #     # splitWatch.exit_program = True
    #     # del splitWatch
    #     break
    # if event == '-RESET-':
    #     paused_time = start_time = time_as_int()
    #     current_time = 0
    #     splitNumber = 0
    # elif event == '-RUN-PAUSE-':
    #     paused = not paused
    #     if paused:
    #         paused_time = time_as_int()
    #     else:
    #         start_time = start_time + time_as_int() - paused_time
    # elif event == '-SPLIT-TIMER-':
    #     # user_times.append('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
    #     #                                             (current_time // 100) % 60,
    #     #                                             current_time % 100))
    #     callOnSplit()

    #     splitNumber += 1
    #     window['-SPLIT-TEXT-'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
    #                                                  (current_time // 100) % 60,
    #                                                  current_time % 100))
    #     # Change button's text
    #     window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    # --------- Display timer in window --------
    format_time()

if __name__ == "__main__":
  main()