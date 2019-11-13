import numpy as np
import cv2


imgHSB = cv2.imread('green2.png')
img = cv2.cvtColor(imgHSB, cv2.COLOR_BGR2GRAY)
mask = np.zeros(img.shape)
kSize = 9
l = kSize // 2
for i in range(l, img.shape[0] - l):
    for j in range(l, img.shape[1] - l):
        ar = img[i - l: i + l + 1, j - l: j + l + 1]
        var = np.var(ar)
        h, s, v = imgHSB[i, j]
        if var <= 13:
            mask[i, j] = 255
        else:
            mask[i, j] = 0

cv2.imshow('img', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()