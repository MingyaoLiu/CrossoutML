import numpy as np
import time
import cv2
import d3dshot



from matplotlib import pyplot as plt

# mapArea = [174:920,587:1330]

screenWidth = 1920
screenHeight = 1080


in_battle_mini_map_width = 150
in_battle_mini_map_width_start = int(screenWidth - 210 - in_battle_mini_map_width / 2)
in_battle_mini_map_width_end = int(screenWidth - 210 + in_battle_mini_map_width / 2)
in_battle_mini_map_height = 150
in_battle_mini_map_height_start = int(screenHeight - 180 - in_battle_mini_map_height / 2)
in_battle_mini_map_height_end = int(screenHeight - 180 + in_battle_mini_map_height / 2)
in_battle_mini_map_trigger_pos_x = int(in_battle_mini_map_width_start + in_battle_mini_map_width / 2)
in_battle_mini_map_trigger_pos_y = int(in_battle_mini_map_height_start + in_battle_mini_map_height / 2)


OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects
tracker = OPENCV_OBJECT_TRACKERS["csrt"]()

initBB = None



d = d3dshot.create(capture_output='numpy')

print(d.displays)
if (len(d.displays) > 1):
    d.display = d.displays[1]
else:
    d.display = d.displays[0]

d.capture(target_fps=30, region=(0, 0, screenWidth, screenHeight))
time.sleep(1)


sensitivity = 25
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255, sensitivity, 255])

font = cv2.FONT_HERSHEY_COMPLEX


methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

method = eval('cv2.TM_CCOEFF')

garage_map = cv2.imread("./assets/garage_map_1.png",0)
img2 = garage_map.copy()

# loop over frames from the video stream
while True:


    np_frame = d.get_latest_frame()
    frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)

    if frame is None:
        break


############################

    srcmap = garage_map.copy()

    minimap_frame = frame[in_battle_mini_map_height_start:in_battle_mini_map_height_end, in_battle_mini_map_width_start:in_battle_mini_map_width_end]
    minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_RGB2GRAY)
    scale_percent = 80 # percent of original size

    width = int(minimap_frame.shape[1] * scale_percent / 100)
    height = int(minimap_frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    minimap_frame = cv2.resize(minimap_frame, dim, interpolation=cv2.INTER_AREA)
    w, h = minimap_frame.shape[::-1]

    cv2.imshow('minimap', minimap_frame)
    cv2.imshow("garagemap", garage_map)

    img = img2.copy()
    method = eval('cv2.TM_CCOEFF')

    res = cv2.matchTemplate(img,minimap_frame,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv2.rectangle(img, top_left, bottom_right, 255, 2)  ## Draw Template Rect on Src
    circle_center_x = int(top_left[0] + w / 2)
    circle_center_y = int(top_left[1] + h / 2)
    cv2.circle(img, (circle_center_x, circle_center_y), 2, (255, 0, 0) , 2) 

    cv2.imshow("img", img)


####################################
    # map_frame = frame[174:920, 587:1330]
    # cv2.imshow("map", map_frame)



###################################
	# # resize the frame (so we can process it faster) and grab the
	# # frame dimensions
    # # frame = cv2.resize(frame, width=500)
    # (H, W) = frame.shape[:2]

    
    # img2 = frame

    # hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    # mask = cv2.inRange(hsv, lower_white, upper_white)

    # _, threshold = cv2.threshold(mask, 110, 255, cv2.THRESH_BINARY) 
    # contours, _= cv2.findContours(threshold, cv2.RETR_TREE, 
    #                            cv2.CHAIN_APPROX_SIMPLE)
                               
    # # for cnt in contours : 

    # if len(contours) > 0:
    #     cnt = contours[0]

    #     print("Number of Contours found = " + str(len(contours)))

    #     approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
        
    #         # draws boundary of contours. 
    #     cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)  
        
    #         # Used to flatted the array containing 
    #         # the co-ordinates of the vertices. 
    #     n = approx.ravel()  
    #     i = 0

    #     x = n[i] 
    #     y = n[i + 1] 
        
    #                 # String containing the co-ordinates. 
    #     string = str(x) + " " + str(y)  
        
    #     if(i == 0): 
    #                     # text on topmost co-ordinate. 
    #         cv2.putText(img2, "Arrow tip", (x, y), 
    #                             font, 0.5, (255, 0, 0))  
    #     else: 
    #                     # text on remaining co-ordinates. 
    #         cv2.putText(img2, string, (x, y),  
    #                 font, 0.5, (0, 255, 0))  

    # # for j in n : 
    # #     if(i % 2 == 0): 
    # #         x = n[i] 
    # #         y = n[i + 1] 
    
    # #             # String containing the co-ordinates. 
    # #         string = str(x) + " " + str(y)  
    
    # #         if(i == 0): 
    # #                 # text on topmost co-ordinate. 
    # #             cv2.putText(img2, "Arrow tip", (x, y), 
    # #                                 font, 0.5, (255, 0, 0))  
    # #         else: 
    # #                 # text on remaining co-ordinates. 
    # #             cv2.putText(img2, string, (x, y),  
    # #                     font, 0.5, (0, 255, 0))  
    # #     i = i + 1



    # # Bitwise-AND mask and original image
    # cv2.imshow('mask', mask)
    



    # # check to see if we are currently tracking an object
    # if initBB is not None:
	# 	# grab the new bounding box coordinates of the object
    #     (success, box) = tracker.update(frame)
	# 	# check to see if the tracking was a success
    #     if success:
    #         (x, y, w, h) = [int(v) for v in box]
    #         cv2.rectangle(frame, (x, y), (x + w, y + h),
    #             (0, 255, 0), 2)
	# 	# initialize the set of information we'll be displaying on
	# 	# the frame
    #     info = [
    #         ("Tracker", "csrt"),
    #         ("Success", "Yes" if success else "No"),
    #     ]
	# 	# loop over the info tuples and draw them on our frame
    #     for (i, (k, v)) in enumerate(info):
    #         text = "{}: {}".format(k, v)
    #         cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



    # 	# show the output frame
    # cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
	# # if the 's' key is selected, we are going to "select" a bounding
	# # box to track
    if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
            showCrosshair=True)
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)

# if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        d.stop()
        break

# close all windows
cv2.destroyAllWindows()







			