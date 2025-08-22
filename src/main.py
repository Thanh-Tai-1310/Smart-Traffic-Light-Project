import cv2
import time
import json
import os
from vehicle_detector import VehicleDetector
from traffic_analyzer import TrafficAnalyzer
from traffic_logger import TrafficLogger
from gui import TrafficControlGUI

class TrafficControlApp:
    def __init__(self):
        # Load configuration
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            
        # Initialize components
        self.detector = VehicleDetector()
        self.analyzer = TrafficAnalyzer()
        self.logger = TrafficLogger()
        self.gui = TrafficControlGUI()
        
        # Initialize video captures and other variables
        self.cap_road1 = None
        self.cap_road2 = None
        self.is_running = False
        
        # Set up GUI callbacks
        self.gui.process_video = self.process_video
        
    def init_video_captures(self):
        """Initialize video captures with error handling"""
        try:
            # Get video paths from config
            video_path1 = self.config['video_sources']['road1']
            video_path2 = self.config['video_sources']['road2']
            
            # Check if video files exist
            if not os.path.exists(video_path1):
                print(f"Error: Video file not found: {video_path1}")
                return False
            if not os.path.exists(video_path2):
                print(f"Error: Video file not found: {video_path2}")
                return False
            
            # Initialize video captures
            self.cap_road1 = cv2.VideoCapture(video_path1)
            self.cap_road2 = cv2.VideoCapture(video_path2)
            
            # Check if videos opened successfully
            if not self.cap_road1.isOpened():
                print(f"Error: Could not open {video_path1}. The file might be corrupted.")
                return False
            if not self.cap_road2.isOpened():
                self.cap_road1.release()
                print(f"Error: Could not open {video_path2}. The file might be corrupted.")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error initializing video captures: {str(e)}")
            if hasattr(self, 'cap_road1') and self.cap_road1 is not None:
                self.cap_road1.release()
            if hasattr(self, 'cap_road2') and self.cap_road2 is not None:
                self.cap_road2.release()
            return False
        
    def process_video(self):
        """Main video processing loop"""
        if not self.init_video_captures():
            return
            
        last_analysis_time = time.time()
        analysis_interval = self.config['analysis']['analysis_interval']
        
        try:
            while self.is_running and not self.gui.is_paused:
                # Read frames
                ret1, frame1 = self.cap_road1.read()
                ret2, frame2 = self.cap_road2.read()
                
                if not ret1 or not ret2:
                    # Reset videos to start
                    self.cap_road1.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.cap_road2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Detect vehicles
                vehicles_road1 = self.detector.detect_vehicles(frame1)
                vehicles_road2 = self.detector.detect_vehicles(frame2)
                
                # Calculate density
                self.analyzer.calculate_density(vehicles_road1, 'road_1', frame1)
                self.analyzer.calculate_density(vehicles_road2, 'road_2', frame2)
                
                # Update traffic light status
                self.analyzer.update_traffic_light()
                
                # Get current status
                status = self.analyzer.get_traffic_status()
                
                # Log and analyze periodically
                current_time = time.time()
                if current_time - last_analysis_time >= analysis_interval:
                    recommendations = self.analyzer.get_timing_recommendation()
                    self.logger.log_traffic_status(status)
                    self.logger.log_recommendation(recommendations)
                    last_analysis_time = current_time
                
                # Draw detections
                frame1 = self.detector.draw_detections(frame1, vehicles_road1)
                frame2 = self.detector.draw_detections(frame2, vehicles_road2)
                
                # Update GUI
                self.gui.update_frame(frame1, frame2)
                self.gui.update_stats(status)
                
                # Control playback speed
                delay = int(30 / self.gui.speed_scale.get())
                time.sleep(max(1, delay) / 1000)
                
        finally:
            # Clean up
            self.cap_road1.release()
            self.cap_road2.release()
            self.logger.save_statistics()
            
    def run(self):
        """Start the application"""
        self.is_running = True
        self.gui.run()

if __name__ == '__main__':
    app = TrafficControlApp()
    app.run()
