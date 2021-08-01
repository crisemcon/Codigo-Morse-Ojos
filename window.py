import cv2
import numpy as np

image1 = cv2.imread('recordar-codigo-morse.png')
image2 = cv2.imread('recordar-codigo-morse.png')
# I just resized the image to a quarter of its original size
image1 = cv2.resize(image1, (0, 0), None, .25, .25)    #rem it out if u want smaller size
image2 = cv2.resize(image2, (0, 0), None, .25, .25)    #rem it out if u want smaller size

#grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Make the grey scale image have three channels
#grey_3_channel = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

numpy_horizontal = np.hstack((image1, image2))

numpy_horizontal_concat = np.concatenate((image1,image2), axis=1)

cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)
cv2.waitKey()