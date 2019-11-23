import cv2
import numpy as np


def variance_filter(img):
    # this function is used to detect intensity variance within a neighbourhood of 9X9.
    # cut off variance value used is 13, used in detecting stagnant water.
    # input -> Gray scaled image.
    # returns binary image, white indicates variance value less than 13.
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


def detect_water(img):
    # this function detects the amount of water present in a satellite image.
    # input -> RGB image of any size.
    # returns a binary image indicating the presence of water and percentage of water
    # white components indicates presence of water.
    # calls variance_filter() function.
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
    count = 0
    for i in range(mask_color.shape[0]):
        for j in range(mask_color.shape[1]):
            if (mask_color[i, j] != 0 and mask[i, j] != 0) or mask_light[i, j] != 0:
                mask_color[i, j] = 255
                count = count + 1
            else:
                mask_color[i, j] = 0
    percentage = count * 100 / (mask_color.shape[0] * mask_color.shape[1])
    return mask_color, percentage


def get_green_percentage(img):
    # this function detects presence of greenery in an satellite image
    # input -> RGB image
    # returns binary image indicating presence of greenery and percentage in an image.
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
    return imgOut, percentage


def detect(img):
    # this function detects the percentage of water, greenery and urban cover present in an image
    # input -> RGB image
    # returns binary image indicating presence of water, greenery, urban cover and their respective percentages in an
    # image
    water_mask, water_percentage = detect_water(img)
    green_mask, green_percentage = get_green_percentage(img)
    urban_percentage = 100 - water_percentage - green_percentage
    urban_mask = np.zeros(water_mask.shape)
    for i in range(water_mask.shape[0]):
        for j in range(water_mask.shape[1]):
            if water_mask[i, j] != 255 and green_mask[i, j] != 255:
                urban_mask[i, j] = 255
    print('Water Percentage: ',water_percentage)
    print('Greenery Percentage: ', green_percentage)
    print('Urban cover Percentage: ', urban_percentage)
    return water_mask, green_mask, urban_mask, water_percentage, green_percentage, urban_percentage


# Example
img = cv2.imread('water2.jpg')
water_mask, green_mask, urban_mask, water_percentage, green_percentage, urban_percentage = detect(img)
cv2.imshow('img', green_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
