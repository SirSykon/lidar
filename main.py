
import time
import lidar_processing_utils.lidar_processing_utils as lidar_processing_utils

example_bag_path = "./input/20211105_Aurora_ZirkerSee_9.bag"
topics = ['/cloud']

example_bag = lidar_processing_utils.read_bag(example_bag_path)

lidar_processing_utils.show_cloud_messages_from_rosbag(example_bag)

example_bag.close()
