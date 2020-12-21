sudo apt-get update

sudo pip3 install mavproxy

sudo apt-get install python3-wxgtk3.0 libxml2-dev python3-pip python3-matplotlib python3-lxml
Not good. python3-wxgtk3.0 doesn't exist.
References:
https://www.raspberrypi.org/forums/viewtopic.php?t=235820
I installed:
	sudo apt install python-wxgtk3.0
and then:
	sudo apt-get install python3-dev python3-opencv libxml2-dev python3-pip python3-matplotlib python3-lxml
and then:
sudo apt-get install python-dev python-opencv python-wxgtk3.0 python-pip python-matplotlib python-pygame python-lxml python-yaml

I got an idea and installed:
sudo apt install python3-wxgtk4.0

and then:
sudo pip3 install future and sudo pip install future
sudo pip3 install pymavlink sudo pip install pymavlink
just in case sudo pip install mavproxy

python3 -m site --user-site:
/home/pi/.local/lib/python3.7/site-packages
python -m site --user-site:
/home/pi/.local/lib/python2.7/site-packages

python2:
mavproxy.py --master=/dev/serial0 --baudrate 921600 --aircraft MyCopter
python3:
python3 /usr/local/lib/python3.7/dist-packages/MAVProxy/mavproxy.py <blablabla>

sudo apt install -y libgstreamer1.0-dev libgstrtspserver-1.0-0 libgstrtspserver-1.0

mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --out 192.168.137.1:14550 --aircraft MyCopter

sudo apt install aptitude

sudo aptitude install gstreamer1.0-tools

sudo apt install screen

gst-inspect x264enc

sudo apt install gstreamer1.0-plugins-ugly
sanity: gst-launch-1.0 v4l2src device=/dev/video1 ! videoconvert ! ximagesink

server:
	gst-launch-1.0 -v -e v4l2src device=/dev/video0  ! "video/x-raw,width=640,height=480,framerate=(fraction)30/1" ! videoconvert ! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast  ! rtph264pay ! udpsink host=172.23.40.132 port=5000
	
client:
    gst-launch-1.0 -e -v udpsrc port=5000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! decodebin ! videoconvert ! autovideosink sync=false
server also:
	gst-launch-1.0 -v -e v4l2src device=/dev/video0  ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast  ! rtph264pay ! udpsink host=192.168.0.11 port=5000


In order to know which raspberry you are using:
cat /sys/firmware/devicetree/base/model;echo
grep Model /proc/cpuinfo

check gpu memory behavior
sudo /opt/vc/bin/vcdbg reloc stats

OS details
cat /etc/os-release 

For Geany debug plugin:
git clone https://github.com/geany/geany-plugins
sudo apt install vim
sudo apt install intltool
sudo apt-get install libgtk-3-dev
./autogen.sh
make
sudo make install 

Backup:
sudo cat /etc/fstab
sudo dd if=/dev/mmcblk0p2 of=/home/pi/networkdrive/my.img bs=1M
Reference: https://raspberrytips.com/backup-raspberry-pi/#Create_an_image_of_the_SD_card
rsync -avz -e ssh pi@172.23.40.54:/boot boot
Actually:
	save: sudo dd bs=4M if=dev/sdb | gzip > rasp`date +%d%m%y`.gz
	restore: sudo gzip -dc /home/robil/<image.gz> | dd bs=4M of=/dev/sdb
		

gstreamer: 
https://gist.github.com/neilyoung/8216c6cf0c7b69e25a152fde1c022a5d
./test-launch --gst-debug=3 '( videotestsrc !  x264enc ! rtph264pay name=pay0 pt=96 )'
gst-launch-1.0 -v rtspsrc location=rtsp://172.23.40.54:8554/test latency=0 buffer-mode=auto ! decodebin ! videoconvert ! autovideosink sync=false

with camera:
./test-launch --gst-debug=3 "( rpicamsrc bitrate=8000000 awb-mode=tungsten preview=false ! video/x-h264, width=640, height=480, framerate=30/1 ! h264parse ! rtph264pay name=pay0 pt=96 )"

RTSP good:
./test-launch "v4l2src device=/dev/video0  num-buffers=9000 ! video/x-raw, width=640, height=480, framerate=(fraction)30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast  ! rtph264pay name=pay0"
RTSP better:
./test-launch --gst-debug=3 "v4l2src device=/dev/video0  num-buffers=9000 ! video/x-raw, width=640, height=480, framerate=(fraction)30/1 ! videoconvert ! video/x-raw, format=I420 ! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast  ! rtph264pay name=pay0"

Starting to try:
./test-launch --gst-debug=3 "( v4l2src device=/dev/video0  ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast  ! rtph264payname=pay0 pt=96 )"
or: GST_DEBUG=2,v4l2*=7 ./test-launch "v4l2src device=/dev/video0 num-buffers=9000 ! video/x-raw,width=(int)720,height=(int)576,format=UYVY, interlace-mode=interleaved ! nvvidconv ! video/x-raw(memory:NVMM),width=(int)1920,height=(int)1080,framerate=30/1,format=NV12 ! nvv4l2h264enc bufapi-version=True ! h264parse ! rtph264pay name=pay0"

or: GST_DEBUG=2,v4l2*=7 ./test-launch "v4l2src device=/dev/video0 num-buffers=9000 ! video/x-raw,width=(int)640,height=(int)480,format=UYVY, interlace-mode=interleaved ! videoconvert ! video/x-raw,width=(int)1920,height=(int)1080,framerate=30/1 ! x264enc ! h264parse ! rtph264pay name=pay0"

/test-launch --gst-debug=3 "(v4l2src device=/dev/video0  ! \"video/x-raw,width=640,height=480,framerate=(fraction)30/1\" ! videoconvert ! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast  ! rtph264pay name=pay0)"









client

***************** MIPI TCP:
streamer:
	raspivid -t 0 -w 640 -h 480 -fps 48 -b 2000000 -awb tungsten  -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=0.0.0.0 port=5000
client:
	gst-launch-1.0 -v tcpclientsrc host=172.23.40.54 port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert  ! autovideosink sync=false

****************** RTSP
streamer:
	./leg-test-launch --gst-debug=3 "( rpicamsrc bitrate=8000000 awb-mode=tungsten preview=false ! video/x-h264, width=640, height=480, framerate=30/1 ! h264parse ! rtph264pay name=pay0 pt=96 )"
client:
	gst-launch-1.0 -v rtspsrc location=rtsp://172.23.40.54:8554/test latency=0 buffer-mode=auto ! decodebin ! videoconvert ! autovideosink sync=false

*****************************************************************************************************************

Debugging RTSP server:
Compile one test:
gcc -g -o test-launch  test-launch.c  `pkg-config --cflags --libs gstreamer-rtsp-server-1.0`
BTW:
pkg-config --cflags --libs gstreamer-rtsp-server-1.0 = 
-pthread -I/usr/local/include/gstreamer-1.0 -I/usr/include/gstreamer-1.0 -I/usr/include/glib-2.0 
-I/usr/lib/arm-linux-gnueabihf/glib-2.0/include -L/usr/local/lib -lgstrtspserver-1.0 -lgstbase-1.0 
-lgstreamer-1.0 -lgobject-2.0 -lglib-2.0


Visual Code:
Reference: https://pimylifeup.com/raspberry-pi-visual-studio-code/

jtop
sudo -H pip install -U jetson-stats



