"""
Code to process LIDAR information.
Author: Jorge García-González
Last Update: 30/11/2021
"""
import cv2


def computer_disparity(left_img_rgb, right_img_rgb):
    stereo = cv2.StereoBM_create()

    disp = stereo.compute(left_img_rgb, right_img_rgb)

    return disp


"""
def compute_disparity_pyramid(self):
        self.disparity = []
        stereo = cv2.StereoBM_create()
        # stereo = cv2.StereoSGBM_create(minDisparity=0,
        #                                numDisparities=64,
        #                                blockSize=11)

        # Compute disparity at full resolution and downsample
        disp = stereo.compute(self.im_left, self.im_right).astype(float) / 16.

        for pyrlevel in range(self.pyrlevels):
            if pyrlevel == 0:
                self.disparity = [disp]
            else:
                pyr_factor = 2**-pyrlevel
                # disp = cv2.pyrDown(disp) # Applies a large Gaussian blur
                # kernel!
                disp = disp[0::2, 0::2]
                self.disparity.append(disp * pyr_factor) 

"""