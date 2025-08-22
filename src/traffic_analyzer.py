import numpy as np
import time

class TrafficAnalyzer:
    def __init__(self):
        self.traffic_density = {'road_1': 0, 'road_2': 0}
        self.vehicle_counts = {'road_1': 0, 'road_2': 0}
        self.current_signal_times = {'road_1': 30, 'road_2': 30}  # Default signal times in seconds
        self.density_threshold = 0.3  # Adjustable threshold for traffic density
        self.last_signal_change = time.time()
        self.current_green = 'road_1'  # Start with road_1 having green light
        
    def calculate_density(self, vehicles, road_id, frame):
        """Calculate traffic density based on number and size of detected vehicles"""
        height, width, _ = frame.shape
        frame_area = width * height
        total_vehicle_area = sum(w * h for (_, _, w, h) in vehicles)
        density = total_vehicle_area / frame_area
        
        self.traffic_density[road_id] = density
        self.vehicle_counts[road_id] = len(vehicles)
        return density

    def is_congested(self, road_id):
        """Determine if traffic is congested based on density"""
        return self.traffic_density[road_id] > self.density_threshold
    
    def optimize_signal_timing(self):
        """Calculate optimal signal timing based on traffic density"""
        total_cycle_time = 120  # Total cycle time in seconds
        min_green_time = 20    # Minimum green time for any road
        
        # Calculate ratio of traffic density
        total_density = self.traffic_density['road_1'] + self.traffic_density['road_2']
        if total_density == 0:
            return self.current_signal_times
            
        # Calculate new timings based on density ratio
        road_1_time = max(
            min_green_time,
            int((self.traffic_density['road_1'] / total_density) * total_cycle_time)
        )
        road_2_time = max(
            min_green_time,
            total_cycle_time - road_1_time
        )
        
        return {
            'road_1': road_1_time,
            'road_2': road_2_time
        }
    
    def get_timing_recommendation(self):
        """Generate recommendations based on current and optimal timings"""
        optimal_times = self.optimize_signal_timing()
        recommendations = []
        
        for road in ['road_1', 'road_2']:
            current_time = self.current_signal_times[road]
            optimal_time = optimal_times[road]
            
            if abs(current_time - optimal_time) >= 5:  # If difference is significant
                if current_time < optimal_time:
                    recommendations.append(
                        f"Increase {road} green time from {current_time}s to {optimal_time}s"
                    )
                else:
                    recommendations.append(
                        f"Decrease {road} green time from {current_time}s to {optimal_time}s"
                    )
        
        return recommendations if recommendations else ["Current timing is optimal"]
    
    def update_traffic_light(self):
        """Update traffic light status based on timing"""
        current_time = time.time()
        elapsed_time = current_time - self.last_signal_change
        
        if (self.current_green == 'road_1' and 
            elapsed_time >= self.current_signal_times['road_1']):
            self.current_green = 'road_2'
            self.last_signal_change = current_time
            return True
            
        elif (self.current_green == 'road_2' and 
              elapsed_time >= self.current_signal_times['road_2']):
            self.current_green = 'road_1'
            self.last_signal_change = current_time
            return True
            
        return False
    
    def get_traffic_status(self):
        """Get current traffic status for display"""
        return {
            'densities': self.traffic_density,
            'vehicle_counts': self.vehicle_counts,
            'current_green': self.current_green,
            'time_remaining': self.get_remaining_time()
        }
    
    def get_remaining_time(self):
        """Calculate remaining time for current signal"""
        elapsed_time = time.time() - self.last_signal_change
        current_cycle_time = self.current_signal_times[self.current_green]
        return max(0, current_cycle_time - elapsed_time)
