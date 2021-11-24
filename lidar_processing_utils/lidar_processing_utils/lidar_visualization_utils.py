import open3d as o3d
import numpy as np
import rosbag
import time
from typing import Tuple, List, Generator
from .lidar_decoder import *
import matplotlib

def show_cloud(sparse_representation_of_points:np.ndarray, color_for_each_point:np.ndarray=None) -> None:
    """
    Procedure to show 3D vidualization of sparse representation of points.
    sparse_representation_of_points : np.ndarray -> Nx3 matrix with N (x,y,z) points.
    color_for_each_point : np.ndarray -> Nx3 matrix with N colors.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    if not color_for_each_point is None:
        pcd.colors = o3d.utility.Vector3dVector(color_for_each_point)
    o3d.visualization.draw_geometries([pcd])

def intensities2colors(intensities:np.ndarray, normalize:bool=True) -> np.ndarray:
    """
    Function to transform Nx1 intensities vector to Nx3 color vector.
    intensities:np.ndarray -> Nx1 intensities vector.
    """

    cmap = matplotlib.cm.get_cmap('cool')
    normalized_intensities = intensities/255.
    colors = cmap(normalized_intensities)[:,:3]

    if not normalize:
        colors = colors*255.

    return colors

def initialize_cloud_rendering(sparse_representation_of_points:np.ndarray, color_for_each_point:np.ndarray=None) -> Tuple[o3d.cpu.pybind.visualization.Visualizer,o3d.cpu.pybind.geometry.PointCloud]:
    """
    Procedure to initialize cloud rendering of sparse representation of points.
    sparse_representation_of_points : np.ndarray -> Nx3 matrix with N (x,y,z) points.
    color_for_each_point : np.ndarray -> Nx3 matrix with N colors to be used. If None, generic color degradation will be used (default None).
    """

    vis = o3d.visualization.Visualizer()
    vis.create_window()

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    if not color_for_each_point is None:
        pcd.colors = o3d.utility.Vector3dVector(color_for_each_point)
    vis.add_geometry(pcd)
    return vis, pcd

def update_cloud_rendering(vis:o3d.cpu.pybind.visualization.Visualizer, pcd:o3d.cpu.pybind.geometry.PointCloud, sparse_representation_of_points:np.ndarray, color_for_each_point:np.ndarray=None) -> Tuple[o3d.cpu.pybind.visualization.Visualizer,o3d.cpu.pybind.geometry.PointCloud]:
    """
    Procedure to initialize cloud rendering of sparse representation of points.
    vis:o3d.cpu.pybind.visualization.Visualizer -> visualization object.
    pcd:o3d.cpu.pybind.geometry.PointCloud -> pointcloud object related to the visualization.
    sparse_representation_of_points : np.ndarray -> Nx3 matrix with N (x,y,z) points.
    color_for_each_point : np.ndarray -> Nx3 matrix with N colors to be used. If None, generic color degradation will be used (default None).
    """
    pcd.points = o3d.utility.Vector3dVector(sparse_representation_of_points)
    if not color_for_each_point is None:
        pcd.colors = o3d.utility.Vector3dVector(color_for_each_point)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    return vis, pcd

def get_cloud_points_as_image(points_matrix:np.ndarray) -> np.ndarray:
    """
    Function to transform a cloud points numpy matrix as image.
    points_matrix:np.ndarray -> cloud points numpy matrix with shape Nx4 with each point as (x,y,z,intensity).
    """
    image_matrix = np.zeros(points_matrix.shape)
    image_matrix = np.linalg.norm(points_matrix, axis=2)
    image_matrix = np.concatenate([np.expand_dims(points_matrix[:,:,3], axis=-1), np.expand_dims(image_matrix,axis=-1), np.expand_dims(image_matrix,axis=-1)], axis=2)
    return image_matrix

def show_cloud_from_numpy_vector_generator(generator:Generator[np.ndarray, None, None]) -> None:
    """
    Process to get all cloud messages from a generator and visualize them in 3D real time.
    generator:Generator[np.ndarray, None, None] -> generator to get numpy vector with shape Nx5 with N points: (x,y,z,intensity,time)
    """

    print("Rendering point clouds from received generator.")
    vis = None
    dt = 0.1
    last_time = None
    for numpy_vector_of_points in generator:
        sparse_representation = numpy_vector_of_points[:,:3]
        intensities = numpy_vector_of_points[:,3]
        time_stamp = np.mean(numpy_vector_of_points[:,4])
        if last_time is None:
            last_time = time_stamp
        else:
            dt = time_stamp - last_time
            last_time = time_stamp
        print(f"dt={dt}")
        time.sleep(dt)
        if vis is None:
            vis, pcd = initialize_cloud_rendering(sparse_representation, intensities2colors(intensities))
        else:
            vis, pcd = update_cloud_rendering(vis,pcd,sparse_representation, intensities2colors(intensities))

    print("Redering finished.")

def show_cloud_from_ORCA_Uboat_USVInland_lidar_data_folder(orca_csv_folder_path:str) -> None:
    """
    Process to get all cloud messages from a folder with .csv files and visualize them in 3D real time.
    orca_csv_folder_path:str -> Path to folder with .csv files.
    """
    show_cloud_from_numpy_vector_generator(generator_numpy_vectors_from_ORCA_Uboat_USVInland_csv(orca_csv_folder_path, indexes=[0,1,2,6,7]))

def show_cloud_messages_from_rosbag(rosbag:rosbag.bag.Bag) -> None:
    """
    Process to get all cloud messages from rosbag file and visualize them in 3D real time.
    rosbag : rosbag.bag.Bag -> Ros bag as readed by rosbag package.
    """
    show_cloud_from_numpy_vector_generator(generator_numpy_vectors_from_rosbag(rosbag, ['/cloud']))
