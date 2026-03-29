# 🎨 AI Gesture-Paint: Next-Gen Air Drawing Canvas
**VITyarthi AIML Capstone Project (BYOP)**

---

## 🌌 Project Overview
**AI Gesture-Paint** is a touchless, gesture-controlled digital art application that transforms a standard webcam into a virtual canvas. By leveraging high-fidelity hand tracking and real-time image processing, this project eliminates the need for physical mice or touchscreens, offering a **Natural User Interface (NUI)** for creative expression.

### 💡 The Problem
Digital art often requires expensive hardware. Additionally, in many professional and public environments, "touchless" interfaces are becoming a necessity for hygiene and accessibility. This project solves the barrier to entry for digital sketching by using a standard laptop webcam and Python.

---

## 🚀 Core Features & Gestures

| Feature | Gesture Logic | Action |
| :--- | :--- | :--- |
| **Precision Draw** | Index finger extended (Standing position) | Draws a 5px line on the canvas |
| **Air-Tap Menu** | Rapid Z-axis "Double Tap" near RGB icon | Toggles the stylish color palette |
| **RGB Scrubbing** | Index + Middle fingers (2-Finger slide) | Slides through the full HSV color spectrum |
| **Smart Eraser** | Index + Middle + Ring fingers up | Activates a 80px circular eraser |
| **Auto-Hide UI** | Single finger drawing motion | Closes menu to maximize drawing space |
| **Safety Lock** | Hand tilt or wrist-up position | Pauses drawing to prevent accidental marks |

---

## 🛠️ Technical Architecture

### 1. Hand Landmark Mapping
The engine utilizes a 21-point hand landmark model provided by MediaPipe. We calculate the Euclidean distance between points and compare the Y-coordinates of finger tips relative to knuckles to interpret user intent.

### 2. Dual-Layer Rendering
The system maintains two distinct layers:
* **Frame Layer:** The live webcam feed processed at 1280x720.
* **Canvas Layer:** A NumPy black matrix where drawing persists.
The two layers are merged using bitwise operations (`cv2.bitwise_and` and `cv2.bitwise_or`) to create a seamless overlay.

### 3. Dynamic Color Engine
Instead of fixed buttons, the project uses the **HSV (Hue, Saturation, Value)** color space. Users can select any color by sliding two fingers across the rainbow bar generated via the `colorsys` library.

---

## ⚙️ Development Environment
* **Language:** Python 3.12 (Stable)
* **Libraries:** OpenCV, MediaPipe, NumPy, Colorsys.

---

## 📥 Setup & Execution
1. Install the required libraries:
   `pip install opencv-python mediapipe numpy`

2. Run the application:
   `python Project.py`

---

## 🧠 Reflection & Challenges
* **The Z-Axis Challenge:** Detecting a "click" in 2D video is difficult. I solved this by tracking the `z` coordinate of the index finger tip and measuring the velocity of movement toward the camera to trigger an "Air Tap."
* **Library Stability:** Transitioning from Python 3.14 (experimental) to 3.12 (stable) was a key learning moment regarding dependency management.
* **Latency Optimization:** By limiting the tracking to a single hand and optimizing the NumPy overlay logic, I achieved a consistent 30+ FPS, ensuring a lag-free experience.
