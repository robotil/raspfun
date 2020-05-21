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

gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! ximagesink

gst-inspect x264enc

sudo apt install gstreamer1.0-plugins-ugly

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

Backup:
sudo cat /etc/fstab
sudo dd if=/dev/mmcblk0p2 of=/home/pi/networkdrive/my.img bs=1M
https://raspberrytips.com/backup-raspberry-pi/#Create_an_image_of_the_SD_card
rsync -avz -e ssh pi@172.23.40.54:/boot boot
