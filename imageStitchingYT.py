import numpy as np
import cv2
import glob

# load images
# image_paths = glob.glob('images/*.jpg')
#image_paths = glob.glob('one_cell/*.jpg')
# image_paths = glob.glob('colourful_image/*.jpg')
#image_paths = glob.glob('Brute-Force/*.jpg')
def imageStitching():
    image_paths = glob.glob('Final EL images/*.jpg')
    images = []
    print(image_paths)
    for image in image_paths:
        img = cv2.imread(image)
        img = cv2.resize(img, (200, 200))
    
        images.append(img)

    #limitations
    # 1. Area of overlap must be big enough to detect feature points
    # 2. Ensure the captured image is perpendicular to ensure better warping

    imageStitcher = cv2.Stitcher_create()

    error, stitched_img = imageStitcher.stitch(images)
    # stitched_img_resized = cv2.resize(stitched_img, (1000, 1000))

    if not error:
        cv2.imwrite("stitchedOutput.png", stitched_img)
        cv2.imshow("Stitched Img", stitched_img)
        cv2.waitKey(0)
    else:
        print("Images could not be stitched!")
        print("Likely not enough keypoints being detected!")

imageStitching()