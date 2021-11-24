# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 09:54:41 2021

@author: hoes_lu
"""

import numpy as np
import open3d as o3d
import csv
import pandas as pd
import copy
import colour
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def intensity2rgb(input_arr):
    arr = input_arr*255
    color_array = np.zeros((len(arr),3))

    for i in range(len(arr)):
        if arr[i]!=0:
            a = colour.RGB_color_picker(arr[i])
            b = a.rgb

            color_array[i,0] = b[0]
            color_array[i,1] = b[1]
            color_array[i,2] = b[2]

    return color_array
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def read_csv_data(this_data, this_current_timestamp):
    this_current_data = this_data.loc[this_data['unix timestamp'] == this_current_timestamp]
    this_xyz_array = this_current_data.loc[:, ['x', 'y', 'z']].values
    #this_int_array = 0*np.ones((len(this_xyz_array),3)) # format needed for o3d color processing
    #this_int_array[:,0] = this_current_data.loc[:,'intensity'].values

    this_int_array = intensity2rgb(this_current_data.loc[:,'intensity'].values)

    return this_xyz_array, this_int_array
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#read in the csv file
#my_csv_name = 'trial4.csv'
my_csv_name = 'C:/Users/hoes_lu/Documents/Diplomarbeit/lidar_repo/point_cloud_aurora_zirkerSee_20211105.csv'
my_data = pd.read_csv(my_csv_name)
i = 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# get first timestamp
current_timestamp = my_data.iloc[i,0]
xyz_array, int_array = read_csv_data(this_data=my_data, this_current_timestamp=current_timestamp)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#implement visualization
vis = o3d.visualization.Visualizer()
vis.create_window()

# geometry is the point cloud used in your animaiton
geometry = o3d.geometry.PointCloud()

geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))

#vis.add_geometry(geometry)

R = geometry.get_rotation_matrix_from_xyz((3*np.pi / 2, 0, np.pi / 2))
geometry.rotate(R, center=(0,0,0))

vis.add_geometry(geometry)

#mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
# mesh_r = copy.deepcopy(mesh).translate((2, 0, 0))
# mesh_r.rotate(mesh.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4)),
#               center=(0, 0, 0))
#o3d.visualization.draw_geometries([mesh, mesh_r])

#TODO: update POV

for i in np.arange(0,len(my_data), len(xyz_array)):
   
    # get first timestamp
    current_timestamp = my_data.iloc[i,0]
    print(current_timestamp)
    # read associated data
    xyz_array, int_array = read_csv_data(this_data=my_data, this_current_timestamp=current_timestamp)

    geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
    geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))
    geometry.rotate(R, center=(0,0,0))

    vis.update_geometry(geometry)
    geometry.translate((2,2,2), relative = False)
    
    vis.run()
    vis.poll_events()
    vis.update_renderer()
    print(i)

print('Done')