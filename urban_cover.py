import numpy as np
import cv2

img = cv2.imread('test22.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
sky = 0
mask = np.zeros([img.shape[0], img.shape[1]])
# ================Detecting sky and its reflection in water =================
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        h, s, v = img[i, j]
        if (s <= 69 and v >= 140) or (80 <= h <= 110 and 27 > s > 10 and 60 < v):
            mask[i, j] = 255
# ============================================================================
imgOut = np.zeros((img.shape[0], img.shape[1]))
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        h, s, v = img[i, j]
        if 36 <= h <= 70:
            if 25 <= s <= 255:
                if 25 <= v <= 255:
                    imgOut[i, j] = 255
mask = mask + imgOut
cv2.imshow('Classified_image4.png', imgOut)
cv2.waitKey(0)
cv2.destroyAllWindows()