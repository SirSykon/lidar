'''main script: visualize lidar point cloud and its projections with associated gnss position as animation

- lidar point cloud is loaded from a csv file (I can't load it directly from .bag files)
    - the pregenerated csv file contains one cloud per second (10 clouds per second were recorded)
- point cloud is projected into the yz plane while the visualization is performed.
    - TODO: generate csv file to store projections and load them
- gnss data is loaded from a csv file with adapted timestamp
    - TODO: add second antenna to define attitude
    - TODO: zoom in the map and move it together with target

updating figures in loop: https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
'''
from numpy.lib.function_base import select
import lidar_utils
import gnss_utils
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import cartopy.crs as ccrs
import plane_projector_func as plane_projector
import time

# define name for file containing projected poinr cloud
projector_csv_storage_path = r'C:\Users\hoes_lu\Documents\Diplomarbeit\my_playground\data'
projector_csv_file_name = '2D_projected_cloud_aurora20211105_complete'#'projected_cloud.csv'

# get lidar point cloud including intensities
lidar_csv_name = 'C:/Users/hoes_lu/Documents/Diplomarbeit/my_playground/data/point_cloud_aurora_zirkerSee_20211105.csv'
lidar_dataframe = lidar_utils.read_file(lidar_csv_name)
#lidar_first_timestamp = lidar_utils.get_first_timestamp(lidar_dataframe, index=0)
lidar_xyz_array, lidar_int_array = lidar_utils.get_first_pointcloud(this_data=lidar_dataframe, index=0)

lidar_visualizer, lidar_geometry, lidar_rotation_matrix = lidar_utils.implement_o3d_visualizer(lidar_xyz_array,
                                                                                                lidar_int_array)

plt.ion() # turn interactive mode on
lidar_first_timestamp = lidar_dataframe.iloc[0,0]

# get gnss data
gnss_file_path = r'C:\Users\hoes_lu\Documents\Diplomarbeit\my_playground\data'
gnss_file_name = 'processedBOW000DEU_R_20213141001_03H_02Z_MO.csv'
gnss_dataframe = gnss_utils.load_position_data(gnss_file_path+'/'+gnss_file_name)
gnss_dataframe = gnss_dataframe.loc[(round(gnss_dataframe['unix timestamp']/1e3) >= round(lidar_first_timestamp/1e9) )] # align first timestamp
g = 0 # initialize index for selecting gnss position
# initialize gnss visualization 
zoom = 0.05 # for zooming out of center point
figg, axg = gnss_utils.get_openstreetmap(file_path=gnss_file_path+'/'+gnss_file_name, zoom=zoom) # get figure with map 
   
# initialize figures for projections
figp = plt.figure(figsize=(10,8))
axd = figp.add_subplot(211)
axi = figp.add_subplot(212)
plane_projector.set_axes_limits(axd, axi)

for i in np.arange(0,len(lidar_dataframe), len(lidar_xyz_array)):
    current_timestamp = lidar_dataframe.iloc[i,0]
    current_second = round(current_timestamp/1e9) # round timestamp to full second
    print('timestamp', current_second)
    # read associated lidar data
    selecter_array = np.arange(i,i+len(lidar_xyz_array)) # array for selecting point cloud by index
    xyz_array, int_array = lidar_utils.get_point_cloud(this_data=lidar_dataframe, index=selecter_array) # lidar point cloud with intesities
    lidar_utils.visualize_point_cloud(vis=lidar_visualizer, geometry=lidar_geometry, xyz_array=xyz_array, int_array=int_array,
                                        rotation_matrix=lidar_rotation_matrix) # visualize the point cloud
    
    # project lidar point cloud
    # TODO: store in csv to process it faster; select then by index
    x_proj, y_proj, normalized_distance = plane_projector.project(xyz_array, projector_csv_storage_path, projector_csv_file_name, current_timestamp,index=selecter_array)
    # visualize projections
    axd.clear() # clear old values
    axi.clear()
    plane_projector.set_axes_limits(axd, axi) # label axes and subplots
    axd.scatter(x_proj,y_proj,color=normalized_distance) 
    axi.scatter(x_proj,y_proj,color=int_array)
    figp.canvas.draw()
    
    # update and display gnss data
    curr_lat = gnss_dataframe.iloc[g][1]
    curr_lon = gnss_dataframe.iloc[g][2]
    axg.plot(curr_lon, curr_lat, markersize=5,marker='o',linestyle='',color='#3b3b3b',transform=ccrs.PlateCarree())
    figg.canvas.draw()
    g += 1 # update index for data selection
 
    time.sleep(0.1) # necessary to display all updated figures