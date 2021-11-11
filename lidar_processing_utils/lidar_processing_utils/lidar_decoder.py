"""
Code to process LIDAR information.
Author: Jorge García-González
Last Update: 11/11/2021
"""

import time
from bagpy import bagreader
import pandas as pd
import os
import numpy as np
import open3d as o3d
import rosbag
import rospy
import ros_numpy
from typing import Tuple, List

def get_cloud_point_from_bag(bag_path:str) -> np.ndarray:
    """
    DEPRECATED
    Function to read a .bag ros file.
    """
    pass

def generate_csv_from_bag(bag_path:str, topic:str, force:bool = True) -> str:
    """
    DEPRECATED
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
    DEPRECATED
    Function to read a .csv file with cloud data messages and return it as pd.Dataframe.
    cloud_csv_path : str -> .csv file path.
    print_info : bool -> Do we print dataframe information?
    """

    print(f"Reading .csv from {os.path.abspath(cloud_csv_path)}")
    df = pd.read_csv(cloud_csv_path)
    df['data'] = df['data'].apply(lambda d : np.frombuffer(d[2:-1].encode('latin-1').decode('unicode-escape').encode('latin-1'), np.float32))

    if print_info:
        print("COLUMNS")
        print(df.columns)
        print(df.data)

    return df

def get_points_from_lidar_msg(msg:pd.Series) -> np.ndarray:
    """
    DEPRECATED
    Function to get a Nx3 matrix with the N points positions in msg.
    msg : pd.Series -> Lidar message.
    """

    pointcloud2_vector = msg['data']
    number_of_points = int(pointcloud2_vector.shape[0]/4)
    pointcloud2_matrix = pointcloud2_vector.reshape((number_of_points,4))

    return pointcloud2_matrix[:,:3]

def from_lidar_msg_to_numpy(msg:pd.Series) -> np.ndarray:
    """
    DEPRECATED
    Function to transform a msg containing pointcloud2 array information to a 3D-matrix.
    msg : pd.Series -> Lidar message.
    """
    print(msg)
    pointcloud2_vector = msg['data']
    row_length = msg['row_step']
    print(pointcloud2_vector)
    number_of_points = int(pointcloud2_vector.shape[0]/4)
    print(f"Number of points: {number_of_points}")
    pointcloud2_matrix = pointcloud2_vector.reshape((number_of_points,4))
    print(pointcloud2_matrix.shape)
    max_x, max_y, max_z, max_intensity = list(np.max(pointcloud2_matrix, axis=0))
    print(max_x)
    print(max_y)
    print(max_z)
    print(max_intensity)
    points_matrix = np.zeros(shape=(max_x+1, max_y+1, max_z+1), dtype=np.uint8)
    for point_cloud2 in pointcloud2_matrix:
        points_matrix[point_cloud2[0], point_cloud2[1], point_cloud2[2]] = point_cloud2[3]
    print(points_matrix)

    return points_matrix

def project_to_2D(points_matrix:np.ndarray, axis:int) -> np.ndarray:
    """
    Funtion to get a 2D projection from 3D matrix.
    """
    assert len(points_matrix) > axis

    projected_points_matrix = np.sum(points_matrix, axis=axis)
    normalized_projected_points_matrix = projected_points_matrix

    return normalized_projected_points_matrix/np.max(normalized_projected_points_matrix)

def generator_msgs_from_rosbag(bag:rosbag.bag.Bag, topics:List[str]) -> Tuple[str, object, rospy.rostime.Time]:
    """
    Function to return ros messages contained in a ros .bag file in bag_path.
    bag:rosbag.bag.Bag -> The bag to read messages from.
    topics:list(str) -> Topics to get messages from the bag.
    """
    for topic, msg, t in bag.read_messages(topics=topics):
        yield topic, msg, t
 

def read_bag(bag_path:str, print_bag_info:bool=False) -> rosbag.bag.Bag:
    """
    Function to get a rosbag bag from ros .bag file.
    bag_path:str -> Path to ros bag file.
    print_bag_info:bool -> Do we print bag info? Default: False.
    """
    bag = rosbag.Bag(bag_path)

    if print:
        print(f"Bag topics: {bag.get_type_and_topic_info()[1].keys()}")

    return bag


def close_bag(bag:rosbag.bag.Bag):
    bag.close()

def get_numpy_sparse_representation_from_pointcloud2_msg(pointcloud2_msg:object):
    """
    Funtion to get a numpy matrix with the sparse representation of points contained in a point cloud 2 ros message.
    pointcloud2_msg:object -> The point cloud 2 ros message to get the points from.
    """
    sparse_representation_of_points = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(pointcloud2_msg, remove_nans=True) 
    return sparse_representation_of_points

def show_cloud(sparse_representation_of_points:np.ndarray) -> None:
    """
    Procedure to show 3D vidualization of sparse representation of points.
    sparse_representation_of_points : np.ndarray -> Nx3 matrix with N (x,y,z) points.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    o3d.visualization.draw_geometries([pcd])

def initialize_cloud_rendering(sparse_representation_of_points:np.ndarray) -> o3d.cpu.pybind.visualization.Visualizer:
    """
    TODO: Description.
    """

    vis = o3d.visualization.Visualizer()
    print(type(vis))
    vis.create_window()

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    vis.add_geometry(pcd)
    return vis, pcd

def update_cloud_rendering(vis:o3d.cpu.pybind.visualization.Visualizer, pcd, sparse_representation_of_points:np.ndarray) -> o3d.cpu.pybind.visualization.Visualizer:
    """
    TODO: Description.
    """

    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    return vis, pcd

def show_cloud_messages_from_rosbag(rosbag:rosbag.bag.Bag) -> None:
    """
    Process to get all cloud messages from a bag and visualize them in 3D real time.
    rosbag : rosbag.bag.Bag -> Ros bag as readed by rosbag package.
    """

    print("Rendering point clouds from received bag.")
    vis = None
    dt = 0.1
    last_time = None
    for topic, msg, t in generator_msgs_from_rosbag(rosbag, ['/cloud']):
        sparse_representation = get_numpy_sparse_representation_from_pointcloud2_msg(msg)
        if last_time is None:
            last_time = t.to_time()
        else:
            aux_t = t.to_time()
            dt = aux_t - last_time
            last_time = aux_t
        time.sleep(dt)
        if vis is None:
            vis, pcd = initialize_cloud_rendering(sparse_representation)
        else:
            vis, pcd = update_cloud_rendering(vis,pcd,sparse_representation)

    print("Redering finished.")



