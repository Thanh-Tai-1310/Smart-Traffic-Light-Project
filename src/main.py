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
        
        # Initialize video captures for 4 directions
        self.cap_north = None
        self.cap_south = None
        self.cap_east = None
        self.cap_west = None
        self.is_running = False
        
        # Set up GUI callbacks
        self.gui.process_video = self.process_video
        
    def init_video_captures(self):
        """Initialize video captures for 4 directions with error handling"""
        try:
            # Get video paths from config
            video_paths = {
                'north': self.config['video_sources']['north'],
                'south': self.config['video_sources']['south'],
                'east': self.config['video_sources']['east'],
                'west': self.config['video_sources']['west']
            }
            
            # Check if video files exist
            for direction, path in video_paths.items():
                if not os.path.exists(path):
                    print(f"Error: Video file not found for {direction}: {path}")
                    return False
            
            # Initialize video captures
            self.cap_north = cv2.VideoCapture(video_paths['north'])
            self.cap_south = cv2.VideoCapture(video_paths['south'])
            self.cap_east = cv2.VideoCapture(video_paths['east'])
            self.cap_west = cv2.VideoCapture(video_paths['west'])
            
            # Check if videos opened successfully
            captures = [self.cap_north, self.cap_south, self.cap_east, self.cap_west]
            directions = ['north', 'south', 'east', 'west']
            
            for i, cap in enumerate(captures):
                if not cap.isOpened():
                    print(f"Error: Could not open {directions[i]} video. The file might be corrupted.")
                    # Release all captures
                    for j in range(i):
                        captures[j].release()
                    return False
                    
            return True
            
        except Exception as e:
            print(f"Error initializing video captures: {str(e)}")
            # Release any opened captures
            for cap in [self.cap_north, self.cap_south, self.cap_east, self.cap_west]:
                if cap is not None:
                    cap.release()
            return False
        
    def process_video(self):
        """Main video processing loop for 4-way intersection"""
        if not self.init_video_captures():
            return
            
        last_analysis_time = time.time()
        analysis_interval = self.config['analysis']['analysis_interval']
        
        try:
            while self.is_running and not self.gui.is_paused:
                # Read frames from all 4 directions
                ret_north, frame_north = self.cap_north.read()
                ret_south, frame_south = self.cap_south.read()
                ret_east, frame_east = self.cap_east.read()
                ret_west, frame_west = self.cap_west.read()
                
                # Check if any frame failed to read
                if not all([ret_north, ret_south, ret_east, ret_west]):
                    # Reset videos to start
                    self.cap_north.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.cap_south.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.cap_east.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.cap_west.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Detect vehicles in all directions
                vehicles_north = self.detector.detect_vehicles(frame_north)
                vehicles_south = self.detector.detect_vehicles(frame_south)
                vehicles_east = self.detector.detect_vehicles(frame_east)
                vehicles_west = self.detector.detect_vehicles(frame_west)
                
                # Calculate density for all directions
                self.analyzer.calculate_density(vehicles_north, 'north', frame_north)
                self.analyzer.calculate_density(vehicles_south, 'south', frame_south)
                self.analyzer.calculate_density(vehicles_east, 'east', frame_east)
                self.analyzer.calculate_density(vehicles_west, 'west', frame_west)
                
                # Update traffic light status (for analysis purposes)
                self.analyzer.update_traffic_light()
                
                # Get current status
                status = self.analyzer.get_traffic_status()
                
                # Get timing analysis and recommendations
                timing_comparison = self.analyzer.get_timing_comparison()
                recommendations = self.analyzer.get_timing_recommendation()
                
                # Log and analyze periodically
                current_time = time.time()
                if current_time - last_analysis_time >= analysis_interval:
                    self.logger.log_traffic_status(status)
                    self.logger.log_recommendation(recommendations)
                    self.logger.log_timing_analysis(timing_comparison)
                    last_analysis_time = current_time
                
                # Draw detections on all frames
                frame_north = self.detector.draw_detections(frame_north, vehicles_north)
                frame_south = self.detector.draw_detections(frame_south, vehicles_south)
                frame_east = self.detector.draw_detections(frame_east, vehicles_east)
                frame_west = self.detector.draw_detections(frame_west, vehicles_west)
                
                # Prepare frames dict for GUI
                frames = {
                    'north': frame_north,
                    'south': frame_south,
                    'east': frame_east,
                    'west': frame_west
                }
                
                # Update GUI with comprehensive information
                self.gui.update_frame(frames)
                self.gui.update_stats(status)
                self.gui.update_suggested_timing(timing_comparison['suggested'])
                self.gui.update_recommendations(recommendations)
                
                # Control playback speed
                delay = int(30 / self.gui.speed_scale.get())
                time.sleep(max(1, delay) / 1000)
                
        finally:
            # Clean up all video captures
            for cap in [self.cap_north, self.cap_south, self.cap_east, self.cap_west]:
                if cap is not None:
                    cap.release()
            self.logger.save_statistics()
            
    def run(self):
        """Start the application"""
        self.is_running = True
        self.gui.run()

if __name__ == '__main__':
    app = TrafficControlApp()
    app.run()
