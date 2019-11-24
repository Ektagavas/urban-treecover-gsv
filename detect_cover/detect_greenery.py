import numpy as np
import cv2


"""
    this function detects presence of greenery in an satellite image
    input -> RGB image
    returns binary image indicating presence of greenery in an image.
"""
def detect_greenery(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, (30, 25, 10), (90, 255, 255))
    return mask