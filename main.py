import cv2
import numpy as np

alpha = 1.2 # [1.0;3.0]
beta = 20 # [0;100]
o_img = cv2.imread("original_images/photo_1.jpg")

new_image = cv2.convertScaleAbs(o_img, alpha=alpha, beta=beta)

cv2.imshow('Original Image', o_img)
cv2.imshow('New Image', new_image)
 
# Wait until user press some key
cv2.waitKey()

img_small = cv2.resize(o_img, ) #TODO: resCale keeping ratio
