import pandas as pd
import os
import numpy as np
import sys

import lidar_processing_utils.lidar_processing_utils as lidar_processing_utils

example_bag_path = "./input/prueba2.bag"

csv_path = lidar_processing_utils.generate_csv_from_bag(example_bag_path, "/cloud")

lidar_processing_utils.read_cloud_csv(csv_path, print_info=True)


df = pd.read_csv(csv_path)
print(df.columns)
t = df.data[210]
t1 = t[2:10].encode('latin-1').decode('unicode-escape')
print("t1")
print(type(t1))
print(t1)
print(t1.encode('latin-1'))
print(np.frombuffer(t1.encode("latin-1"), np.uint8))

df['data'] = df['data'].apply(lambda d : np.frombuffer(d[2:-1].encode('latin-1').decode('unicode-escape').encode('latin-1'), np.uint8))
print(len(df['data'][200]))

lidar_processing_utils.from_pointcloud2_format_to_numpy(df['data'][200], df['row_step'][200])