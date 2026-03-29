# AIML-Project-Vityaarthi
AI Air Drawing Canvas (Computer Vision Project)
An interactive digital canvas that allows users to draw in 3-0 space using hand gestures. This project uses OpenCv and MediaPipe to track hand movements and translate them into digital art in real-time.

✨ Features
Contactless Drawing: Draw using only your index finger.

Air-Tap Menu: Open the RGB color palette by "tapping" the air twice near the menu icon.

Two-Finger Color Scrub: Change colors by sliding two fingers across the rainbow bar.

Smart Eraser: Use three fingers to erase parts of your drawing.

Gesture Stability: Only draws when the hand is in a "standing" (upright) position to prevent accidental lines.

🛠️ Tech Stack
Python 3.12

OpenCV: For video processing and canvas rendering.

MediaPipe: For high-fidelity hand landmark tracking.

NumPy: For matrix-based canvas manipulation.

🚀 Setup & Installation
Clone the repository:

Bash
git clone https://github.com/your-username/air-drawing-project.git
cd air-drawing-project
Install Dependencies:

Bash
pip install opencv-python mediapipe numpy
Run the Project:

Bash
python Project.py
🎮 How to Use
To Draw: Hold your hand upright and use your index finger.

To Open Menu: Point at the "RGB" circle and "Double Tap" toward the camera.

To Change Color: With the menu open, hold up two fingers and slide left/right.

To Erase: Hold up three fingers to wipe the screen.

To Close Menu: Start drawing with one finger, and the menu will auto-hide.
