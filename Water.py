import numpy as np
import cv2

# Detecting reflection of sky in water
imgHSB = cv2.imread('green2.png')
imgHSB = cv2.cvtColor(imgHSB, cv2.COLOR_BGR2HSV)
lower_blue = np.array([75, 40, 124])
upper_blue = np.array([100, 255, 255])

mask = cv2.inRange(imgHSB, lower_blue, upper_blue)

cv2.imshow('img', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
