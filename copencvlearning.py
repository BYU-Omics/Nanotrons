import cv2
import numpy as np

img = cv2.imread('foto.jpg', 1)
# img = cv2.resize(img, (0, 0), fx=0.5, fy = 0.5)
# img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

hsv = cv2.cvtColor(img, cv2.COLOR_HSV2BGR) # converts to hsv

lower_blue = np.array([70, 70, 70])
upper_blue = np.array([250, 250, 250])

mask = cv2.inRange(hsv, lowerb = lower_blue, upperb= upper_blue) # which pixels we should keep and which not

result = cv2.bitwise_and(img, img, mask=mask)

# cv2.imwrite('new_img.jpg', img) # to write a new image 

cv2.imshow('result', result)
cv2.imshow('mask', mask)
cv2.imshow('img', img)


cv2.waitKey(0)

cv2.destroyAllWindows()
