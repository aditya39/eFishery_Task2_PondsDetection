from PIL import Image
import math, shutil, requests, os
import pandas as pd
import os
import cv2, numpy as np

class GoogleMapsLayers:
  ROADMAP = "v"
  TERRAIN = "p"
  ALTERED_ROADMAP = "r"
  SATELLITE = "s"
  TERRAIN_ONLY = "t"
  HYBRID = "y"


class GoogleMapDownloader:
    def __init__(self, lat, lng, zoom=12, layer=GoogleMapsLayers.ROADMAP):
        self._lat = lat
        self._lng = lng
        self._zoom = zoom
        self._layer = layer

    # Get X, Y coordinate from lat & long
    def getXY(self):
        tile_size = 256
        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom
        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size
        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))
        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    # Get Google Earth image
    def generateImage(self, **kwargs):
        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 8)
        tile_height = kwargs.get('tile_height', 8)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()
        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height
        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))
        for x in range(-tile_width//2, tile_width//2):
            for y in range(-tile_height//2, tile_height//2):
                url = f'https://mt0.google.com/vt?lyrs={self._layer}&x=' + str(start_x + x) + \
                       '&y=' + str(start_y + y) + '&z=' + str(self._zoom)
                current_tile = str(x) + '-' + str(y)
                response = requests.get(url, stream=True)
                with open(current_tile, 'wb') as out_file: shutil.copyfileobj(response.raw, out_file)
                im = Image.open(current_tile)
                map_img.paste(im, ((x+tile_width//2) * 256, (y+tile_height//2) * 256))
                os.remove(current_tile)
        print('Image size (pix): ', map_img.size)
        return map_img

def getSatelliteImage(latitudes, longitudes, zoomLevel = 18):
    try:
        gmd = GoogleMapDownloader(latitudes, longitudes, zoomLevel, GoogleMapsLayers.SATELLITE)
    except:
        img = None
        isError = True
        message = "Could not generate the image - try adjusting the zoom level and checking your coordinates"
        return img, isError, message

    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        img = gmd.generateImage()
        img = np.array(img) 
        print(img.shape)
        # Convert RGB to BGR
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    except IOError:
        img = None
        isError = True
        message = "Could not generate the image - try adjusting the zoom level and checking your coordinates"
    else:
        # Save the image to disk
        isError = False
        message = "The map has successfully been created"

    return img, isError, message
