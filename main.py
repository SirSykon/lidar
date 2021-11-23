
import time
import lidar_processing_utils.lidar_processing_utils as lidar_processing_utils
import numpy as np
import cv2

example_bag_path = "./input/20211105_Aurora_ZirkerSee_9.bag"
topics = ['/cloud']


example_bag = lidar_processing_utils.read_bag(example_bag_path)

#lidar_processing_utils.show_cloud_messages_from_rosbag(example_bag)
index = 0
for topic, msg, t in lidar_processing_utils.generator_msgs_from_rosbag(example_bag, topics):

    xyz_array = lidar_processing_utils.get_numpy_sparse_representation_from_pointcloud2_msg(msg)
    print(xyz_array.shape)
    print(xyz_array)
    print(xyz_array.dtype)

    np_array = lidar_processing_utils.get_numpy_matrix_from_pointcloud2_msg(msg)
    print(np_array.shape)
    print(np_array)
    print(np_array[0][1])
    print(np_array[0][2])
    print(np_array[0][3])
    print(np_array.dtype)
    image = lidar_processing_utils.get_cloud_points_as_image(np_array)
    image = np.flip(np.flip(image, axis=0), axis=1)
    cv2.imwrite(f"./output/images/test_{index}.jpg", image)
    index+=1
#lidar_processing_utils.show_cloud_messages_from_rosbag(example_bag)

example_bag.close()
