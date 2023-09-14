from math import dist
import mediapipe as mp
import cv2
import numpy as np
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

model_path = './Smart_Presentation_CameraTracking/learning-mediapipe/python/gesture_recognizer.task'

count = 0
is_hands_close = False
close_timeout = None

# Function to measure hand distance


def check_hand_distance(first_hand, second_hand):
    thumb_distance = abs(first_hand[4].x - second_hand[4].x)
    return thumb_distance < 0.15


# Zooming Function and Variable---------------------------------------------
zoom_out_interval = None
zoom_int_interval = None
# ---------------------------------------------------------------

def hands_apart(first_hand, second_hand):
    thumb_distance = abs(first_hand[4].x - second_hand[4].x)
    return thumb_distance > 0.15

# ---------------------------------------------------------------


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            # only detect 2 hands
            if len(results.multi_hand_landmarks) == 2:

                # first hand
                first_hand = results.multi_hand_landmarks[0].landmark
                # get all of coordinate in first hand
                for idx in first_hand:

                    # print(idx.x, idx.y, idx.z)
                    x1, y1, z1 = idx.x, idx.y, idx.z

                    # create mark in coordinate
                    position = (
                        int(x1 * image.shape[1]), int(y1 * image.shape[0]))
                    color = (0, 0, 255)
                    # Mark radius
                    radius = 5
                    cv2.circle(image, position, radius, color, -1)

                # second hand
                second_hand = results.multi_hand_landmarks[1].landmark
                for idx in second_hand:
                    x2, y2, z2 = idx.x, idx.y, idx.z

                    position = (
                        int(x2 * image.shape[1]), int(y2 * image.shape[0]))

                    color = (0, 0, 255)
                    radius = 5

                    cv2.circle(image, position, radius, color, -1)

                hands_close = check_hand_distance(first_hand, second_hand)

                if hands_close:
                    zoom_in_interval = time.time()+1
                elif zoom_in_interval != None and time.time() < zoom_in_interval:
                    if not hands_close:
                        pyautogui.hotkey('ctrl', '+')
                    zoom_in_interval = None

                #
                if not hands_close:
                    zoom_out_interval = time.time()+1
                elif zoom_out_interval != None and time.time() < zoom_out_interval:
                    if hands_close:
                        pyautogui.hotkey('ctrl', '-')
                    zoom_out_interval = None

            # 1 hand detection
            # if len(results.multi_hand_landmarks) == 1:
            #     print("tess")

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
