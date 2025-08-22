import cv2
import time
from vehicle_detector import VehicleDetector
from traffic_analyzer import TrafficAnalyzer

def main():
    # Initialize video captures for both roads
    cap_road1 = cv2.VideoCapture(0)  # Camera for road 1
    cap_road2 = cv2.VideoCapture(1)  # Camera for road 2
    
    # Initialize detector and analyzer
    detector = VehicleDetector()
    analyzer = TrafficAnalyzer()
    
    # Initialize timing variables
    last_analysis_time = time.time()
    analysis_interval = 60  # Analyze every 60 seconds
    
    try:
        while True:
            # Read frames from both cameras
            ret1, frame1 = cap_road1.read()
            ret2, frame2 = cap_road2.read()
            
            if not ret1 or not ret2:
                print("Error reading from cameras")
                break
            
            # Detect vehicles in both roads
            vehicles_road1 = detector.detect_vehicles(frame1)
            vehicles_road2 = detector.detect_vehicles(frame2)
            
            # Calculate density for both roads
            density_road1 = analyzer.calculate_density(vehicles_road1, 'road_1', frame1)
            density_road2 = analyzer.calculate_density(vehicles_road2, 'road_2', frame2)
            
            # Update traffic light status
            light_changed = analyzer.update_traffic_light()
            
            # Get current traffic status
            status = analyzer.get_traffic_status()
            
            # Analyze traffic and get recommendations periodically
            current_time = time.time()
            if current_time - last_analysis_time >= analysis_interval:
                recommendations = analyzer.get_timing_recommendation()
                print("\n=== Traffic Analysis ===")
                print(f"Road 1: {status['vehicle_counts']['road_1']} vehicles (density: {status['densities']['road_1']:.3f})")
                print(f"Road 2: {status['vehicle_counts']['road_2']} vehicles (density: {status['densities']['road_2']:.3f})")
                print("\nRecommendations:")
                for rec in recommendations:
                    print(f"- {rec}")
                last_analysis_time = current_time
            
            # Draw vehicle detections and status information
            for road_id, frame in [('road_1', frame1), ('road_2', frame2)]:
                vehicles = vehicles_road1 if road_id == 'road_1' else vehicles_road2
                frame = detector.draw_detections(frame, vehicles)
                
                # Add traffic light status
                light_color = (0, 255, 0) if road_id == status['current_green'] else (0, 0, 255)
                cv2.circle(frame, (30, 30), 20, light_color, -1)
                
                # Add information
                cv2.putText(frame, f'Vehicles: {status["vehicle_counts"][road_id]}', (60, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f'Density: {status["densities"][road_id]:.2f}', (60, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                if road_id == status['current_green']:
                    cv2.putText(frame, f'Time: {int(status["time_remaining"])}s', (60, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show frames
            cv2.imshow('Road 1', frame1)
            cv2.imshow('Road 2', frame2)
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Clean up
        cap_road1.release()
        cap_road2.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
