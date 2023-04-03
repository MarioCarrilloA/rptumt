from picamera2 import Picamera2, Preview
import time

# Manual picamera2
#https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf


picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1280, 720)},
    lores={"size": (320, 240)}, display="lores")
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 2400})
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(5)
picam2.capture_file("test.png")
picam2.stop()
picam2.close()

