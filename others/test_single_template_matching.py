import cv2
import numpy as np
from matplotlib import pyplot as plt


img_garage_mask = cv2.imread("./assets/garage_map_1_mask_1.png", 0)


img = cv2.imread("./assets/garage_map_1.png",0)
img2 = img.copy()
template = cv2.imread("./assets/garage_minimap_1.png",0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

_, threshold = cv2.threshold(img_garage_mask, 127, 255, cv2.THRESH_BINARY) 
contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)



    cv2.imshow("img", img)
    cv2.waitKey(0)

    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)

    # cv2.rectangle(img,top_left, bottom_right, 255, 2)

    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)

    # plt.show()