import cv2 as cv 
import numpy as np 
import math


#reading image and grayscaling it 
img = cv.imread('Photos/polygons.png')

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#thresholding the image 
threshold, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

#finding countours 
contours, cont = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

output_centroid = []

for cnt in contours:
    area = cv.contourArea(cnt)
    peri = cv.arcLength(cnt, True)

    if peri == 0:
        continue

    # 1)circularity check 
    circularity = 4* math.pi* area /(peri* peri)

    # 2) approximating sides
    approx = cv.approxPolyDP(cnt, 0.02* peri, True)
    vertices = len(approx)

    # 3) checking the polygon 
    if circularity > 0.8:
        shape = "circle"
    
    else: 
        if vertices == 3:
            shape = "triangle"
        if vertices == 4:
            shape = "quadilateral"
        if vertices == 5:
            shape = "pentagon"
        if vertices == 6:
            shape = "hexagon"
        if vertices == 7:
            shape = "heptagon"
        if vertices == 8:
            shape = "octagon"
    
    # locating centroid 
    M = cv.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0

    cv.drawContours(img, [cnt], -1, (0, 255, 0), 2)
    cv.putText(img, shape, (cx - 40, cy - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    print(f"{shape} → Centroid: ({cx}, {cy}), circularity={circularity:.2f}")

    output_centroid.append(f"{shape} -> Centroid: ({cx}, {cy}), circularity={circularity:.2f}\n")

#output text file 
with open("task2_output_centroids.txt", "w") as f:
    f.writelines(output_centroid)

print("\nresults saved to task2_output_centroids.txt")



#output 
cv.imshow("detected shapes", img)
cv.waitKey(0)
cv.destroyAllWindows()




