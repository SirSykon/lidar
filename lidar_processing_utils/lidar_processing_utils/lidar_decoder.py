"""
Code to process LIDAR information.
Author: Jorge García-González
Last Update: 8/11/2021
"""

from bagpy import bagreader
import pandas as pd
import os
import numpy as np

def get_cloud_point_from_bag(bag_path:str) -> np.ndarray:
    """
    Function to read a .bag ros file.
    """
    pass

def generate_csv_from_bag(bag_path:str, topic:str, force:bool = True) -> str:
    """
    Function to generate a .csv file with the bag messages regarding a given topic.
    bag_path : str -> .bg file path.
    topic : str -> Topic from which to extract messages.
    force : bool -> Do we force de extraction? If true, extraction will be done, otherwise if the file already exist extraction shall be avoided. 
    """

    if force or not os.path.isfile(bag_path):
        bag = bagreader(bag_path)
        topic_csv_path = bag.message_by_topic(topic)
    else:
        topic_csv_path = f"{os.path.splitext(bag_path)}.csv"

    return topic_csv_path

def read_cloud_csv(cloud_csv_path:str, print_info:bool=False) -> pd.DataFrame:
    """
    Function to read a .csv file with cloud data messages and return it as pd.Dataframe.
    cloud_csv_path : str -> .csv file path.
    print_info : bool -> Do we print dataframe information?
    """

    df = pd.read_csv(cloud_csv_path)
    df['data'] = df['data'].apply(lambda d : np.frombuffer(d[2:-1].encode('latin-1').decode('unicode-escape').encode('latin-1'), np.uint8))

    if print_info:
        print("COLUMNS")
        print(df.columns)
        print(df.data)
        
def from_pointcloud2_format_to_numpy(pointcloud2_vector:np.ndarray, row_length:int) -> np.ndarray:
    """
    Function to transform a vector containing pointcloud2 array information to a 2D-matrix.
    pointcloud2_vector : list -> pointcloud2 vector.
    row_length : int -> Length to split pointcloud2_vector.
    """
    print(pointcloud2_vector)
    print(row_length)
    number_of_points = int(pointcloud2_vector.shape[0]/4)
    print(number_of_points)
    pointcloud2_matrix = pointcloud2_vector.reshape((number_of_points,4))
    print(pointcloud2_matrix.shape)
    max_x, max_y, max_z, max_intensity = list(np.max(pointcloud2_matrix, axis=0))
    print(max_x)
    print(max_y)
    print(max_z)
    print(max_intensity)
    print(pointcloud2_matrix)


