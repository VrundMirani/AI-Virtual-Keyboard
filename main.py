
import cv2
import math
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# -------------------- CAMERA SETUP --------------------

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    raise RuntimeError("Unable to access webcam.")

detector = HandDetector(detectionCon=0.8)

pyautogui.FAILSAFE = True

# -------------------- KEYBOARD CONFIGURATION --------------------

KEY_WIDTH = 42
KEY_HEIGHT = 32
KEY_GAP = 4
ROW_GAP = 5

START_Y = 48
HORIZONTAL_OFFSET = -40

# Keyboard transparency
OVERLAY_ALPHA = 0.42
BACKGROUND_ALPHA = 0.58

keyboard_rows = [
    [
        ("1", "1", 1), ("2", "2", 1), ("3", "3", 1),
        ("4", "4", 1), ("5", "5", 1), ("6", "6", 1),
        ("7", "7", 1), ("8", "8", 1), ("9", "9", 1),
        ("0", "0", 1), ("-", "-", 1), ("=", "=", 1),
        ("BACK", "backspace", 2)
    ],
    [
        ("Q", "q", 1), ("W", "w", 1), ("E", "e", 1),
        ("R", "r", 1), ("T", "t", 1), ("Y", "y", 1),
        ("U", "u", 1), ("I", "i", 1), ("O", "o", 1),
        ("P", "p", 1), ("[", "[", 1), ("]", "]", 1),
        ("\\", "\\", 1)
    ],
    [
        ("A", "a", 1), ("S", "s", 1), ("D", "d", 1),
        ("F", "f", 1), ("G", "g", 1), ("H", "h", 1),
        ("J", "j", 1), ("K", "k", 1), ("L", "l", 1),
        (";", ";", 1), ("'", "'", 1), ("ENTER", "enter", 2)
    ],
    [
        ("SHIFT", "shift", 2),
        ("Z", "z", 1), ("X", "x", 1), ("C", "c", 1),
        ("V", "v", 1), ("B", "b", 1), ("N", "n", 1),
        ("M", "m", 1), (",", ",", 1), (".", ".", 1),
        ("/", "/", 1)
    ],
    [
        ("SPACE", "space", 6)
    ]
]

was_touching = False
shift_active = False


# -------------------- DRAW KEYBOARD --------------------

def draw_keyboard(img, pointer):

    overlay = img.copy()
    key_boxes = []

    frame_width = img.shape[1]

    for row_index, row in enumerate(keyboard_rows):

        total_units = sum(key[2] for key in row)

        total_width = (
            total_units * KEY_WIDTH
            + (len(row) - 1) * KEY_GAP
        )

        # Position keyboard slightly left of centre
        x = (
            (frame_width - total_width) // 2
            + HORIZONTAL_OFFSET
        )

        y = START_Y + row_index * (KEY_HEIGHT + ROW_GAP)

        for label, value, units in row:

            width = units * KEY_WIDTH + (units - 1) * KEY_GAP

            key_boxes.append(
                (label, value, (x, y, x + width, y + KEY_HEIGHT))
            )

            hovered = (
                pointer is not None
                and x <= pointer[0] <= x + width
                and y <= pointer[1] <= y + KEY_HEIGHT
            )

            # Dark charcoal keys
            if hovered:
                color = (100, 85, 65)
            else:
                color = (25, 25, 25)

            cv2.rectangle(
                overlay,
                (x, y),
                (x + width, y + KEY_HEIGHT),
                color,
                cv2.FILLED
            )

            # Key borders
            cv2.rectangle(
                overlay,
                (x, y),
                (x + width, y + KEY_HEIGHT),
                (90, 90, 90),
                1
            )

            # Key text
            font_scale = 0.62 if len(label) > 2 else 0.95

            text_size = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                1
            )[0]

            text_x = x + (width - text_size[0]) // 2
            text_y = y + (KEY_HEIGHT + text_size[1]) // 2

            cv2.putText(
                overlay,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (220, 220, 220),
                1,
                cv2.LINE_AA
            )

            x += width + KEY_GAP

    # Blend keyboard into camera background
    img = cv2.addWeighted(
        overlay,
        OVERLAY_ALPHA,
        img,
        BACKGROUND_ALPHA,
        0
    )

    return img, key_boxes


# -------------------- TYPE KEY --------------------

def type_key(value):

    global shift_active

    if value == "shift":

        shift_active = not shift_active

    elif value in ["space", "enter", "backspace"]:

        pyautogui.press(value)

    else:

        if shift_active:
            pyautogui.write(value.upper())
            shift_active = False

        else:
            pyautogui.write(value)


# -------------------- MAIN PROGRAM --------------------

try:

    while True:

        success, img = cap.read()

        if not success:
            break

        # Correct hand labels without mirroring camera image
        hands, img = detector.findHands(
            img,
            flipType=True
        )

        pointer = None
        touching = False

        if hands:

            landmarks = hands[0]["lmList"]

            index_tip = landmarks[8]
            middle_tip = landmarks[12]

            pointer = (
                index_tip[0],
                index_tip[1]
            )

            distance = math.hypot(
                index_tip[0] - middle_tip[0],
                index_tip[1] - middle_tip[1]
            )

            touching = distance < 35

        # Draw keyboard
        img, key_boxes = draw_keyboard(img, pointer)

        # Draw fingertip pointer
        if pointer is not None:

            cv2.circle(
                img,
                pointer,
                10,
                (0, 255, 255),
                cv2.FILLED
            )

            if touching:

                cv2.circle(
                    img,
                    pointer,
                    15,
                    (0, 255, 0),
                    3
                )

        # One key press per pinch gesture
        if touching and not was_touching and pointer is not None:

            for label, value, (x1, y1, x2, y2) in key_boxes:

                if (
                    x1 <= pointer[0] <= x2
                    and y1 <= pointer[1] <= y2
                ):

                    type_key(value)
                    break

        was_touching = touching

        # Shift status
        status = "SHIFT: ON" if shift_active else "SHIFT: OFF"

        status_color = (
            (0, 255, 0) if shift_active
            else (180, 180, 180)
        )

        cv2.putText(
            img,
            status,
            (30, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            status_color,
            2,
            cv2.LINE_AA
        )

        # Display camera window
        cv2.imshow("AI Virtual Keyboard", img)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:

    cap.release()
    cv2.destroyAllWindows()
