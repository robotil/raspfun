from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.annotate_text_size = 50
camera.brightness = 70
#camera.image_effect = 'colorswap'
camera.start_preview()
#camera.start_preview(alpha=200)

# for i in range(5):
#     sleep(5)
#     camera.capture('/home/pi/Desktop/image1%s.jpg' % i)
# camera.stop_preview()
# print("Let's take a little nap!")
# sleep(2)
# print("Now, let's do a short movie!")
# camera.start_preview()
# camera.start_recording('/home/pi/Desktop/michele.h264')
# sleep(5)
# camera.stop_recording()
# camera.stop_preview()

print("Now, let's play with color!")
camera.start_preview()
camera.annotate_background = Color('blue')
camera.annotate_foreground = Color('yellow')
camera.annotate_text = " Hello world "
sleep(2)
camera.stop_preview()

print("Let's check brightness")
camera.start_preview()
for i in range(100):
    camera.annotate_text = "Brightness: %s" % i
    camera.brightness = i
    sleep(0.1)
camera.stop_preview()
camera.brightness = 70
print("Let's check contrast")
camera.start_preview()
for i in range(100):
    camera.annotate_text = "Contrast: %s" % i
    camera.contrast = i
    sleep(0.1)
camera.stop_preview()
camera.contrast = 50
print("Now, let's play with all the effects!")
camera.start_preview()
for effect in camera.IMAGE_EFFECTS:
    camera.image_effect = effect
    camera.annotate_text = "Effect: %s" % effect
    sleep(5)
camera.stop_preview()