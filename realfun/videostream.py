#!/usr/bin/python3
import PySimpleGUI as sg
import os, sys
import multiprocessing as mp
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

sg.theme('BluePurple')	# Add a touch of color
framerates_ch = ('5','10', '15', '20', '25', '30')
myip = get_ip()
# All the stuff inside our window.
layout = [  
            [sg.Text('IP address of UDP client:'), sg.InputText('172.23.40.58')],
            [sg.Text('Port for UDP:'), sg.InputText('5000')],
            [sg.Frame(layout=[
            [sg.Radio('UDP    ', "RADIO1", default=True, size=(10,1)), sg.Radio('RTSP', "RADIO1",default=False)]], title='Protocol',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],      

            [sg.Text('bitrate [bit/s]'), sg.InputText('1000000')],
            [sg.Text('framerate [fps]'), sg.Listbox(framerates_ch, size=(15,len(framerates_ch)), key='-FRAMERATE-', default_values=framerates_ch[1])],
            [sg.Text('WidthxHeight='), sg.InputText('720'), sg.Text('x'), sg.InputText('480')],
            #[sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3), default_values='Listbox 2' , enable_events=True) ],         
            [sg.Button('Stream'), sg.Button('Cancel'), sg.Button('Stop')] ]

# Create the Window
window = sg.Window('Video Stream Parameters', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        print('width', values[5])
        print('height', values[6])
        break
    if event == 'Stop':
        print("Desire to stop")
        if values[2] == True:
            os.system("pkill -f gst-launch")
        else:
            os.system("pkill -f test-launch")
        print("Killed!")
    if event == 'Stream':
        ourpipeline = ""
        if values[2] == True:
            ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! \'video/x-raw(memory:NVMM), format=NV12, width="+values[5]+" , height="+values[6]+", framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! \'video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            ourpipeline = ourpipeline + values['-FRAMERATE-'][0]+"/1\' ! nvv4l2h264enc insert-sps-pps=true bitrate="+values[4]+ " ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e &"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
        else:
            ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)'+values[5]+', height=(int)'+values[6]+', format=(string)NV12, framerate=(fraction)' #10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            #ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)' #10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            ourpipeline = ourpipeline+values['-FRAMERATE-'][0]+'/1 ! nvv4l2h264enc insert-sps-pps=true bitrate='+values[4]+' ! h264parse !   rtph264pay name=pay0 pt=96 )" &'
            #ourpipeline = ourpipeline+values['-FRAMERATE-'][0]+'/1 ! nvv4l2h264enc insert-sps-pps=true bitrate='+values[4]+' ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            #ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
        print(ourpipeline)
        
        print("Our IP is "+myip)
        our_process = mp.Process(target=os.system(ourpipeline))
        our_process.start()
        #os.system(ourpipeline)
    # print('IP Address', values[0])
    # print('Port', values[1])
    # print('UDP', values[2])
    # print('RTSP', values[3])
    # print('Bitrate', values[4])
    # print('framerate', values['-FRAMERATE-'][0])
    # print('width', values[6])

window.close()