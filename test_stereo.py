import os
import cv2
from glob import glob
import matplotlib.pyplot as plt

import stereo_camera_processing_utils.stereo_camera_processing_utils.stereo_camera_utils as stereo_camera_utils
import general_utils.general_utils.read_utils as read_utils

left_stereo_images_folder = "./input/ORCA/N02_4_Sequence_155_370/Image/PIC_Left/"
right_stereo_images_folder = "./input/ORCA/N02_4_Sequence_155_370/Image/PIC_Right/"

left_images_format = os.path.join(left_stereo_images_folder, "*.jpg")
right_images_format = os.path.join(right_stereo_images_folder, "*.jpg")

left_gen = read_utils.generator_from_files_input_format(left_images_format)
right_gen = read_utils.generator_from_files_input_format(right_images_format)

for index, (left_img, right_img) in enumerate(zip(left_gen,right_gen)):
    left_img_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    right_img_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    disparity = stereo_camera_utils.computer_disparity(left_img_gray, right_img_gray)
    plt.imshow(disparity, 'gray')
    plt.show()