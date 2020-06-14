#!/usr/bin/python3
import PySimpleGUI as sg

sg.theme('BluePurple')	# Add a touch of color
framerates_ch = ('5','10', '15', '20', '25', '30')
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('UDP or RTSP'), sg.InputText()],
            [sg.Text('bitrate [bit/s]'), sg.InputText()],
            [sg.Text('framerate [fps]'), sg.Listbox(framerates_ch, size=(15,len(framerates_ch)), key='-FRAMERATE-', enable_events=True)],
            [sg.Text('IP address of streamer or udp client:'), sg.InputText()],
            [sg.Text('TCP/UDP Port:'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Video Stream Parameters', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    print('UDP or RTSP', values[0])
    print('bitrate', values[1])
    print('framerate', values['-FRAMERATE-'][0])

window.close()