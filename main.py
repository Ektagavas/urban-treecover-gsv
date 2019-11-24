# Import libraries
import flask
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
import pandas as pd
from detect_cover.detect_cover import get_percent_cover
from visualization.visualize import show_map
import plotly.express as px
from plotly.offline import iplot

app = flask.Flask(__name__)
CORS(app)
app_args = None

# Path to images directory
DIR_PATH = './dataset/ny_data/'


def main () :
    j = 0
    
    # Read lat long from csv
    ny_data = pd.read_csv('./dataset/ny.csv')

    # Number of small images or locations
    n = len(ny_data.index)
    data = []

    # For each small patch
    for i in range(n):
        path = DIR_PATH + 'ny_' + str(j) + '.jpg'
        img = cv2.imread(path)

        # img = cv2.resize(img, (300, 300), interpolation = cv2.INTER_AREA)

        # Find green, water and urban cover percent
        green_pcent, water_pcent, urban_pcent = get_percent_cover(img)
        data.append([green_pcent, water_pcent, urban_pcent])
        print('Image', j)
        print('Greenery Percentage: ', green_pcent)
        print('Water Percentage: ',water_pcent)
        print('Urban cover Percentage: ', urban_pcent)
        print('-----------------------------------------')
        j += 1
    
    # Create the DataFrame 
    df = pd.DataFrame(data, columns = ['greenery', 'water', 'urban'])


    # Combine lat long and detected cover percent for results
    ny_data = pd.concat([df, ny_data], axis=1)

    # Print first few rows of results
    print(ny_data.head())

    # Write results to file
    ny_data.to_csv('./dataset/results.csv', index=True)


    # Visualize data
    # show_map(ny_data, "greenery")
    # show_map(ny_data, "water")
    # show_map(ny_data, "urban")


if __name__ == "__main__":
    main()


