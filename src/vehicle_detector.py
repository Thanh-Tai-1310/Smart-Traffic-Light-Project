import cv2
import numpy as np

class VehicleDetector:
    def __init__(self):
        # Load the pre-trained vehicle detection model (using HOG + SVM by default)
        self.car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')
        
    def detect_vehicles(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply some image processing to improve detection
        # 1. Gaussian blur to reduce noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 2. Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blur)
        
        # Detect vehicles in the frame with optimized parameters
        vehicles = self.car_cascade.detectMultiScale(
            enhanced,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Filter out false positives based on size constraints
        filtered_vehicles = []
        for (x, y, w, h) in vehicles:
            aspect_ratio = float(w) / h
            if 0.7 <= aspect_ratio <= 2.0:  # Common aspect ratios for vehicles
                filtered_vehicles.append((x, y, w, h))
        
        return filtered_vehicles
        
    def draw_detections(self, frame, vehicles):
        # Create a copy of the frame to avoid modifying the original
        display_frame = frame.copy()
        
        # Draw detection boxes and add information
        for (x, y, w, h) in vehicles:
            # Draw filled rectangle with transparency
            overlay = display_frame.copy()
            cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 255, 0), -1)
            display_frame = cv2.addWeighted(overlay, 0.2, display_frame, 0.8, 0)
            
            # Draw border
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw center point
            center_x = x + w//2
            center_y = y + h//2
            cv2.circle(display_frame, (center_x, center_y), 3, (0, 0, 255), -1)
        
        return display_frame
