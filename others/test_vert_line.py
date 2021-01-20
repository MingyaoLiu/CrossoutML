import numpy as np
import cv2
import d3dshot
import time

# gray = cv2.imread('./assets/line_test (3).png')
# edges = cv2.Canny(gray,50,150,apertureSize = 3)
# cv2.imwrite('edges-50-150.jpg', edges)
# # line = cv2.imread('edges-50-150.jpg')
# # cv2.imshow("lines", line)
# minLineLength=100
# lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=20)

# a,b,c = lines.shape
# for i in range(a):
#     cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
#     cv2.imwrite('houghlines5.jpg', gray)

screenWidth = 1920
screenHeight = 1080

d = d3dshot.create(capture_output='numpy')

print(d.displays)
if (len(d.displays) > 1):
    d.display = d.displays[1]
else:
    d.display = d.displays[0]

d.capture(target_fps=30, region=(0, 0, screenWidth, screenHeight))
time.sleep(1)



in_battle_front_view_width = 720
in_battle_front_view_width_start = int(screenWidth / 2 - in_battle_front_view_width / 2)
in_battle_front_view_width_end = int(screenWidth / 2 + in_battle_front_view_width / 2)
in_battle_front_view_height = 260
in_battle_front_view_height_start = int(screenHeight / 2.2 - in_battle_front_view_height / 2)
in_battle_front_view_height_end = int(screenHeight / 2.2 + in_battle_front_view_height / 2)
in_battle_front_view_trigger_pos_x = int(in_battle_front_view_width_start + in_battle_front_view_width / 2)
in_battle_front_view_trigger_pos_y = int(in_battle_front_view_height_start + in_battle_front_view_height / 2)

def nothing(*arg):
    pass
cv2.namedWindow('edge')
cv2.createTrackbar('thrs1', 'edge', 200, 500, nothing)
cv2.createTrackbar('thrs2', 'edge', 400, 500, nothing)

while True:
    np_frame = d.get_latest_frame()
    frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2GRAY)

    image = frame[ in_battle_front_view_height_start:in_battle_front_view_height_end,in_battle_front_view_width_start:in_battle_front_view_width_end ]


    thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
    thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
    edge = cv2.Canny(image, thrs1, thrs2, apertureSize=5)
    vis = image.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow('edge', vis)



# # Apply adaptive threshold
#     image_thr = cv2.adaptiveThreshold(image, 255, cv2.THRESH_BINARY_INV, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 51, 0)

# # Apply morphological opening with vertical line kernel
#     kernel = np.ones((image.shape[0], 1), dtype=np.uint8) * 255
#     image_mop = cv2.morphologyEx(image_thr, cv2.MORPH_OPEN, kernel)

# # Canny edge detection
#     image_canny = cv2.Canny(image_mop, 1, 5)

# # Get pixel values from the input image (force RGB/BGR on given input) within stripes
#     image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#     pixels = image_bgr[image_mop > 0, :]
#     print(pixels)

# # (Visualization) Output
#     cv2.imshow('image', image)
#     cv2.imshow('image_thr', image_thr)
#     cv2.imshow('image_mop', image_mop)
#     cv2.imshow('image_canny', image_canny)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         d.stop()
#         cv2.destroyAllWindows()
#         break
















# image = cv2.imread('./assets/line_test (3).png',0)

# image = image[ in_battle_front_view_height_start:in_battle_front_view_height_end,in_battle_front_view_width_start:in_battle_front_view_width_end ]

# # Apply adaptive threshold
# image_thr = cv2.adaptiveThreshold(image, 255, cv2.THRESH_BINARY_INV, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 51, 0)

# # Apply morphological opening with vertical line kernel
# kernel = np.ones((image.shape[0], 1), dtype=np.uint8) * 255
# image_mop = cv2.morphologyEx(image_thr, cv2.MORPH_OPEN, kernel)

# # Canny edge detection
# image_canny = cv2.Canny(image_mop, 1, 3)

# # Get pixel values from the input image (force RGB/BGR on given input) within stripes
# image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
# pixels = image_bgr[image_mop > 0, :]
# print(pixels)

# # (Visualization) Output
# cv2.imshow('image', image)
# cv2.imshow('image_thr', image_thr)
# cv2.imshow('image_mop', image_mop)
# cv2.imshow('image_canny', image_canny)
# cv2.waitKey(0)
# cv2.destroyAllWindows()