import cv2 as cv
import numpy as np 
import cv2.aruco as aruco


# reading image
img = cv.imread('Photos/aruco.png')

# grayscaling the image
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# loading marker dictionary
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# detect markers 
corners, ids, rej = aruco.detectMarkers(gray,dictionary) 

# just checking if corners nd ids are getting detected properly or not (not relevant to task, for my own convinience)
if ids is not None:
        print("ids detected: ", ids) 
        for i in range(len(ids)):
               element = corners[i]
               print("set of corners ",(i+1), element)


# outlining the boundary of these markers
if ids is not None:
        for i in range(len(ids)):
            # highlighting the outlines of the markers with blue 
            element = corners[i]
            coordinates = element[0].astype(int)
            cv.polylines(img, [coordinates], True, (255,0,0), 4)

            # putting marker id at the centre of the markers in green
            marker_id = ids[i]

            cx = int(coordinates[:,0].mean())
            cy = int(coordinates[:,1].mean())

            cv.putText(img, str(int(marker_id[0])),(cx,cy), cv.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2)



# output
cv.imshow('task1_output',img)
cv.waitKey(0)
cv.destroyAllWindows()

#saving the image
cv.imwrite('task1_output_aruco_annotated.png',img)












