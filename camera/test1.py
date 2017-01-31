import picamera

camera = picamera.PiCamera()
camera.capture('image.jpg')
camera.hflip = True
camera.vflip = True
#camera.start_preview()
#camera.stop_preview()
