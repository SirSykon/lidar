'''function to project point cloud to different planes
sources: https://towardsdatascience.com/spherical-projection-for-point-clouds-56a2fc258e6c
'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import lidar_utils
import pandas as pd

column_scale = 924 # horizontal resolution of our device
row_scale = 24 # vertical resolution of our device

def initilize():
    '''depricated'''
    #fig, ax1 = plt.subplots()
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    return ax1, ax2

def set_axes_limits(axd, axi):
    '''set limits and titles of the projection figures
    args:
        - axd, axi (matplotlib.axes): axes for annonations'''
    axd.set_title('Distance', fontsize=15)
    axi.set_title('Intensity', fontsize=15)
    
    axd.set_xlim(-15,column_scale+15)
    axd.set_ylim(-row_scale-2,2)
    axd.set_xlabel('width')
    axd.set_ylabel('height')
    axd.grid()
    axd.axvline(x=column_scale/2)

    axi.set_xlim(-15,column_scale+15)
    axi.set_ylim(-row_scale-2,2)
    axi.set_xlabel('width')
    axi.set_ylabel('height')
    axi.grid()
    axi.axvline(x=column_scale/2)

def animate_plane(x, y, color_encoding, plot_label):
    '''depricated'''
    plt.cla()

    plt.xlim(-15,column_scale+15)
    plt.ylim(-24-2,2)
    plt.xlabel('width')
    plt.ylabel('height')
    plt.grid()

    plt.title(plot_label)
    #plt.legend()
    plt.scatter(x,y, color=color_encoding)
    # plt.draw()
    # plt.pause(0.01)

def project(xyz_array, csv_stoarge_path, file_name, timestamp, index):
    '''project the point cloud into the yz plane
    args:
        - xyz_array(np.array): lidar point cloud
        - csv_storage_path(String): path for csv file storage
        - file_name(String): file name of csv containing projections
        - timestamp(int): current timestamp
        - index(np.array): index for selecting current point cloud
    returns:
        - bx(np.array): projected x values
        - by(np.array): projected y values
        - normalized_distance(np.array): distance normalized to 1'''

    ax = xyz_array[:,0]
    ay = xyz_array[:,1]
    az = xyz_array[:,2]

    bx = np.zeros(len(ax)) # initialize projection arrays
    by = np.zeros(len(ax))
    bz = np.zeros(len(ax))

    hor_fov = np.deg2rad(120) # horizontal field of view
    vert_fov = np.deg2rad(15) # vertiacal field of view
    fov_down = np.deg2rad(1.5)
    fov_up = np.deg2rad(13.5)

    for i in np.arange(len(ax)):
        theta = math.atan2(ay[i], ax[i])
        distance = np.sqrt(ax[i]**2+ay[i]**2+az[i]**2)
        if distance != 0: # ensure not to dive by 0
            phi = np.arcsin(az[i]/distance) 
            yaw = - (theta/hor_fov) + 0.5
            pitch = (phi - fov_up) / (vert_fov)
            bx[i] = yaw * column_scale
            by[i] = pitch * row_scale
            bz[i] = distance

    output_array = np.array([bx, by, bz]).transpose() # generate array to store it in the cdv file
    # TODO: call csv writer
    # write_csv(storage_path_csv=csv_stoarge_path, file_name_csv=file_name, unix_timestamp=timestamp, my_array=output_array, index=index)

    # TODO: distinguish between loading projection from csv // calculate it hear
    input_data = pd.read_csv(csv_stoarge_path+'/'+file_name)
    # current_data = input_data.iloc[index]
    normalized_distance = lidar_utils.value2rgb(bz, normalizer=200)
    return bx, by, normalized_distance

def write_csv(storage_path_csv, file_name_csv, unix_timestamp, my_array, index):
    '''write projected point cloud to csv
    args:
        - storage_path_csv(String): path for csv file storage
        - file_name_csv(String): file name of csv containing projections
        - unix_timestamp(int): current timestamp
        - my_array(np.array): array for writing to csv
        - index(np.array): current index of lidar point cloud
    '''
    # TODO: create csv using the desired header
    if 0 in index:
        header = ['unix timestamp', 'x', 'y', 'distance']
        with open(storage_path_csv+'/'+file_name_csv, mode='w') as f:
            w = csv.writer(f)
            w.writerow(header)
    else: 
        data = pd.read_csv(storage_path_csv+'/'+file_name_csv)
        header = data.columns
    
    # generate dataframe to store the data there
    cloud_size = len(my_array)
    this_data = {header[0]: np.zeros(cloud_size), header[1]: np.zeros(cloud_size), header[2]: np.zeros(cloud_size), header[3]: np.zeros(cloud_size)}
    this_data_frame = pd.DataFrame(this_data)
    # store data in the generated dataframe
    this_data_frame[header[0]] = np.ones(cloud_size)*unix_timestamp
    this_data_frame[header[1]] = my_array[:,0]
    this_data_frame[header[2]] = my_array[:,1]
    this_data_frame[header[3]] = my_array[:,2]
    # append it to a csv file
    this_data_frame.to_csv(storage_path_csv+'/'+file_name_csv, header=False, mode='a', index=False)