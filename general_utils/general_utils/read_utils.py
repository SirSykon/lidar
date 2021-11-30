import cv2
from glob import glob

def generator_from_video(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()           # We try to read the next image
    while success:
        yield image
        success, image = vidcap.read()           # We try to read the next image
    
def generator_from_files_input_format(files_format):
    input_files = sorted(glob(files_format))
    for image_path in input_files:
        print(image_path)
        image = cv2.imread(image_path)
        yield image