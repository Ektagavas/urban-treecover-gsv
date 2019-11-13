import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

longitude = [34.1251, 34.1262, 34.1295, 34.1285, 34.1209]
longitude_min = 34.1205
longitude_max = 34.1375
longitude_diff = np.abs(longitude_max - longitude_min)
latitude = [-117.9590, -117.9552, -117.9281, -117.9281, -117.9281]
latitude_min = -117.9548
latitude_max = -117.9186
latitude_diff = np.abs(latitude_min - latitude_max)
img = cv2.imread('map.png')
x = img.shape[0] / latitude_diff
y = img.shape[1] / longitude_diff
for i in range(len(latitude)):
    x1 = np.int(np.abs(latitude[i] - latitude_min)*x)
    y1 = np.int(np.abs(longitude[i] - longitude_min)*y)
    val = np.ones((10, 10, 3))*20
    img[x1 - 5: x1 + 5, y1 - 5: y1 + 5] = val

# fig, ax = plt.subplots(figsize=(8, 7))
# ax.set_xlim(latitude_min, latitude_max)  # min and max latitude
# ax.set_ylim(longitude_min, longitude_max)  # min and max longitude

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# ruh_m = plt.imread('map.png')
# imgplot = plt.imshow(ruh_m)
# plt.show()