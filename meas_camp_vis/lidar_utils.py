'''lidar point cloud associated code'''

import numpy as np
import open3d as o3d
import pandas as pd
import colour
import matplotlib.cm
from pandas.core.accessor import register_index_accessor

#TODO: grid in the point cloud plot
#------------------------------------------------------------------------------
def _intensity2colourful_rgb(input_arr):
    '''Depricated.'''
    # very colourful point representation, maybe too time consuming
    arr = input_arr*255
    color_array = np.zeros((len(arr),3))
    for i in range(len(arr)):
        if arr[i]!=0:
            a = colour.RGB_color_picker(arr[i])
            b = a.rgb
            color_array[i,0] = b[0]
            color_array[i,1] = b[1]
            color_array[i,2] = b[2]
#------------------------------------------------------------------------------
def value2rgb(input_arr, normalizer):
    '''assign rgb values to the intensity values. All values are (re)normed by the RGB_color_picker function
    input:
        - input_arr(np.array): array containing intensity values
        - normalizer(int): value on which input_arr should be normalized
    returns:
        - color_array(np.array): array containing color values'''
    cmap = matplotlib.cm.get_cmap('cool')
    normalized_intensities = input_arr/normalizer
    color_array = cmap(normalized_intensities)[:,:3]
    return color_array
#------------------------------------------------------------------------------
def get_point_cloud(this_data, index):
    '''get point cloud includung xyz pont and intensity values for specific timestamp
    input:
        - this_data(pd.Dataframe): dataframe containing all point clouds for all timestamps
        - index (np.array): index for selecting point cloud (is faster then selecting by timestamp)
    returns:
        - this_xyz_array(np.array): xyz values for the current cloud
        - this_int_array(np.array): intensity values for the current cloud'''
    this_current_data = this_data.iloc[index] # select data by index
    this_xyz_array = this_current_data.loc[:, ['x', 'y', 'z']].values
    this_int_array = value2rgb(this_current_data.loc[:,'intensity'].values, normalizer=1)
    return this_xyz_array, this_int_array
#------------------------------------------------------------------------------
def read_file(my_csv_name):
    '''read in the csv file'''
    my_data = pd.read_csv(my_csv_name)
    return my_data
#------------------------------------------------------------------------------
# get first timestamp
def get_first_pointcloud(this_data, index):
    '''get point cloud by single index
    args:
        - this_data(pd.Dataframe): dataframe containing all point clouds for all timestamps
        - index(int): index to select data
    returns:
        - this_xyz_array(np.array): xyz values for the current cloud
        - this_int_array(np.array): intensity values for the current cloud
    '''
    current_timestamp = this_data.iloc[index,0]
    this_current_data = this_data.loc[this_data['unix timestamp'] == current_timestamp]
    
    this_xyz_array = this_current_data.loc[:, ['x', 'y', 'z']].values
    this_int_array = value2rgb(this_current_data.loc[:,'intensity'].values, normalizer=1)

    return this_xyz_array, this_int_array
#------------------------------------------------------------------------------
def implement_o3d_visualizer(xyz_array, int_array):
    '''implement visualization window for lidar point cloud
    args:
        - xyz_array(np.array): current point cloud
        - int_array(np.array): intensities
    returns:
        - vis(open3d.visualizer): visualizer
        - geometry(open3d.geometry): gemeotry
        - R (np.array): rotation matrix'''
    #implement visualization
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # geometry is the point cloud used in your animaiton
    geometry = o3d.geometry.PointCloud()
    geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
    geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))

    # rotate the image
    R = geometry.get_rotation_matrix_from_xyz((3*np.pi / 2, 0, np.pi / 2))
    geometry.rotate(R, center=(0,0,0))
    vis.add_geometry(geometry)

    #add voxel grid
    grid = o3d.geometry.VoxelGrid.create_from_point_cloud(geometry, 0.1)
    my_voxels = o3d.geometry.VoxelGrid.get_voxels(grid)
    # print('shape', np.array(my_voxels).shape)
    # apparently only contains voxels with intensity != 0. maybe assign (very low) intensity to those and use another cloud for grid generation
    return vis, geometry, R
#------------------------------------------------------------------------------
def visualize_point_cloud(vis, geometry, xyz_array, int_array, rotation_matrix):
    '''update and visualize lidar point cloud
    args:
        - vis(open3d.visualizer): visualizer
        - geometry(open3d.geometry): gemeotry
        - xyz_array(np.array): current point cloud
        - int_array(np.array): intensities
        - rotation_matrix (np.array): rotation matrix     
        '''
    geometry.points = o3d.utility.Vector3dVector(xyz_array.astype(float))
    geometry.colors = o3d.utility.Vector3dVector(int_array.astype(float))
    geometry.rotate(rotation_matrix, center=(0,0,0))

    vis.update_geometry(geometry)    
    vis.run()
    vis.poll_events()
    vis.update_renderer()