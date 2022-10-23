# Scale Invariant Feature Transform
import numpy as np
import cv2
from matplotlib import pyplot as plt

smallimage = r'C:\Users\User\Documents\University of Southampton\Year 4\GDP\GDP Software\imageStitching\Feature detection\1.jpg'
Fullimage = r'C:\Users\User\Documents\University of Southampton\Year 4\GDP\GDP Software\imageStitching\Feature detection\6.jpg'
Full = cv2.imread(Fullimage)  # trainImage
Full = cv2.resize(Full, (1000, 1000))
small = cv2.imread(smallimage)  # trainImage
# small = cv2.resize(smallimage, (1000, 1000))
y = 0
x = 0
h = 1000
w = 500
crop = Full[y:y + h, x:x + w]

# Start coordinate, here (5, 5)
# represents the top left corner of rectangle
start_point = (0, 0)

# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
end_point = (w, h)

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.rectangle() method
# Draw a rectangle with blue line borders of thickness of 2 px
Full = cv2.rectangle(Full, start_point, end_point, color, thickness)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
keypoints_1, descriptors_1 = sift.detectAndCompute(small, None)
keypoints_2, descriptors_2 = sift.detectAndCompute(Full, None)
print(len(keypoints_1), len(keypoints_2))

bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(descriptors_1, descriptors_2)
matches = sorted(matches, key=lambda x: x.distance)

img3 = cv2.drawMatches(crop,
                       keypoints_1,
                       Full,
                       keypoints_2,
                       matches[:50],
                       Full,
                       flags=2)
plt.imshow(img3), plt.show()
