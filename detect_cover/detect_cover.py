import numpy as np
from detect_cover.detect_greenery import detect_greenery
from detect_cover.detect_water import detect_water
from detect_cover.detect_urban import detect_urban


def get_percent(mask):
    """
    Function to get percent of foreground pixels of given mask

    Arguments:
    mask: binary image

    Returns:
    value in percentage
    """
    fg = 0
    total = mask.shape[0] * mask.shape[1]
    mask = mask / 255
    fg = np.sum(mask)
    return round(((fg / total) * 100), 3)


def get_percent_cover(img):
    """
    Detect greenery, water and urban cover in an image

    Arguments:
    img: RGB image

    Returns:
    green_pcent : Percentage of green cover
    water_pcent: Percentage of water cover
    urban_pcent: Percentage of urban cover
    """
    green_mask = detect_greenery(img)
    water_mask = detect_water(img)
    urban_mask = detect_urban(img, green_mask, water_mask)

    green_pcent = get_percent(green_mask)
    water_pcent = get_percent(water_mask)
    urban_pcent = get_percent(urban_mask)

    if water_pcent > 75 and green_pcent < 25 and urban_pcent > 0:
        urban_pcent = 0

    return green_pcent, water_pcent, urban_pcent
