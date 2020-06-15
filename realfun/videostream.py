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
current_state = 'Nothing is going on!'
# All the stuff inside our window.
layout = [             
            [sg.Frame(layout=[
            [sg.Radio('UDP    ', "RADIO1", default=True, size=(10,1)), sg.Radio('RTSP', "RADIO1",default=False)]], title='Protocol',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='RTP or RTSP')],      
            [sg.Frame(layout=[
            [sg.Text('IP client', size=(10,1)), sg.InputText('172.23.40.58')], 
            [sg.Text('Port ', size=(10,1)), sg.InputText('5000')]] ,title='UDP', title_color='red', tooltip='IP+Port UDP Client')], 
            [sg.Frame(layout=[
            [sg.Text('rtsp://'+myip+':8554/test')]], title='RTSP', title_color='red')],     
            [sg.Text('Bitrate [bit/s]', size=(15,1)), sg.InputText('1000000')],
            [sg.Text('Framerate [fps]', size=(15,1)), sg.Listbox(framerates_ch, size=(15,len(framerates_ch)), key='-FRAMERATE-', default_values=framerates_ch[1])],
            [sg.Text('Width', size=(15,1)), sg.InputText('720')],
            [sg.Text('Height', size=(15,1)), sg.InputText('480')],
            #[sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3), default_values='Listbox 2' , enable_events=True) ],         
            [sg.Button('Stream'), sg.Button('Close'), sg.Button('Stop')] ,
            [sg.Text('_'  * 80)],    
            [sg.Text(current_state, size=(70, 5), key='-PL-', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)]]

# Create the Window
window = sg.Window('Video Stream Parameters', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':	# if user closes window or clicks cancel
        print('UDP', values[0])
        print('RTSP', values[1])

        print('IP Address', values[2])
        print('Port', values[3])
    
        print('Bitrate', values[4])
        print('Framerate', values['-FRAMERATE-'][0])
        print('Width', values[5])
        print('Height', values[6])
        if current_state == 'Nothing is going on!':
            break
        else:
            window['-PL-'].update('It seems that there is some streaming going on, stop streaming first')
            

    if event == 'Stop':
        print("Desire to stop")
        if values[0] == True:
            os.system("pkill -f gst-launch-1.0")
            window['-PL-'].update("gst-launch-1.0 Killed!")
        else:
            os.system("pkill -f test-launch")
            window['-PL-'].update("test-launch Killed!")
            #os.system("echo 1 > sudo systemctl restart nvargus-daemon")
        current_state = 'Nothing is going on!'
        
    if event == 'Stream':
        ourpipeline = ""
        if values[0] == True:
            ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! \'video/x-raw(memory:NVMM), format=NV12, width="+values[5]+" , height="+values[6]+", framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! \'video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            ourpipeline = ourpipeline + values['-FRAMERATE-'][0]+"/1\' ! nvv4l2h264enc insert-sps-pps=true bitrate="+values[4]+ " ! h264parse ! rtph264pay pt=96 ! udpsink host="+values[2]+" port="+values[3]+" sync=false -e &"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=" #10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
            #ourpipeline = "gst-launch-1.0 nvarguscamerasrc ! '\''video/x-raw(memory:NVMM), format=NV12, width=720, height=480, framerate=10/1'\'' ! nvv4l2h264enc insert-sps-pps=true bitrate=500000 ! h264parse ! rtph264pay pt=96 ! udpsink host=172.23.40.58 port=5000 sync=false -e"
        else:
            ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)'+values[5]+', height=(int)'+values[6]+', format=(string)NV12, framerate=(fraction)' #10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            #ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)' #10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            ourpipeline = ourpipeline+values['-FRAMERATE-'][0]+'/1 ! nvv4l2h264enc insert-sps-pps=true bitrate='+values[4]+' ! h264parse !   rtph264pay name=pay0 pt=96 )" &'
            #ourpipeline = ourpipeline+values['-FRAMERATE-'][0]+'/1 ! nvv4l2h264enc insert-sps-pps=true bitrate='+values[4]+' ! h264parse !   rtph264pay name=pay0 pt=96 )"'
            #ourpipeline = 'test-launch "( nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)720, height=(int)480, format=(string)NV12, framerate=(fraction)10/1 ! nvv4l2h264enc insert-sps-pps=true bitrate=1000000 ! h264parse !   rtph264pay name=pay0 pt=96 )"'
        print(ourpipeline)
        window['-PL-'].update(ourpipeline)
        print("Our IP is "+myip)
        current_state = 'Streaming'
        our_process = mp.Process(target=os.system(ourpipeline))
        our_process.start()
        #os.system(ourpipeline)
    

window.close()