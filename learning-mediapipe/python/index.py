from math import dist
import mediapipe as mp
import cv2
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

model_path = './Smart_Presentation_CameraTracking/learning-mediapipe/python/gesture_recognizer.task'

# Function to measure hand distance


def check_hand_distance(first_hand, second_hand):
    thumb_distance = abs(first_hand[4]['x'] - second_hand[4]['x'])
    return thumb_distance < 0.15


def on_hands_close():
    print("Tangan berdekatan, menjalankan fungsi...")


def on_hands_apart():
    print("Tangan berjauhan, menjalankan fungsi...")


def set_close_timeout():
    global close_timeout, is_hands_close
    close_timeout = None  # Inisialisasi timeout
    # Waktu timeout dalam detik (1 detik dalam contoh ini)
    close_timeout = time.time() + 1
    is_hands_close = True


def cancel_close_timeout():
    global close_timeout, is_hands_close
    if close_timeout:
        if time.time() < close_timeout:
            on_hands_close()  # Jika timeout belum tercapai, tangan tetap berdekatan
        close_timeout = None
        is_hands_close = False


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
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
            print("tttt", results.multi_hand_landmarks)
            for hand_landmarks in results.multi_hand_landmarks:
                firstHand = results.multi_hand_landmarks[0]
                secondHand = results.multi_hand_landmarks[9]

                handsClose = checkHandDistance(firstHand, secondHand)

                if handsClose and not isHandsClose:
                    onHandsClose()
                    isHandsClose = true
                    setCloseTimeout()

                elif not handsClose and isHandsClose:
                    cancelCloseTimeout()
                    onHandsApart()
                    isHandsClose = false

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()