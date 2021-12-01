#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
from pynput.keyboard import Controller, Key

keyboard = Controller()

video = VideoStream(src=0).start()
frame = None

lb = [40, 100, 0]
rb = [0xFF, 0xFF, 0xFF]


def set_lb(i, v):
    lb[i] = v


def set_rb(i, v):
    rb[i] = v


actions = ['', '']

cv2.namedWindow('mask')

def press_key(key): #Press a key 
    keyboard.press(key)


def straighten(): #Release the left and right key
    keyboard.release(Key.left)
    keyboard.release(Key.right)


def neutral(): #Release the up and down key 
    keyboard.release(Key.up)
    keyboard.release(Key.down)


def direction(angle): #Actions depends on the angle of the steering wheel
    if 70 <= angle <= 105:
        actions[1] = 'straight'
        straighten()
    elif angle > 105:
        actions[1] = 'left'
        press_key(Key.left)
    elif angle < 70:
        actions[1] = 'right'
        press_key(Key.right)


def gas(y): #State of the car (Accelerating/Braking/Coasting) depend on the position y of the steering wheel
    if 200 <= y <= 250:
        actions[0] = 'Coasting'
        neutral()
    elif y < 200:
        actions[0] = 'Accelerating'
        press_key(Key.up)
    elif y > 250:
        actions[0] = 'Braking'
        press_key(Key.down)


def get_action():#Return actions with correct format to display
    return '{} {}'.format(actions[0], actions[1])


def process_wheel():  #Find the center of 2 BLUE area and draw a line between the two center. Calculate the angle of the line 
    global frame
    wheel_frame = frame.copy()

    hsv = cv2.cvtColor(wheel_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array(lb.copy())  # [35, 100, 0]
    upper_blue = np.array(rb.copy())  # [255, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    anded_res = cv2.bitwise_and(wheel_frame, wheel_frame, mask=mask)
    (contours, _) = cv2.findContours(cv2.Canny(anded_res, 0xFF / 3,
            0xFF), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    area_threshold = 400
    inds = []
    for (i, c) in enumerate(contours): #For each contours found, check if the area is bigger than the threshold and if our 2 area aren't already found.
        a = cv2.contourArea(c)
        if a > area_threshold and len(inds) < 2:
            inds.append(i)

    if not inds or len(inds) != 2: #If no area found
        cv2.imshow('wheel', wheel_frame)  # [165:200, 326:500])
 
        #' cv2.imshow('mask', mask)  # [165:200, 326:500]) #Display mask

        return

    if cv2.contourArea(contours[inds[0]]) \
        < cv2.contourArea(contours[inds[1]]): #Place the biggest area in first
        (inds[0], inds[1]) = (inds[1], inds[0])

    #Calculate moments of the 2 areas
    moments1 = cv2.moments(contours[inds[0]])
    moments2 = cv2.moments(contours[inds[1]])

    #Calculate coordinate of center
    p1 = [int(moments1['m10'] / moments1['m00']), int(moments1['m01']
          / moments1['m00'])]
    p2 = [int(moments2['m10'] / moments2['m00']), int(moments2['m01']
          / moments2['m00'])]

    #Draw circle around the center of the areas
    cv2.circle(wheel_frame, (p1[0], p1[1]), 3, (0xFF, 0xFF, 0xFF), -1)
    cv2.circle(wheel_frame, (p2[0], p2[1]), 3, (0xFF, 0xFF, 0xFF), -1)

    #Draw line between the 2 center points
    cv2.line(wheel_frame, (p1[0], p1[1]), (p2[0], p2[1]), (0, 0xFF, 0),
             2)
    #Calculate the angle of the line with coordinates of the 2 points
    if p2[0] - p1[0] == 0:
        angle = 90
    else:
        angle = -np.rad2deg(np.arctan2(p2[1] - p1[1], p2[0] - p1[0])) \
            % 360

    #Draw the contours of the area
    cv2.drawContours(wheel_frame, contours, inds[0], (0, 0, 0xFF), 2)
    cv2.drawContours(wheel_frame, contours, inds[1], (0, 0xFF, 0), 2)

    #Display angle and actions
    cv2.putText(
        wheel_frame,
        'Steering angle: {}'.format(np.round(angle)),
        (10, 100),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (0xFF, 0xFF, 0),
        2,
        )
    cv2.putText(
        wheel_frame,
        '{}'.format(get_action()),
        (10, 140),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (0xFF, 0xFF, 0),
        2,
        )

    #Draw 2 lines as center of the frame to change the state (Up the first line = Accelerating / Between the two line = Coasting / Under the third line = Braking)
    cv2.line(wheel_frame, (0, 200), (600, 200), (0xFF, 0xFF, 0xFF), 1)
    cv2.line(wheel_frame, (0, 250), (600, 250), (0xFF, 0xFF, 0xFF), 1)
    direction(angle)
    gas(p1[1])
    cv2.imshow('wheel', wheel_frame)  # [165:200, 326:500])


    #cv2.imshow('mask', mask)  # [165:200, 326:500]) #Display mask

while True:

    # Capture frame-by-frame
    
    frame = video.read()
    # print(frame)
    frame = cv2.flip(frame, 1)
    frame = cv2.medianBlur(frame, 5)
    frame = imutils.resize(frame, width=600, height=400)

    process_wheel()

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture

video.stop()
cv2.destroyAllWindows()
