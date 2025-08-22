# Traffic Monitoring System

This project implements a traffic monitoring system using computer vision to detect vehicles, analyze traffic density, and determine congestion status.

## Features

- Vehicle detection using OpenCV
- Real-time vehicle counting
- Traffic density calculation
- Congestion status monitoring
- Visual feedback with annotations

## Project Structure

```
STL/
├── src/
│   ├── main.py              # Main application entry point
│   ├── vehicle_detector.py  # Vehicle detection implementation
│   └── traffic_analyzer.py  # Traffic analysis logic
└── data/                    # Directory for video files (if using recorded videos)
```

## Requirements

- Python 3.x
- OpenCV (opencv-python)
- NumPy

## Installation

1. Ensure Python is installed on your system
2. Install required packages:
   ```bash
   pip install opencv-python numpy
   ```

## Usage

1. Run the main script:
   ```bash
   python src/main.py
   ```

2. The program will start using your default webcam. To use a video file instead, modify the video source in `main.py`:
   ```python
   cap = cv2.VideoCapture('path_to_your_video.mp4')
   ```

3. Press 'q' to quit the application

## Configuration

You can adjust the following parameters in the code:

- `density_threshold` in `TrafficAnalyzer` class: Threshold for determining traffic congestion
- Detection parameters in `VehicleDetector` class for better detection accuracy
