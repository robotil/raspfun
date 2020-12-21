Computer IMA, camera usb, rtp streaming




==================================================================================================

Apollo - Client - Decoder:

UDP
=========

gst-launch-1.0 -e -v udpsrc port=5000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! decodebin ! videoconvert ! autovideosink sync=false
gst-launch-1.0 -vv -e udpsrc port=5000 ! application/x-rtp, payload=96 ! rtph264depay ! queue ! avdec_h264 ! videoconvert ! autovideosink sync=false
gst-launch-1.0 -v -e udpsrc port=5000 ! application/x-rtp, payload=96 ! rtph264depay ! avdec_h264 ! timeoverlay halignment=right valignment=bottom ! videorate ! video/x-raw,framerate=1000/10001 ! jpegenc ! multifilesink location="/home/robil/Pictures/rtpframe%08d.jpg"

======================================================================================

RTSP:
====

gst-launch-1.0 rtspsrc location=rtsp://172.23.40.131:8554/test latency=100 ! decodebin ! xvimagesink
gst-launch-1.0 -v rtspsrc location=rtsp://172.23.40.130:8554/test ! rtph264depay ! avdec_h264 ! timeoverlay halignment=right valignment=bottom ! videorate ! video/x-raw,framerate=6000/1001 ! jpegenc ! multifilesink location="/home/robil/Pictures/frame%08d.jpg"
