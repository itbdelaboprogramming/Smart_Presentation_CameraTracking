import cv2
import numpy as np
import time
from src import HandTracking as ht
import pyautogui
# import autopy   # Install using "pip install autopy"

# Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

# Detecting one hand at max
detector = ht.handDetector(maxHands=2)
screen_width, screen_height = pyautogui.size()       # Getting the screen size
width = screen_width
height = screen_height


cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(
        img)           # Getting position of hand

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()      # Checking if fingers are upwards

        # If fore finger is up and middle finger is down
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, width-frameR), (0, screen_width))
            y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            # Moving the cursor
            # pyautogui.moveTo(screen_width - curr_x, curr_y) # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (0, 0, 0), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            if length < 20:
                print("ooo")
                # Ketika length kurang dari 20
                if length > 10:
                    print("rrr")
                    # Jika length kemudian lebih dari 40
                    # If both fingers are really close to each other
                    pyautogui.hotkey('ctrl', '+')

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
