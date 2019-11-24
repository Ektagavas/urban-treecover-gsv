import numpy as np
 
def detect_urban(img, green_mask, water_mask):
    urban_mask = np.zeros(water_mask.shape)
    for i in range(water_mask.shape[0]):
        for j in range(water_mask.shape[1]):
            if water_mask[i][j] != 255 and green_mask[i][j] != 255:
                urban_mask[i][j] = 255
    return urban_mask