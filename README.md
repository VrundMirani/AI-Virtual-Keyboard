# AI Virtual Keyboard

**A touch-free virtual typing experience powered by Computer Vision and Real-Time Hand Tracking.**

AI Virtual Keyboard transforms your webcam into an interactive typing interface. Using hand landmark detection and gesture recognition, it enables users to interact with an on-screen keyboard and type without a physical keyboard.

## Overview

The project combines computer vision and gesture-based interaction to create a hands-free virtual keyboard. It tracks hand movements through a webcam, detects finger positions, and interprets gestures to trigger keyboard interactions in real time.

The objective is to explore intuitive human-computer interaction by replacing traditional keyboard input with a vision-based interface.

## Key Features

- **Real-Time Hand Tracking:** Detects and tracks hand landmarks through a webcam.
- **Virtual Keyboard Interface:** Displays an interactive keyboard overlay on the camera feed.
- **Gesture-Based Typing:** Uses finger gestures and pinch detection to select and activate keys.
- **Keyboard Controls:** Supports special keys such as SHIFT.
- **Live Visual Feedback:** Displays hand landmarks, keyboard interactions, and visual selection feedback.
- **Touch-Free Interaction:** Enables typing without directly touching a physical keyboard.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core development |
| OpenCV | Camera processing and visual interface |
| MediaPipe | Hand landmark detection |
| CVZone | Hand tracking utilities |
| PyAutoGUI | Keyboard input automation |

## Project Structure

```text
AI-Virtual-Keyboard/
│
├── main.py          # Main application and gesture recognition
├── .gitignore       # Excluded files and directories
├── README.md        # Project documentation
└── .venv/           # Local virtual environment (not tracked)
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VrundMirani/AI-Virtual-Keyboard.git
cd AI-Virtual-Keyboard
```

### 2. Create a Virtual Environment

```bash
py -3.12 -m venv .venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install opencv-contrib-python==4.11.0.86 mediapipe==0.10.21 cvzone==1.6.1 pyautogui==0.9.54
```

### 5. Run the Application

```bash
python main.py
```

Make sure your webcam is connected and accessible before starting the application.

## How It Works

1. The webcam captures live video frames.
2. MediaPipe and CVZone detect and track hand landmarks.
3. Finger positions and gestures are analyzed in real time.
4. Pinch-based interaction identifies the selected virtual key.
5. PyAutoGUI translates the interaction into keyboard input.

## Requirements

- Windows operating system
- Python 3.12
- Webcam
- Working internet connection for initial dependency installation

## Future Improvements

- Multi-hand interaction support
- Customizable keyboard layouts
- Improved gesture recognition and interaction accuracy
- Additional keyboard shortcuts and accessibility controls
- Enhanced visual customization

## Author

**Vrund Mirani**

[GitHub Profile](https://github.com/VrundMirani)

---

*Exploring the intersection of Computer Vision, Gesture Recognition, and Human-Computer Interaction.*