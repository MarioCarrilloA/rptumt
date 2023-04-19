import cv2
import os

imgfile = "./1280x720_iso_0_ss_0_id_0.jpg"

# this function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# read the experimental image
original = cv2.imread(imgfile)

# create trackbar for canny edge detection threshold changes
cv2.namedWindow('canny')

# add lower and upper threshold slidebars to "canny"
cv2.createTrackbar('lower', 'canny', 0, 255, nothing)
cv2.createTrackbar('upper', 'canny', 0, 255, nothing)

# Infinite loop until we hit the escape key on keyboard
while(1):
    img = original.copy()
    # get current positions of four trackbars
    lower = cv2.getTrackbarPos('lower', 'canny')
    upper = cv2.getTrackbarPos('upper', 'canny')


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, lower, upper)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) != 0):
        for contour in contours:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.putText(img, str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # display images
    cv2.imshow('original', img)
    cv2.imshow('canny', edges)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('s'):
        cv2.imwrite(str("canny_" + os.path.basename(imgfile)), edges)
        print("saved!")
    elif k == 27:
        break

cv2.destroyAllWindows()
