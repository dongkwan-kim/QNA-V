import numpy as np
import cv2
import os

def handle_frame(video_path, frame_func):
    cap = cv2.VideoCapture(video_path)

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_func(frame)

        if not ret:
            break
    cap.release()

def save_img(img_path, img_name, image):
    """
    @param image: frame of video
    """
    cv2.imwirte(os.path.join(img_path, img_name), image)

if __name__ == "__main__":
    vtest_ysm = "video/test/test_ysm.mp4"
    vtest_kbs = "video/test/test_kbs.mp4"
