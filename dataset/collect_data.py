import urllib.parse
import urllib.request
from io import StringIO, BytesIO
from PIL import Image
from math import log, exp, tan, atan, pi, ceil

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0

DIR_PATH = './data/'

# Insert your api key for google maps here
API_KEY = ''


# Function to convert Lat,Long coordinates to pixels
def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) /180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py

# Function to convert pixels to Lat,Long coordinates
def pixelstolatlon(px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon


# a neighbourhood in Manhatten, NY:

upperleft =  '40.787322, -73.983632'
lowerright = '40.743758, -73.855146'


zoom = 19   # depending on how many images we want


ullat, ullon = map(float, upperleft.split(','))
lrlat, lrlon = map(float, lowerright.split(','))

# Set parameters
scale = 1
maxsize = 600
bottom = 10
maxsize -= bottom

# convert latlong coordinates to pixels
ulx, uly = latlontopixels(ullat, ullon, zoom)
lrx, lry = latlontopixels(lrlat, lrlon, zoom)

# calculate total pixel dimensions of final image
dx, dy = lrx - ulx, uly - lry

# calculate rows and columns
cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))
print(cols, rows)

# calculate pixel dimensions of each small image
width = int(ceil(dx/cols))
height = int(ceil(dy/rows))
heightplus = height + bottom

# Store image data
data = []
j = 0
for x in range(cols):
    for y in range(rows):
        dxn = width * (0.5 + x)
        dyn = height * (0.5 + y)
        latn, lonn = pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
        position = ','.join((str(round(latn,6)), str(round(lonn,6))))
        print(x, y, position)
        urlparams = urllib.parse.urlencode({'center': position,
                                      'zoom': str(zoom),
                                      'size': '%dx%d' % (width, heightplus),
                                      'maptype': 'satellite',
                                      'sensor': 'false',
                                      'scale': scale,
                                      'key':API_KEY})
        url = 'http://maps.google.com/maps/api/staticmap?' + urlparams
        f=urllib.request.urlopen(url)
        im=Image.open(BytesIO(f.read()))
        im.save(DIR_PATH+'i'+str(j)+'.png')
        data.append([round(latn,6), round(lonn,6), str(j)])
        j += 1

# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['lat', 'lon', 'patch_idx'])