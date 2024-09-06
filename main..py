from cvzone.HandTrackingModule import HandDetector
import pygame
import cv2

# Initialize pygame for audio playback
pygame.init()
pygame.mixer.init()

# Load audio files
audio_file1 = 'A_Major.wav'
sound1 = pygame.mixer.Sound(audio_file1)

audio_file2 = 'C_Major.wav'
sound2 = pygame.mixer.Sound(audio_file2)

audio_file3 = 'E_Major.wav'
sound3 = pygame.mixer.Sound(audio_file3)

audio_file4 = 'G_Major.wav'
sound4 = pygame.mixer.Sound(audio_file4)

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 2200)
cap.set(4, 1000)

# Initialize HandDetector
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Define rectangle coordinates
rect1_x1, rect1_y1 = 200, 200
rect1_x2, rect1_y2 = 400, 400
rect2_x1, rect2_y1 = 430, 200
rect2_x2, rect2_y2 = 630, 400
rect3_x1, rect3_y1 = 660, 200
rect3_x2, rect3_y2 = 860, 400
rect4_x1, rect4_y1 = 890, 200
rect4_x2, rect4_y2 = 1090, 400

# Track the last played state
last_played = {1: False, 2: False, 3: False, 4: False}

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not success:
        break

    # Draw rectangles
    cv2.rectangle(img, (rect1_x1, rect1_y1), (rect1_x2, rect1_y2), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (rect2_x1, rect2_y1), (rect2_x2, rect2_y2), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (rect3_x1, rect3_y1), (rect3_x2, rect3_y2), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (rect4_x1, rect4_y1), (rect4_x2, rect4_y2), (0, 255, 0), cv2.FILLED)

    # Put text inside rectangles
    cv2.putText(img, "A", (rect1_x1 + 80, rect1_y1 + 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(img, "C", (rect2_x1 + 80, rect2_y1 + 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(img, "E", (rect3_x1 + 80, rect3_y1 + 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(img, "G", (rect4_x1 + 80, rect4_y1 + 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

    hands, img = detector.findHands(img, draw=True, flipType=False)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            finger_tip = lmList[8]
            finger_x, finger_y = finger_tip[0], finger_tip[1]

            if rect1_x1 <= finger_x <= rect1_x2 and rect1_y1 <= finger_y <= rect1_y2:
                if not last_played[1]:
                    cv2.putText(img, "Inside Box 1", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
                    sound1.play()
                    last_played = {1: True, 2: False, 3: False, 4: False}
            elif rect2_x1 <= finger_x <= rect2_x2 and rect2_y1 <= finger_y <= rect2_y2:
                if not last_played[2]:
                    cv2.putText(img, "Inside Box 2", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
                    sound2.play()
                    last_played = {1: False, 2: True, 3: False, 4: False}
            elif rect3_x1 <= finger_x <= rect3_x2 and rect3_y1 <= finger_y <= rect3_y2:
                if not last_played[3]:
                    cv2.putText(img, "Inside Box 3", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
                    sound3.play()
                    last_played = {1: False, 2: False, 3: True, 4: False}
            elif rect4_x1 <= finger_x <= rect4_x2 and rect4_y1 <= finger_y <= rect4_y2:
                if not last_played[4]:
                    cv2.putText(img, "Inside Box 4", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
                    sound4.play()
                    last_played = {1: False, 2: False, 3: False, 4: True}

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
