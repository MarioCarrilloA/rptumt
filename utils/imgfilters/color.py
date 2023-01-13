import cv2
import numpy as np
import time


def nothing(x):
    pass

# Main window
cv2.namedWindow('Results')

# Hue
cv2.createTrackbar('lowerH', 'Results', 150, 179, nothing)
cv2.createTrackbar('upperH', 'Results', 160, 179, nothing)

# Saturation
cv2.createTrackbar('lowerS', 'Results', 0, 255, nothing)
cv2.createTrackbar('upperS', 'Results', 255, 255, nothing)

# Value
cv2.createTrackbar('lowerV', 'Results', 0, 255, nothing)
cv2.createTrackbar('upperV', 'Results', 255, 255, nothing)


#img = cv2.imread(imgfile)
#original = img.copy()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, img = cap.read()
    original = img.copy()
    bk = original.copy()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #img_blur_hsv = cv2.GaussianBlur(img_hsv, (7, 7), 3)
    img_blur_hsv = img_hsv

    lH = cv2.getTrackbarPos('lowerH', 'Results')
    uH = cv2.getTrackbarPos('upperH', 'Results')
    lS = cv2.getTrackbarPos('lowerS', 'Results')
    uS = cv2.getTrackbarPos('upperS', 'Results')
    lV = cv2.getTrackbarPos('lowerV', 'Results')
    uV = cv2.getTrackbarPos('upperV', 'Results')

    # define range of red color in HSV
    lower_th = np.array([lH, lS, lV])
    upper_th = np.array([uH, uS, uV])
    mask = cv2.inRange(img_blur_hsv, lower_th, upper_th)
    result = cv2.bitwise_and(bk, bk, mask=mask)

    cv2.imshow("mask", mask)
    cv2.imshow("Results", original)
    Hmax = np.amax(img_hsv[0])
    Hmin = np.amin(img_hsv[0])
    Smax = np.amax(img_hsv[1])
    Smin = np.amin(img_hsv[1])
    Vmax = np.amax(img_hsv[2])
    Vmin = np.amin(img_hsv[2])
    print("[HSV]=[MIN:MAX] -> Hmax=" + str(Hmin) + ":" + str(Hmax) +
            " Smin=" + str(Smin) + ":" + str(Smax) +
            " Vmin=" + str(Vmin) + ":" + str(Vmax))
    
    time.sleep(0.09)
    #frame = cv2.bitwise_and(frame, frame, mask=mask)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
