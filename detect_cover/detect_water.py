import numpy as np
import cv2


"""
    this function is used to detect intensity variance within a neighbourhood of 9X9.
    cut off variance value used is 13, used in detecting stagnant water.
    input -> Gray scaled image.
    returns binary image, white indicates variance value less than 13.
"""
def variance_filter(img):
    mask = np.zeros(img.shape)
    kSize = 9
    l = kSize // 2
    for i in range(l, img.shape[0] - l):
        for j in range(l, img.shape[1] - l):
            ar = img[i - l: i + l + 1, j - l: j + l + 1]
            var = np.var(ar)
            if var <= 13:
                mask[i, j] = 255
            else:
                mask[i, j] = 0
    return mask



"""
    this function detects the amount of water present in a satellite image.
    input -> RGB image of any size.
    returns a binary image indicating the presence of water
    white components indicates presence of water.
    calls variance_filter() function.
"""
def detect_water(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.blur(imgGray, (3, 3))

    imgHSB = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([70, 60, 0])
    upper_blue = np.array([130, 200, 255])
    mask_color = cv2.inRange(imgHSB, lower_blue, upper_blue)

    mask = variance_filter(imgGray)
    
    lower_blue = np.array([75, 40, 173])
    upper_blue = np.array([100, 255, 255])
    mask_light = cv2.inRange(imgHSB, lower_blue, upper_blue)
    for i in range(mask_color.shape[0]):
        for j in range(mask_color.shape[1]):
            if (mask_color[i, j] != 0 and mask[i, j] != 0) or mask_light[i, j] != 0:
                mask_color[i, j] = 255
            else:
                mask_color[i, j] = 0
    return mask_color