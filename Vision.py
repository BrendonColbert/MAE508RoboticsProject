import cv2
import numpy as np

WINDOW_NAME = 'GreenBallTracker' 

def mousePosition(event,x,y,flags,param):

    if event == cv2.EVENT_MOUSEMOVE:
        print x,y
        param = (x,y)

def track(image,lower_color,upper_color):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    # lower_green = lower_color # np.array([40,70,70])
    # upper_green = upper_color # np.array([80,200,200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        # Put Red circle in at centroid in image
        # cv2.circle(image, ctr, 8, (0,100,100), 5)

    # Display full-color image
    # cv2.imshow(WINDOW_NAME, bmask)
    # cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid
    return ctr

# Test with input from camera
if __name__ == '__main__':
    green_lower = np.array([40,70,70])
    green_upper = np.array([80,200,200])
    red_upper   = np.array([250,200,200])
    red_lower   = np.array([160,50,50])
    blue_upper  = np.array([120,200,200])
    blue_lower  = np.array([100,70,70])
    capture = cv2.VideoCapture(0)
    

    okay, image = capture.read()
    img = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('image')
    

    while(1):
        cv2.setMouseCallback('Drawing spline',mousePosition,param)

    while True:
	okay, image = capture.read()
        if okay:
            locR = track(image,red_lower,red_upper)
	    locB = track(image,blue_lower,blue_upper)
	    locG = track(image,green_lower,green_upper)
            diff = ( locB[0] - locG[0], locB[1] - locG[1])
            # print(np.angle(diff[0]+diff[1]*1j, deg=True) )
	    cv2.line(image,locB,locG,(255,255,255),10)
	    cv2.circle(image,(10,10),8,(255,255,255),10)
	    cv2.imshow('Robot Tracker', image )
	    cv2.setMouseCallback('Robot Tracker',draw_circle)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break
