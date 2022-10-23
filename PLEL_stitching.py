import numpy as np
import cv2
import glob

EL = 'EL_24112021_151009'
PL = 'PL_24112021_151009'
def imageStitching():
    # image_paths = glob.glob('small-intersection/*.jpg')
    # EL_paths = glob.glob('EL_24112021_151009/*.jpg')
    EL_paths = glob.glob('xxx/*.jpeg')
    print(EL_paths)
    #EL_paths = glob.glob('xxx' + '.jpeg')
    PL_paths = glob.glob('PL_24112021_151009/*.jpg')
    print(PL_paths)

    PL_images = []
    EL_images = []

    for image in EL_paths:
        img = cv2.imread(image)
        EL_images.append(img)

    for image in PL_paths:
        img = cv2.imread(image)
        PL_images.append(img)

    #limitations
    # 1. Area of overlap must be big enough to detect feature points
    # 2. Ensure the captured image is perpendicular to ensure better warping

    imageStitcher = cv2.Stitcher_create()

    error_PL, stitched_img_PL = imageStitcher.stitch(PL_images)
    stitched_img_resized_PL = cv2.resize(stitched_img_PL, (1000, 1000))

    if not error_PL:
        print('foefkoefk')
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_PL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_PL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

    error_EL, stitched_img_EL = imageStitcher.stitch(EL_images)
    stitched_img_resized_EL = cv2.resize(stitched_img_EL, (1000, 1000))

    if not error_EL:
        cv2.imwrite("stitchedOutput_PL.png", stitched_img_resized_EL)
        cv2.imshow("Stitched Img_PL", stitched_img_resized_EL)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

imageStitching()
