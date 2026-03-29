import cv2
import numpy as np
import mediapipe as mp
import colorsys
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

canvas = np.zeros((720, 1280, 3), np.uint8)
px, py = 0, 0
brush_color = (255, 0, 255)
hue = 0.0
show_menu = False
menu_pos = [150, 150]
last_z = 0
tap_count = 0
last_tap_time = 0

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mx, my = menu_pos
    overlay = frame.copy()
    cv2.circle(overlay, (mx, my), 45, (50, 50, 50), -1)
    cv2.circle(overlay, (mx, my), 40, brush_color, 3)
    cv2.putText(overlay, "RGB", (mx - 22, my + 8), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    if show_menu:
        cv2.rectangle(overlay, (mx + 60, my - 60), (mx + 420, my + 60), (30, 30, 30), -1)
        for i in range(300):
            color_hue = i / 300.0
            rgb = colorsys.hsv_to_rgb(color_hue, 1.0, 1.0)
            bgr = (int(rgb[2] * 255), int(rgb[1] * 255), int(rgb[0] * 255))
            cv2.line(overlay, (mx + 80 + i, my - 25), (mx + 80 + i, my + 25), bgr, 2)

    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        lms = results.multi_hand_landmarks[0].landmark
        wrist = lms[0]
        idx_tip = lms[8]
        idx_knuckle = lms[5]
        mid_tip = lms[12]
        rng_tip = lms[16]

        ix, iy, iz = int(idx_tip.x * w), int(idx_tip.y * h), idx_tip.z
        mx_tip, my_tip = int(mid_tip.x * w), int(mid_tip.y * h)

        if wrist.y > idx_knuckle.y:
            # 1. Air Tap Logic (Z-axis movement)
            if np.hypot(ix - mx, iy - my) < 80:
                if (last_z - iz) > 0.02:  # Moving toward camera
                    curr_time = time.time()
                    if curr_time - last_tap_time < 0.5:
                        tap_count += 1
                    else:
                        tap_count = 1
                    last_tap_time = curr_time
                    if tap_count >= 2:
                        show_menu = not show_menu
                        tap_count = 0
            last_z = iz

            # Identify which fingers are up
            index_up = idx_tip.y < lms[6].y
            middle_up = mid_tip.y < lms[10].y
            ring_up = rng_tip.y < lms[14].y

            # 2. Erase (3 Fingers)
            if index_up and middle_up and ring_up:
                if px != 0: cv2.line(canvas, (px, py), (ix, iy), (0, 0, 0), 80)
                px, py = ix, iy
                cv2.circle(frame, (ix, iy), 40, (255, 255, 255), 2)

            # 3. Change Color (2 Fingers Scrubbing)
            elif index_up and middle_up:
                if show_menu and my - 80 < iy < my + 80:
                    if mx + 80 < ix < mx + 380:
                        hue = (ix - (mx + 80)) / 300.0
                        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                        brush_color = (int(rgb[2] * 255), int(rgb[1] * 255), int(rgb[0] * 255))
                px, py = 0, 0
                cv2.circle(frame, (ix, iy), 10, brush_color, -1)
                cv2.circle(frame, (mx_tip, my_tip), 10, brush_color, -1)

            # 4. Draw (1 Finger) - Closes menu
            elif index_up:
                if show_menu and iy > my + 100: show_menu = False
                if px != 0: cv2.line(canvas, (px, py), (ix, iy), brush_color, 5)
                px, py = ix, iy
                cv2.circle(frame, (ix, iy), 8, brush_color, -1)
            else:
                px, py = 0, 0
        else:
            px, py = 0, 0
    else:
        px, py = 0, 0

    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Air Tap RGB Pro", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()