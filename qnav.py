import numpy as np
import cv2
import os

class KNN_FM:
    def __init__(self, f1, kp1, f2, kp2, good):
        self.f1 = f1
        self.f2 = f2
        self.kp1 = kp1
        self.kp2 = kp2
        self.good = good

    def score(self):
        return len(self.good)

    def save_img(self, img_path, img_name):
        i = cv2.drawMatchesKnn(self.f1, self.kp1, \
                self.f2, self.kp2, self.good, None, flags=2)
        save_img(img_path, img_name +"_"+ str(self.score()) + ".png", i)


def save_img(img_path, img_name, image):
    """
    @param image: frame of video
    """
    cv2.imwrite(os.path.join(img_path, img_name), image)

def compare_video(video_1, video_2, cmp_func):
    o = open("output.txt", "w")
    idx_1, idx_2 = 0, 0

    cap_1 = cv2.VideoCapture(video_1)
    while(cap_1.isOpened()):
        idx_1 += 1
        ret_1, frame_1 = cap_1.read()

        if ret_1:
            cap_2 = cv2.VideoCapture(video_2)
            while(cap_2.isOpened()):
                idx_2 += 1
                ret_2, frame_2 = cap_2.read()

                if ret_2:
                    knn_fm = cmp_func(frame_1, frame_2)
                    o.write(str(idx_1) +"\t" + str(idx_2) +"\t"+ str(knn_fm.score())+"\n")
                    if knn_fm.score() > 100:
                        knn_fm.save_img("result", "knn_" + str(idx_1)+"_"+str(idx_2))
                else:
                    break
            break
        else:
            break

    cap_1.release()
    cap_2.release()
    o.close()

def compare_fm(frame_1, frame_2):
    sift = sift=cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(frame_1, None)
    kp2, des2 = sift.detectAndCompute(frame_2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    return KNN_FM(frame_1, kp1, frame_2, kp2, good)

if __name__ == "__main__":
    vtest_ysm = "video/test/test_ysm.mp4"
    vtest_kbs = "video/test/test_kbs.mp4"
    compare_video(vtest_ysm, vtest_kbs, compare_fm)
