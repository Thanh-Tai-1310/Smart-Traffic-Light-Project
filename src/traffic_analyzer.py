import numpy as np
import time

class TrafficAnalyzer:
    def __init__(self):
        # Initialize for 4 directions
        self.directions = ['north', 'south', 'east', 'west']
        self.traffic_density = {direction: 0 for direction in self.directions}
        self.vehicle_counts = {direction: 0 for direction in self.directions}
        
        # Traffic light phases for 4-way intersection
        self.phases = {
            'phase1': ['north', 'south'],  # North-South green
            'phase2': ['east', 'west']     # East-West green
        }
        
        # Current signal times for each direction
        self.current_signal_times = {direction: 30 for direction in self.directions}
        self.density_threshold = 0.3
        
        # Traffic light state
        self.current_phase = 'phase1'
        self.last_signal_change = time.time()
        
        # Timing analysis for 4 directions
        self.timing_analysis = {
            direction: {'green_time': 30, 'yellow_time': 3, 'total_cycle': 0} 
            for direction in self.directions
        }
        self.analysis_history = []
        
    def calculate_density(self, vehicles, direction, frame):
        """Calculate traffic density based on number and size of detected vehicles"""
        height, width, _ = frame.shape
        frame_area = width * height
        if len(vehicles) > 0:
            total_vehicle_area = sum(w * h for (_, _, w, h) in vehicles)
            density = total_vehicle_area / frame_area
        else:
            density = 0.0
        
        self.traffic_density[direction] = density
        self.vehicle_counts[direction] = len(vehicles)
        return density

    def is_congested(self, direction):
        """Determine if traffic is congested based on density"""
        return self.traffic_density[direction] > self.density_threshold
    
    def get_phase_density(self, phase):
        """Get combined density for a specific phase"""
        phase_directions = self.phases[phase]
        total_density = sum(self.traffic_density[direction] for direction in phase_directions)
        return total_density
    
    def analyze_current_timing(self):
        """Analyze current traffic light timing performance"""
        current_time = time.time()
        elapsed_time = current_time - self.last_signal_change
        
        # Calculate current phase time
        current_phase_directions = self.phases[self.current_phase]
        current_phase_time = max(
            self.timing_analysis[direction]['green_time'] + self.timing_analysis[direction]['yellow_time']
            for direction in current_phase_directions
        )
        
        return {
            'current_phase': self.current_phase,
            'current_directions': current_phase_directions,
            'elapsed_time': elapsed_time,
            'current_phase_time': current_phase_time,
            'time_remaining': max(0, current_phase_time - elapsed_time)
        }
    
    def calculate_optimal_timing(self):
        """Calculate optimal signal timing based on traffic density comparison for 4-way intersection"""
        total_cycle_time = 120  # Total cycle time in seconds
        min_green_time = 20    # Minimum green time for any phase
        yellow_time = 3        # Yellow time
        
        # Calculate density for each phase
        phase1_density = self.get_phase_density('phase1')  # North-South
        phase2_density = self.get_phase_density('phase2')  # East-West
        
        total_density = phase1_density + phase2_density
        if total_density == 0:
            return {direction: 30 for direction in self.directions}
        
        # Calculate optimal timing for each phase
        phase1_time = max(
            min_green_time,
            int((phase1_density / total_density) * (total_cycle_time - 2 * yellow_time))
        )
        phase2_time = max(
            min_green_time,
            total_cycle_time - phase1_time - 2 * yellow_time
        )
        
        # Distribute time among directions in each phase
        optimal_times = {}
        for direction in self.directions:
            if direction in self.phases['phase1']:
                optimal_times[direction] = phase1_time
            else:
                optimal_times[direction] = phase2_time
                
        return optimal_times
    
    def get_timing_recommendation(self):
        """Generate detailed recommendations based on current and optimal timings for 4-way intersection"""
        optimal_times = self.calculate_optimal_timing()
        current_analysis = self.analyze_current_timing()
        
        recommendations = []
        
        # Compare current vs optimal timing for each direction
        for direction in self.directions:
            current_time = self.current_signal_times[direction]
            optimal_time = optimal_times[direction]
            
            if abs(current_time - optimal_time) >= 5:  # If difference is significant
                if current_time < optimal_time:
                    recommendations.append(
                        f"Tăng thời gian đèn xanh cho hướng {direction} từ {current_time}s lên {optimal_time}s"
                    )
                else:
                    recommendations.append(
                        f"Giảm thời gian đèn xanh cho hướng {direction} từ {current_time}s xuống {optimal_time}s"
                    )
        
        # Add phase-based insights
        phase1_density = self.get_phase_density('phase1')
        phase2_density = self.get_phase_density('phase2')
        
        if phase1_density > phase2_density:
            recommendations.append("Hướng Bắc-Nam có mật độ xe cao hơn - cần tăng thời gian đèn xanh")
        elif phase2_density > phase1_density:
            recommendations.append("Hướng Đông-Tây có mật độ xe cao hơn - cần tăng thời gian đèn xanh")
        else:
            recommendations.append("Mật độ xe các hướng tương đương - thời gian đèn hiện tại phù hợp")
        
        # Add congestion warnings for each direction
        for direction in self.directions:
            if self.is_congested(direction):
                recommendations.append(f"⚠️ Hướng {direction} đang bị ùn tắc - cần tăng thời gian đèn xanh ngay lập tức")
        
        return recommendations if recommendations else ["Thời gian đèn hiện tại đang tối ưu"]
    
    def get_traffic_status(self):
        """Get current traffic status for display"""
        current_analysis = self.analyze_current_timing()
        
        return {
            'densities': self.traffic_density,
            'vehicle_counts': self.vehicle_counts,
            'current_phase': self.current_phase,
            'current_directions': current_analysis['current_directions'],
            'time_remaining': current_analysis['time_remaining'],
            'current_phase_time': current_analysis['current_phase_time'],
            'elapsed_time': current_analysis['elapsed_time']
        }
    
    def get_remaining_time(self):
        """Calculate remaining time for current signal"""
        current_analysis = self.analyze_current_timing()
        return current_analysis['time_remaining']
    
    def update_traffic_light(self):
        """Track traffic light changes (for analysis purposes)"""
        current_time = time.time()
        elapsed_time = current_time - self.last_signal_change
        
        current_phase_directions = self.phases[self.current_phase]
        current_phase_time = max(
            self.timing_analysis[direction]['green_time'] + self.timing_analysis[direction]['yellow_time']
            for direction in current_phase_directions
        )
        
        if elapsed_time >= current_phase_time:
            # Switch to next phase
            if self.current_phase == 'phase1':
                self.current_phase = 'phase2'
            else:
                self.current_phase = 'phase1'
            self.last_signal_change = current_time
            return True
            
        return False
    
    def get_timing_comparison(self):
        """Get comparison between current and suggested timing"""
        optimal_times = self.calculate_optimal_timing()
        
        return {
            'current': self.current_signal_times,
            'suggested': optimal_times,
            'differences': {
                direction: optimal_times[direction] - self.current_signal_times[direction]
                for direction in self.directions
            }
        }
    
    def get_intersection_summary(self):
        """Get summary of intersection traffic status"""
        total_vehicles = sum(self.vehicle_counts.values())
        total_density = sum(self.traffic_density.values())
        congested_directions = [direction for direction in self.directions if self.is_congested(direction)]
        
        return {
            'total_vehicles': total_vehicles,
            'total_density': total_density,
            'congested_directions': congested_directions,
            'busiest_direction': max(self.directions, key=lambda d: self.traffic_density[d]),
            'least_busy_direction': min(self.directions, key=lambda d: self.traffic_density[d])
        }
