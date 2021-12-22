'''gnss processing related code'''

from datetime import time
from urllib.request import urlopen, Request
from PIL import Image
import io
import cartopy.io.img_tiles as cimgt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
import pandas as pd

def _image_spoof(self, tile): # this function pretends not to be a Python script
    '''load open street map from web'''
    url = self._image_url(tile) # get the url of the street map API
    req = Request(url) # start request  
    req.add_header('User-agent','Anaconda 3') # add user agent to request
    fh = urlopen(req) 
    im_data = io.BytesIO(fh.read()) # get image
    fh.close() # close url
    img = Image.open(im_data) # open image with PIL
    img = img.convert(self.desired_tile_form) # set image format
    return img, self.tileextent(tile), 'lower' # reformat for cartopy

def _get_center_point(file_path):
    '''define center point for map
    args:
        - file_path(Sting): path were postion data is stored
    returns:
        - center point(tuple)'''
    data = load_position_data(file_path)

    max_lat = data['latitude_decimal_degree'].max()
    min_lat = data['latitude_decimal_degree'].min()
    max_lon = data['longitude_decimal_degree'].max()
    min_lon = data['longitude_decimal_degree'].min()

    mid_lat = np.deg2rad(max_lat) - ((np.deg2rad(max_lat)-np.deg2rad(min_lat))/2)
    mid_lon = np.deg2rad(max_lon) - ((np.deg2rad(max_lon)-np.deg2rad(min_lon))/2)

    return (np.rad2deg(mid_lat), np.rad2deg(mid_lon))

def get_openstreetmap(file_path, zoom):
    '''get figure with map in it
    args:
        - file_path(String): path were position data is stored
        - zoom (float): zoom out of center point
    returns:
        - fig: matplotlib figure
        - ax1: assiciated axes'''
    cimgt.OSM.get_image = _image_spoof # reformat web request for street map spoofing
    osm_img = cimgt.OSM() # spoofed, downloaded street map
    center_point = _get_center_point(file_path)
    extent = [center_point[1]-(zoom*2.0),center_point[1]+(zoom*2.0),center_point[0]-zoom,center_point[0]+zoom] # adjust to zoom

    fig = plt.figure(figsize=(12,9)) # open matplotlib figure
    ax1 = plt.axes(projection=osm_img.crs) # project using coordinate reference system (CRS) of street map
    ax1.set_extent(extent) # set extents

    scale = np.ceil(-np.sqrt(2)*np.log(np.divide(zoom,350.0))) # empirical solve for scale based on zoom
    scale = (scale<20) and scale or 19 # scale cannot be larger than 19
    ax1.add_image(osm_img, int(scale)) # add OSM with zoom specification

    return fig, ax1

def load_position_data(file_path):
    '''load gnss data from csv
    args: 
        - file_path(String): path were gnss data is stored
    returns:
        - import_data(pd.Dataframe): dataframe containing data'''
    import_data = pd.read_csv(file_path)
    return import_data

def animate_position(gnss_dataframe, timestamp, gnss_axis):
    '''deprecated'''
    current_second = round(timestamp/1e9)
    try:
        #plt.cla()
        #gnss_axis.clear()
        #get_openstreetmap(r'C:\Users\hoes_lu\Documents\Diplomarbeit\my_playground\data\processedBOW000DEU_R_20213141001_03H_02Z_MO.csv', 0.04)
        current_position = gnss_dataframe.loc[(round(gnss_dataframe['unix timestamp']/1e3) == current_second)]
        gnss_axis.plot(current_position['longitude_decimal_degree'], current_position['latitude_decimal_degree'],
            markersize=5,marker='o',linestyle='',color='#3b3b3b',transform=ccrs.PlateCarree())
        plt.draw() #TODO: glaub nicht dass wir das brauchen
        plt.pause(0.01)
        if current_position.empty == True:
            raise ValueError('position dataframe is empty')
    except ValueError as err:
        print(err.args)