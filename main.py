import numpy as np
import cv2
import pandas as pd
# from PIL import Image
from detect_cover.detect_cover import get_percent_cover
from visualization.visualize import show_map

DIR_PATH = './dataset/ny_data/'


def main () :
    j = 0
    n = 4
    data = []
    for i in range(n):
        path = DIR_PATH + 'g' + str(j) + '.png'
        img = cv2.imread(path)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # im_pil = Image.fromarray(img)

        
        img = cv2.resize(img, (300, 300), interpolation = cv2.INTER_AREA)
        # img = im_pil.resize((300, 300), Image.LANCZOS)

        # For reversing the operation:
        # img = np.asarray(img)

        green_pcent, water_pcent, urban_pcent = get_percent_cover(img)
        data.append([green_pcent, water_pcent, urban_pcent])
        print('Image', j)
        print('Greenery Percentage: ', green_pcent)
        print('Water Percentage: ',water_pcent)
        print('Urban cover Percentage: ', urban_pcent)
        print('-----------------------------------------')
        j += 1
    
    # Create the pandas DataFrame 
    df = pd.DataFrame(data, columns = ['greenery', 'water', 'urban'])

    # Read lat long from csv
    ny_data = pd.read_csv('./dataset/ny.csv')

    # Combine lat long and detected cover percent
    ny_data = pd.concat([df, ny_data[:4]], axis=1)

    # Print few rows of results
    print(ny_data.head())

    # Write results to file
    ny_data.to_csv('./dataset/results.csv', index=True)

    # Visualize data
    # show_map(ny_data)


if __name__ == "__main__":
    main()


