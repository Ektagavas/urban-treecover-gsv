import cv2 as cv
import numpy as np
import pandas as pd


### resizing image to 300*300
def resize(img, num):
    h, w, c = img.shape
    newX, newY = 300, 300
    img_new = cv.resize(img, (int(newX), int(newY)))
    # cv.imshow("Resize image", img_new)
    # cv.waitKey(0)
    cv.imwrite("ny_%d.jpg" % num, img_new)


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
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgGray = cv.blur(imgGray, (3, 3))
    imgHSB = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_blue = np.array([70, 60, 0])
    upper_blue = np.array([130, 200, 255])
    mask_color = cv.inRange(imgHSB, lower_blue, upper_blue)
    mask = variance_filter(imgGray)
    lower_blue = np.array([75, 40, 173])
    upper_blue = np.array([100, 255, 255])
    mask_light = cv.inRange(imgHSB, lower_blue, upper_blue)
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
    imgOut = np.zeros((img.shape[0], img.shape[1]))
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
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


#### Resizing Images
for i in range(1909):
    img = cv.imread('g%d.png' % i)
    resize(img)


# Output represents percentage array, 1 col greenery percentage, 2 col water percentage and 3 column urban percentage
output = np.zeros((1909, 3))
for i in range(1910):
    img = cv.imread('ny_%d.jpg' % i)
    g_percent, img_out = get_green_percentage(img)
    mask_colour, w_percent = detect_water(img)
    output[i, 0] = g_percent
    output[i, 1] = w_percent
    output[i, 2] = 100 - g_percent - w_percent

df = pd.DataFrame(output)
df.to_excel(excel_writer="DIP_percentage.xlsx")
