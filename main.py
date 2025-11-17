import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import pyautogui
import subprocess
import time
import win32gui
import win32con
import os


WHATSAPP_WINDOW_NAME = "WhatsApp"
CONTACT_NAME = "Amma"
EMERGENCY_MESSAGE = " EMERGENCY! I NEED HELP! "

SEARCH_BAR_COORDS = (194, 147)
CHAT_COORDS = (210, 212)
MESSAGE_BOX_COORDS = (597, 985)
SEND_BUTTON_COORDS = (1676, 186)

CANVAS_W, CANVAS_H = 1280, 720
PREVIEW_W, PREVIEW_H = 220, 165
brush_color = (0, 0, 255)
brush_size = 6

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands_detector = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

canvas = np.ones((CANVAS_H, CANVAS_W, 3), dtype=np.uint8) * 255
points = deque(maxlen=500)
smooth = deque(maxlen=7)
emergency_done = False


def fingers_up(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    
    fingers.append(1 if hand.landmark[4].x < hand.landmark[3].x else 0)

    
    for tip in tips[1:]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0)

    return fingers

def open_whatsapp():
    try:
        hwnd = win32gui.FindWindow(None, WHATSAPP_WINDOW_NAME)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(hwnd)
            return True

        exe_path = os.path.expanduser(r"~\AppData\Local\WhatsApp\WhatsApp.exe")
        if os.path.exists(exe_path):
            subprocess.Popen(exe_path)
            time.sleep(5)
            return True

        subprocess.Popen(["start", "whatsapp:"], shell=True)
        time.sleep(5)
        return True

    except:
        return False

def send_whatsapp_message():
    global emergency_done
    print("🚨 Sending WhatsApp Emergency Message...")

    if not open_whatsapp():
        print("❌ ERROR: WhatsApp could not be opened.")
        return

    try:
        pyautogui.click(*SEARCH_BAR_COORDS)
        time.sleep(0.5)
        pyautogui.write(CONTACT_NAME)
        time.sleep(1)

        pyautogui.click(*CHAT_COORDS)
        time.sleep(0.5)

        pyautogui.click(*MESSAGE_BOX_COORDS)
        pyautogui.write(EMERGENCY_MESSAGE)
        time.sleep(0.3)

        pyautogui.click(*SEND_BUTTON_COORDS)
        time.sleep(0.2)

        print("✅ Emergency message sent!")
        emergency_done = True

    except Exception as e:
        print("❌ Error:", e)


cv2.namedWindow("AI Drawing Assistant", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("AI Drawing Assistant", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print("🎨 CONTROLS:")
print("Index finger → Draw")
print("Fist → Stop drawing")
print("5 fingers → Clear canvas")
print("4 fingers  UP 1 DOWN → WhatsApp Emergency")
print("Press 'ESC' → Quit")


cap = cv2.VideoCapture(0)
cap.set(3, CANVAS_W)
cap.set(4, CANVAS_H)

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(rgb)

    key = cv2.waitKey(1)
    if key == 27:
        break

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        fingers = fingers_up(hand)
        total = sum(fingers)

        ix = int(hand.landmark[8].x * CANVAS_W)
        iy = int(hand.landmark[8].y * CANVAS_H)

        smooth.append((ix, iy))
        avg_x = int(np.mean([p[0] for p in smooth]))
        avg_y = int(np.mean([p[1] for p in smooth]))

       
        if sum(fingers) == 4 and not emergency_done:
            print(" Emergency Gesture Detected (4 UP 1 DOWN)!")
            send_whatsapp_message()

        
        if fingers == [0, 1, 0, 0, 0]:
            points.append((avg_x, avg_y))
            if len(points) > 1:
                cv2.line(canvas, points[-2], points[-1], brush_color, brush_size)
        else:
            points.clear()

        
        if total == 5:
            canvas[:] = 255
            points.clear()
            smooth.clear()

    
    preview = cv2.resize(frame, (PREVIEW_W, PREVIEW_H))
    canvas[10:10+PREVIEW_H, CANVAS_W-PREVIEW_W-10:CANVAS_W-10] = preview

    cv2.imshow("AI Drawing Assistant", canvas)

cap.release()
cv2.destroyAllWindows()
