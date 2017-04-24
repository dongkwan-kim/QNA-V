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

    def set_info(self, video_1, idx_1, video_2, idx_2):
        self.idx_1 = idx_1
        self.idx_2 = idx_2
        self.video_1 = video_1
        self.video_2 = video_2

    def p(self, s):
        s = s.split("/")
        s = "-".join(s[-2:])
        s = s.replace("/", "-")
        s = s.replace(".mp4", "")
        return s

    def get_title(self):
        return "_".join([
            self.p(self.video_1),
            self.p(self.video_2),
        ])


def save_img(img_path, img_name, image):
    """
    @param image: frame of video
    """
    cv2.imwrite(os.path.join(img_path, img_name), image)

def save_cmp_log(cmp_iter):
    i = 0
    for c in cmp_iter:
        if i == 0:
            o = open("result/"+c.get_title() + ".txt", "w")
        o.write("\t".join([
            str(c.idx_1),
            str(c.idx_2),
            str(c.score()),
        ]) + "\n")
        i += 1

    o.close()


def compare_video(video_1, video_2, cmp_func):
    idx_1 = -1

    cap_1 = cv2.VideoCapture(video_1)
    while(cap_1.isOpened()):
        idx_1 += 1
        idx_2 = 0
        ret_1, frame_1 = cap_1.read()

        if ret_1:
            cap_2 = cv2.VideoCapture(video_2)
            while(cap_2.isOpened()):
                idx_2 += 1
                ret_2, frame_2 = cap_2.read()

                if ret_2:
                    if (idx_1 % 30) == 0 and (idx_2 % 30) == 0:
                        knn_fm = cmp_func(frame_1, frame_2)
                        knn_fm.set_info(video_1, idx_1, video_2, idx_2)
                        yield(knn_fm)
                else:
                    break
        else:
            break

    cap_1.release()
    cap_2.release()

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


def camp(c, cv):
    return "video/camp/" + c + "/" + cv

def news(n, nv):
    return "video/news/" + n + "/" + nv


if __name__ == "__main__":
    camp_list = ["ssj"]
    news_list = ["mbc", "sbs", "kbs"]

    err = open("error.txt", "w")
    acc = open("acc.txt", "w")

    for c in camp_list:
        for cv in os.listdir("video/camp/" + c):
            for n in news_list:
                for nv in os.listdir("video/news/" + n):
                    try:
                        acc.write("\t".join([
                            cv,
                            nv,
                        ]) + "\n")
                        cmp_iter = compare_video(camp(c, cv), news(n, nv), compare_fm)
                        save_cmp_log(cmp_iter)
                    except:
                        err.write("\t".join([
                            cv,
                            nv,
                        ]) + "\n")
    err.close()
    acc.close()
