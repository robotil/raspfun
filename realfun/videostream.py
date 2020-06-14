#!/usr/bin/python3
import PySimpleGUI as sg

sg.theme('BluePurple')	# Add a touch of color
framerates_ch = ('5','10', '15', '20', '25', '30')
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('IP address of streamer or udp client:'), sg.InputText('172.23.40.63')],
            [sg.Text('Port:'), sg.InputText('8554')],
            [sg.Frame(layout=[
            [sg.Radio('UDP    ', "RADIO1", default=False, size=(10,1)), sg.Radio('RTSP', "RADIO1",default=True)]], title='Protocol',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],      

            [sg.Text('bitrate [bit/s]'), sg.InputText('1000000')],
            [sg.Text('framerate [fps]'), sg.Listbox(framerates_ch, size=(15,len(framerates_ch)), key='-FRAMERATE-', enable_events=True)],
            
            
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Video Stream Parameters', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    if event == 'Ok':
        ourpipeline = ""
        if values[2] == True:
            ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
        else:
            ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)"' #10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            #ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
        print(ourpipeline)
    print('IP Address', values[0])
    print('Port', values[1])
    print('UDP', values[2])
    print('RTSP', values[3])
    print('Bitrate', values[4])
    print('framerate', values['-FRAMERATE-'][0])

window.close()