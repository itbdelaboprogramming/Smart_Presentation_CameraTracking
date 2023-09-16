from math import dist
import mediapipe as mp
import cv2
import numpy as np
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)           # Adjusting size
cap.set(4, screen_height)

model_path = './Smart_Presentation_CameraTracking/learning-mediapipe/python/gesture_recognizer.task'

# Create command area -----------------------------------------------------------------


def bot_checker(hand):
    if hand.y > 0.2 and hand.y < 0.6:
        return True
    else:
        return False


def hand_inside_bottom_area(first, second):
    first_bot = first[0]
    second_bot = second[0]

    if bot_checker(first_bot) and bot_checker(second_bot):
        return True
    else:
        return False


def side_checker(hand):
    if hand.x < 0.8 and hand.x > 0.15:
        return True
    else:
        return False


def hand_inside_side_area(first, second):
    first_bot = first[20]
    second_bot = second[20]

    if side_checker(first_bot) and side_checker(second_bot):
        return True
    else:
        return False
# -------------------------------------------------------------------------------------

# Zooming Function and Variable---------------------------------------------------------

# Function to measure hand distance


def check_hand_distance(first_hand, second_hand):
    thumb_distance = abs(first_hand[4].x - second_hand[4].x)
    return thumb_distance < 0.15


zoom_out_interval = None
zoom_in_interval = None

# --------------------------------------------------------------------------------------


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

        # Calculate rectangle dimensions and position
        rectangle_width = int(screen_width * 0.20)
        rectangle_height = int(screen_height * 0.2)
        x = (screen_width - rectangle_width) // 2
        y = (screen_height - rectangle_height) // 2

        tes_x = int(100)
        tes_y = int(110)

        # Draw a yellow rectangle border in the center of the screen
        yellow_color = (0, 255, 255)  # Yellow in BGR
        border_thickness = 1  # Set the border thickness
        cv2.rectangle(image, (tes_x, tes_y), (rectangle_width,
                      rectangle_height), yellow_color, border_thickness)

        if results.multi_hand_landmarks:
            # only detect 2 hands
            if len(results.multi_hand_landmarks) == 2:

                # first hand
                first_hand = results.multi_hand_landmarks[0].landmark
                # get all of coordinate in first hand
                for idx in first_hand:
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

                if hand_inside_side_area(first_hand, second_hand) and hand_inside_bottom_area(first_hand, second_hand):
                    if hands_close:
                        zoom_in_interval = time.time()+1
                    elif zoom_in_interval != None and time.time() < zoom_in_interval:
                        if not hands_close:
                            pyautogui.scroll(20)
                        zoom_in_interval = None

                    if not hands_close:
                        zoom_out_interval = time.time()+1
                    elif zoom_out_interval != None and time.time() < zoom_out_interval:
                        if hands_close:
                            pyautogui.scroll(-20)
                        zoom_out_interval = None

                

            # if len(results.multi_hand_landmarks) == 1:
            #     # first hand
            #     first_hand = results.multi_hand_landmarks[0].landmark[20]

            #     x1, y1, z1 = first_hand.x, first_hand.y, first_hand.z

            #     # create mark in coordinate
            #     position = (
            #         int(x1 * image.shape[1]), int(y1 * image.shape[0]))
            #     color = (0, 0, 255)
            #     # Mark radius
            #     radius = 5
            #     cv2.circle(image, position, radius, color, -1)

            #     # print("x : ",x1)
            #     # print("y : ",y1)
            #     # print("z : ",z1)

            #     if x1 < 0.8 and x1 > 0.15:
            #         print("ttt")

        # Show the image in the OpenCV window

        # Create the OpenCV window with a specific size
        # Create a resizable window
        cv2.namedWindow('MediaPipe Hands', cv2.WINDOW_NORMAL)
        # Set the desired width and height
        cv2.resizeWindow('MediaPipe Hands', screen_width, screen_height)
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
