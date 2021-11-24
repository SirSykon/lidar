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
# read associated data
current_data = my_data.loc[my_data['unix timestamp'] == current_timestamp]
xyz_array = current_data.loc[:, ['x', 'y', 'z']].values
int_array = np.zeros((len(xyz_array),3)) # format needed for o3d color processing
int_array[:,0] = current_data.loc[:,'intensity'].values
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#implement visualization
vis = o3d.visualization.Visualizer()
vis.create_window()

# geometry is the point cloud used in your animaiton
geometry = o3d.geometry.PointCloud()

geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))

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
    current_data = my_data.loc[my_data['unix timestamp'] == current_timestamp]
    xyz_array = current_data.loc[:, ['x', 'y', 'z']].values
    int_array = np.zeros((len(xyz_array),3)) # format needed for o3d color processing
    int_array[:,0] = current_data.loc[:,'intensity'].values

    geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
    geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))
    #o3d.visualization.draw_geometries([geometry])
    
    vis.update_geometry(geometry)
    
    vis.run()
    vis.poll_events()
    vis.update_renderer()
    print(i)
    
# pcd = o3d.geometry.PointCloud()
# print('points to o3d')
# pcd.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
# pcd.colors = o3d.utility.Vector3dVector(int_array.astype(float))
# print('write to o3d')
# o3d.visualization.draw_geometries([pcd])

#https://stackoverflow.com/questions/62912397/open3d-visualizing-multiple-point-clouds-as-a-video-animation

print('Done')