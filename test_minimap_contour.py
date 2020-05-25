import numpy as np
import cv2




img = cv2.imread("./assets/arrow_contour.png",0)
ret, thresh = cv2.threshold(img, 200, 255, 0)

# cv2.imshow("TEST", thresh)


contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)





print(len(contours))
cnt = contours[0]
# cv2.drawContours(img, [cnt], 0, (0,255,0), 3)

# ellipse = cv2.fitEllipse( cnt )
# axes = ellipse[1]
# minor, major = axes
# print(ellipse)
# print(axes)
# cv2.ellipse(img,ellipse,(0,0,255),2)

# rect = cv2.minAreaRect(cnt)
# print(rect)
# box = cv2.boxPoints(rect)
# box = np.int0(box)
# cv2.drawContours(img,[box],0,(0,0,255),2)


for i in contours:
    size = cv2.contourArea(i)
    rect = cv2.minAreaRect(i)
    if size <10000:
        gray = np.float32(img)
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.fillPoly(mask, [i], (255,255,255))
        dst = cv2.cornerHarris(mask,5,3,0.04)
        ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

        print(len(corners))

        if rect[2] == 0 and len(corners) == 5:
            x,y,w,h = cv2.boundingRect(i)
            if w == h or w == h +3: #Just for the sake of example
                print('Square corners: ')
                for i in range(1, len(corners)):
                    print(corners[i])
            else:
                print('Rectangle corners: ')
                for i in range(1, len(corners)):
                    print(corners[i])
        if len(corners) == 5 and rect[2] != 0:
            print('Rombus corners: ')
            for i in range(1, len(corners)):
                print(corners[i])
        if len(corners) == 4:
            print('Triangle corners: ')
            for i in range(1, len(corners)):
                print(corners[i])
        if len(corners) == 6:
            print('Pentagon corners: ')
            for i in range(1, len(corners)):
                print(corners[i])
        for i in range(1, len(corners)):
            print(corners[i,0])
            cv2.circle(img, (int(corners[i,0]), int(corners[i,1])), 7, (0,255,0), 2)
        # cv2.imshow('image', img)


cv2.imshow("TEST", img)



if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()