import numpy as np
import cv2
from PIL import ImageGrab as ig
import cur
from utils import POINT_GOOD_MATCH_THRES, IMG_FOUND_THRES, debugPrint


def flannMatch(kp1, des1, kp2, des2):
    """
    @param kp1: keypoints of image1.
    @param des1: descriptors of the kp1.

    @param kp2: keypoints of image2.
    @param des2: descriptors of the kp2.

    @return: keypoints and their descriptors.
    
    @ref: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html
    """

    good_kps1 = []
    good_kps2 = []

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)


    for i, (m, n) in enumerate(matches):
        if m.distance < POINT_GOOD_MATCH_THRES * n.distance:
            good_kps1.append([kp1[m.queryIdx].pt[0], kp1[m.queryIdx].pt[1]])
            good_kps2.append([kp2[m.trainIdx].pt[0], kp2[m.trainIdx].pt[1]])

    return good_kps1, good_kps2


def getImgLoc(imgName, numPts=4000):
    targetImg = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    screenImg = cv2.cvtColor(np.asarray(ig.grab()), cv2.COLOR_RGB2GRAY)

    sift = cv2.SIFT_create(nfeatures=numPts)
    kp1, des1 = sift.detectAndCompute(targetImg, None)
    kp2, des2 = sift.detectAndCompute(screenImg, None)
    _, good_kp2 = flannMatch(kp1, des1, kp2, des2)

    if len(good_kp2) <= IMG_FOUND_THRES:
        debugPrint("getImgLoc:", imgName, "not found. #pts =", len(good_kp2))
        return None 
    
    sumX, sumY = 0, 0
    for i in range(len(good_kp2)):
        sumX += good_kp2[i][0]
        sumY += good_kp2[i][1]

    debugPrint("getImgLoc:", imgName, "found. #pts =", len(good_kp2))
    return int(sumX / len(good_kp2)), int(sumY / len(good_kp2))

def moveToImg(imgName):
    loc = getImgLoc(imgName)
    if loc is None:
        return False
    cur.moveCursorPos(loc[0], loc[1])
    return True
