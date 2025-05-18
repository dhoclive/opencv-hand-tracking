# Gesture-Based Slide Control

This project allows you to control presentation slides using hand gestures through your camera.

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv lib
source lib/bin/activate  # For Linux/Mac
lib\Scripts\activate     # For Windows
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Available Controls

### 1. Slide-Pinch Control
Run `slide-pinch.py` to use pinch gestures:
- Next slide: Pinch thumb and index finger
- Previous slide: Pinch thumb and middle finger

### 2. Slide-Swipe Control  
Run `slide-swipe.py` to use swipe gestures:
- Next slide: Swipe hand right
- Previous slide: Swipe hand left

Make sure your camera has clear view of your hand gestures for optimal detection.