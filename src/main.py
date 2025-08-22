import cv2
from vehicle_detector import VehicleDetector
from traffic_analyzer import TrafficAnalyzer

def main():
    # Initialize video capture (0 for webcam, or provide video file path)
    cap = cv2.VideoCapture(0)
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize detector and analyzer
    detector = VehicleDetector()
    analyzer = TrafficAnalyzer(frame_width, frame_height)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Detect vehicles
        vehicles = detector.detect_vehicles(frame)
        
        # Analyze traffic
        vehicle_count = analyzer.update_vehicle_count(vehicles)
        density = analyzer.calculate_density(vehicles)
        is_congested = analyzer.is_congested(density)
        
        # Draw vehicle detections
        frame = detector.draw_detections(frame, vehicles)
        
        # Display information on frame
        cv2.putText(frame, f'Vehicles: {vehicle_count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Density: {density:.2f}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Congested: {is_congested}', (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Traffic Monitoring', frame)
        
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
