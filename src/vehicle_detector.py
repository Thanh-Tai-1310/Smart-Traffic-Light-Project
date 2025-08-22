import cv2
import numpy as np

class VehicleDetector:
    def __init__(self):
        # Load the pre-trained vehicle detection model (using HOG + SVM by default)
        self.car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')
        
    def detect_vehicles(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect vehicles in the frame
        vehicles = self.car_cascade.detectMultiScale(gray, 1.1, 2)
        
        return vehicles
        
    def draw_detections(self, frame, vehicles):
        # Draw rectangles around detected vehicles
        for (x, y, w, h) in vehicles:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        return frame
