import numpy as np

class TrafficAnalyzer:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.vehicle_count = 0
        self.density_threshold = 0.3  # Adjustable threshold for traffic density
        
    def calculate_density(self, vehicles):
        """Calculate traffic density based on number and size of detected vehicles"""
        total_vehicle_area = sum(w * h for (_, _, w, h) in vehicles)
        frame_area = self.frame_width * self.frame_height
        density = total_vehicle_area / frame_area
        return density
        
    def is_congested(self, density):
        """Determine if traffic is congested based on density"""
        return density > self.density_threshold
        
    def update_vehicle_count(self, vehicles):
        """Update the count of vehicles"""
        self.vehicle_count = len(vehicles)
        return self.vehicle_count
