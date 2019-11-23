import cv2
import numpy as np


def get_green_percentage(img):
    imgOut = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            h, s, v = img[i, j]
            if 30 <= h <= 90:
                if 25 <= s <= 255:
                    if 10 <= v <= 255:
                        imgOut[i, j] = 255
                        count += 1
    percentage = count * 100 / (img.shape[0] * img.shape[1])
    return percentage, imgOut


img = cv2.imread('green2.png')
percentage, imgOut = get_green_percentage(img)
print(percentage)
cv2.imshow('Classified_image4.png', imgOut)
cv2.waitKey(0)
cv2.destroyAllWindows()
