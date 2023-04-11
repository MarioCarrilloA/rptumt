import cv2
import numpy as np
import datetime
import platform

img = np.zeros([720, 1280, 3], dtype=np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 255, 0)
thickness = 2
image = cv2.putText(img, 'No available data to display', (100, 100), font,
                                       fontScale, color, thickness, cv2.LINE_AA)
system = str("Platform: " + platform.system() + " - " + platform.machine())
ct = str("System initialized: " + datetime.datetime.now().strftime('%d-%M-%Y'))
image = cv2.putText(img, system, (100, 200), font,
                                       fontScale, color, thickness, cv2.LINE_AA)

image = cv2.putText(img, ct, (100, 300), font,
                                       fontScale, color, thickness, cv2.LINE_AA)


cv2.imshow("test", img)
cv2.waitKey(0)
