import cv2
import numpy as np

DEFULT_MINIMAL_AREA = 100

imgfile = "new.jpg"
#imgfile = "./vga_frame_307.png"
#imgfile = "./HD_frame_156.png"
#imgfile = "./fullHD_frame_135.png"



def nothing(x):
    pass

# Main window
cv2.namedWindow('Results')

# Hue
cv2.createTrackbar('lowerH', 'Results', 0, 179, nothing)
cv2.createTrackbar('upperH', 'Results', 179, 179, nothing)

# Saturation
cv2.createTrackbar('lowerS', 'Results', 0, 255, nothing)
cv2.createTrackbar('upperS', 'Results', 255, 255, nothing)

# Value
cv2.createTrackbar('lowerV', 'Results', 0, 255, nothing)
cv2.createTrackbar('upperV', 'Results', 255, 255, nothing)


img = cv2.imread(imgfile)
original = img.copy()
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_blur_hsv = img_hsv
#img_blur_hsv = cv2.GaussianBlur(img_hsv, (7, 7), 3)

while(1):
    bk = original.copy()
    lH = cv2.getTrackbarPos('lowerH', 'Results')
    uH = cv2.getTrackbarPos('upperH', 'Results')
    lS = cv2.getTrackbarPos('lowerS', 'Results')
    uS = cv2.getTrackbarPos('upperS', 'Results')
    lV = cv2.getTrackbarPos('lowerV', 'Results')
    uV = cv2.getTrackbarPos('upperV', 'Results')
    print("H={0}:{1}  S={2}:{3}  V={4}:{5}".format(
        lH, uH, lS, uS, lV, uV))

    # define range of red color in HSV
    lower_th = np.array([lH, lS, lV])
    upper_th = np.array([uH, uS, uV])
    mask = cv2.inRange(img_blur_hsv, lower_th, upper_th)
    result = cv2.bitwise_and(bk, bk, mask=mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) != 0):
        for contour in contours:
            if cv2.contourArea(contour) > DEFULT_MINIMAL_AREA:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(bk, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow("HSV image", img_hsv)
    cv2.imshow("Detection", bk)
    cv2.imshow("HSV image blur", img_blur_hsv)
    #cv2.imshow("original", img)
    cv2.imshow("mask", mask)
    cv2.imshow("Results", result)

    #frame = cv2.bitwise_and(frame, frame, mask=mask)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.imwrite("colorR2.png", result)
        cv2.imwrite("imgdec2.png", bk)
        break
cv2.destroyAllWindows()
