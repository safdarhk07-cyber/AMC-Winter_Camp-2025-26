import cv2 as cv
import numpy as np
import cv2.aruco as aruco 


# reading image
img = cv.imread('Photos/arena.png')

# loading marker dictionary 
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)

# detect markers 
corners, ids, rej = aruco.detectMarkers(img, dictionary)

# draw detectors
cv.aruco.drawDetectedMarkers(img, corners)

# create an empty list to store centres of the markers
centres = []

if ids is not None:
    for i in range(len(ids)):
        coord = corners[i]
        pts = coord[0].astype(int)

        # centre of marker i
        cx = int(pts[:,0].mean())
        cy = int(pts[:,1].mean())

        # # append into list
        centres.append([cx,cy])

        # not relevant to task 
        print(centres[i])
        print("\n")

# converting the python list of centre of markers into a numpy array 
centres_real = np.array(centres, dtype = np.int32)

# re-ordering the elements of the array to connect the points properly
# without re-ordering, the points were getting connected incorrectly and produced diagonals 
centres_real = centres_real[[2,3,0,1]]

# drawing the boundary of the arena
pts = centres_real.reshape(-1,1,2).astype(np.int32)
cv.polylines(img, [pts], True, (0,255,0), 4)


# detecting the yellow plants (or atleast trying to)

# converting to hsv
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# defining range of yellow colour (approach explained in text file)
lower_value = np.array([17,143,66], dtype=np.uint8)
upper_value = np.array([29, 250, 140],dtype = np.uint8)

# masking 
mask  = cv.inRange(hsv, lower_value, upper_value)

contours, cnt = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# for counting no. of yellow plants
yellow_plants = 0

for cont in contours:
    area = cv.contourArea(cont)
    if area > 230:    # area is calculated purely by error and trial
        x, y, l, b = cv.boundingRect(cont)
        cv.rectangle(img, (x, y), (x+l, y+b), (255,0,255), 2)
        yellow_plants += 1

print(yellow_plants) # will print 2 in this case


cv.imshow('yellow mask',img)
cv.waitKey(0)
cv.destroyAllWindows



