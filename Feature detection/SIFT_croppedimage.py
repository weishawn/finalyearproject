import numpy as np
import cv2
from matplotlib import pyplot as plt

# path1 = r'C:\Users\User\Documents\University of Southampton\Year 4\GDP\GDP Software\imageStitching\Feature detection\1.jpg'
Fullimage = r'C:\Users\User\Documents\University of Southampton\Year 4\GDP\GDP Software\imageStitching\Feature detection\image_4.jpg'
Full = cv2.imread(Fullimage)  # trainImage
Full = cv2.resize(Full, (1000, 500))
y = 0
x = 0
h1 = 250
w1 = 550
crop1 = Full[y:y + h1, x:x + w1]

h2 = 250
w2 = 550
crop2 = Full[y:y + h1:, w1 - 50:1000]

cv2.imshow("cell1", crop1)
cv2.imshow("cell2", crop2)
cv2.waitKey(0)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
keypoints_1, descriptors_1 = sift.detectAndCompute(crop1, None)
keypoints_2, descriptors_2 = sift.detectAndCompute(crop2, None)
print(len(keypoints_1), len(keypoints_2))

bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(descriptors_1, descriptors_2)
matches = sorted(matches, key=lambda x: x.distance)

img3 = cv2.drawMatches(crop1,
                       keypoints_1,
                       crop2,
                       keypoints_2,
                       matches[:10],
                       crop2,
                       flags=2)
plt.imshow(img3), plt.show()
