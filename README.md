# Hệ thống Phân tích và Gợi ý Thời gian Đèn giao thông - Ngã 4
# Smart Traffic Light Timing Analysis & Recommendation System - 4-Way Intersection

## Tính năng chính

- **Phát hiện xe cộ** sử dụng OpenCV và Haar Cascade
- **Phân tích mật độ giao thông** theo thời gian thực cho 4 hướng
- **Đếm thời gian đèn xanh + vàng** hiện tại cho từng pha
- **So sánh mật độ xe** giữa 4 hướng (Bắc, Nam, Đông, Tây)
- **Gợi ý thời gian đèn hợp lý** dựa trên phân tích AI cho ngã 4
- **Giao diện người dùng** hiển thị 4 video song song và phân tích chi tiết
- **Ghi log và thống kê** để phân tích xu hướng

## Cấu trúc dự án

```
STL/
├── src/
│   ├── main.py              # Điểm khởi đầu ứng dụng chính
│   ├── vehicle_detector.py  # Phát hiện xe cộ
│   ├── traffic_analyzer.py  # Phân tích giao thông và gợi ý thời gian đèn ngã 4
│   ├── traffic_logger.py    # Ghi log và thống kê cho 4 hướng
│   └── gui.py               # Giao diện người dùng với 4 video
├── config.json              # Cấu hình hệ thống ngã 4
├── requirements.txt         # Thư viện cần thiết
└── data/                    # Thư mục chứa 4 video giao thông
    ├── north.mp4           # Video hướng Bắc
    ├── south.mp4           # Video hướng Nam
    ├── east.mp4            # Video hướng Đông
    └── west.mp4            # Video hướng Tây
```

## Yêu cầu hệ thống

- Python 3.x
- OpenCV (opencv-python)
- NumPy
- Pandas

## Cài đặt

1. Đảm bảo Python đã được cài đặt trên hệ thống
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## Sử dụng

1. Chạy ứng dụng chính:
   ```bash
   python src/main.py
   ```

2. Đặt 4 video giao thông vào thư mục `data/` và cập nhật đường dẫn trong `config.json`:
   ```json
   "video_sources": {
       "north": "data/north.mp4",    # Hướng Bắc
       "south": "data/south.mp4",    # Hướng Nam
       "east": "data/east.mp4",      # Hướng Đông
       "west": "data/west.mp4"       # Hướng Tây
   }
   ```

3. Sử dụng giao diện để:
   - Xem video giao thông 4 hướng song song
   - Phân tích mật độ xe theo thời gian thực cho từng hướng
   - Xem thời gian đèn hiện tại và gợi ý tối ưu cho từng pha
   - Đọc các khuyến nghị điều chỉnh thời gian đèn dựa trên phân tích ngã 4

4. Nhấn 'q' để thoát ứng dụng

## Cấu hình

Bạn có thể điều chỉnh các tham số sau trong `config.json`:

- **`density_threshold`**: Ngưỡng mật độ để xác định ùn tắc
- **`analysis_interval`**: Khoảng thời gian phân tích (giây)
- **`total_cycle_time`**: Tổng thời gian chu kỳ đèn giao thông
- **`min_green_time`**: Thời gian đèn xanh tối thiểu
- **`yellow_time`**: Thời gian đèn vàng
- **`phases`**: Cấu hình pha đèn giao thông (Bắc-Nam và Đông-Tây)

## Cách hoạt động

1. **Phát hiện xe**: Sử dụng Haar Cascade để nhận diện xe cộ trong 4 video
2. **Tính mật độ**: Dựa trên số lượng và kích thước xe phát hiện được cho từng hướng
3. **Phân tích pha đèn**: Theo dõi thời gian đèn xanh + vàng cho từng pha
4. **So sánh mật độ**: Đánh giá mật độ giao thông giữa 4 hướng
5. **Đưa ra gợi ý**: Dựa trên mật độ giao thông và hiệu suất hiện tại
6. **Ghi log**: Lưu trữ dữ liệu để phân tích xu hướng dài hạn

## Pha đèn giao thông

Hệ thống sử dụng 2 pha đèn giao thông:

- **Pha 1**: Đèn xanh cho hướng **Bắc-Nam** (cùng lúc)
- **Pha 2**: Đèn xanh cho hướng **Đông-Tây** (cùng lúc)

Thời gian mỗi pha được tối ưu hóa dựa trên mật độ giao thông thực tế.

## Ứng dụng

- **Quy hoạch giao thông**: Phân tích lưu lượng ngã 4 để tối ưu hóa thời gian đèn
- **Nghiên cứu**: Thu thập dữ liệu giao thông đa hướng để nghiên cứu
- **Giảng dạy**: Học về Computer Vision và AI trong giao thông phức tạp
- **Đánh giá hiệu quả**: So sánh hiệu suất của các cài đặt đèn giao thông khác nhau
- **Quản lý đô thị**: Tối ưu hóa giao thông tại các ngã tư quan trọng

---

## Key Features

- **Vehicle Detection** using OpenCV and Haar Cascade
- **Real-time Traffic Density Analysis** for 4 directions
- **Current Green + Yellow Light Timing** monitoring for each phase
- **Vehicle Density Comparison** between 4 directions (North, South, East, West)
- **AI-based Traffic Light Timing Recommendations** for 4-way intersection
- **User Interface** displaying 4 parallel videos and detailed analysis
- **Logging and Statistics** for trend analysis

## Project Structure

```
STL/
├── src/
│   ├── main.py              # Main application entry point
│   ├── vehicle_detector.py  # Vehicle detection
│   ├── traffic_analyzer.py  # Traffic analysis and timing recommendations for 4-way intersection
│   ├── traffic_logger.py    # Logging and statistics for 4 directions
│   └── gui.py               # User interface with 4 videos
├── config.json              # 4-way intersection system configuration
├── requirements.txt         # Required libraries
└── data/                    # Directory containing 4 traffic videos
    ├── north.mp4           # North direction video
    ├── south.mp4           # South direction video
    ├── east.mp4            # East direction video
    └── west.mp4            # West direction video
```

## System Requirements

- Python 3.x
- OpenCV (opencv-python)
- NumPy
- Pandas

## Installation

1. Ensure Python is installed on your system
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```bash
   python src/main.py
   ```

2. Place 4 traffic videos in the `data/` directory and update paths in `config.json`:
   ```json
   "video_sources": {
       "north": "data/north.mp4",    # North direction
       "south": "data/south.mp4",    # South direction
       "east": "data/east.mp4",      # East direction
       "west": "data/west.mp4"       # West direction
   }
   ```

3. Use the interface to:
   - View 4-direction traffic videos in parallel
   - Analyze real-time vehicle density for each direction
   - Monitor current light timing and optimal suggestions for each phase
   - Read timing adjustment recommendations based on 4-way intersection analysis

4. Press 'q' to exit the application

## Configuration

You can adjust the following parameters in `config.json`:

- **`density_threshold`**: Density threshold for determining congestion
- **`analysis_interval`**: Analysis time interval (seconds)
- **`total_cycle_time`**: Total traffic light cycle time
- **`min_green_time`**: Minimum green light time
- **`yellow_time`**: Yellow light time
- **`phases`**: Traffic light phase configuration (North-South and East-West)

## How It Works

1. **Vehicle Detection**: Use Haar Cascade to identify vehicles in 4 videos
2. **Density Calculation**: Based on detected vehicle count and size for each direction
3. **Light Phase Analysis**: Monitor green + yellow light timing for each phase
4. **Density Comparison**: Evaluate traffic density across 4 directions
5. **Recommendations**: Based on current traffic density and performance
6. **Logging**: Store data for long-term trend analysis

## Traffic Light Phases

The system uses 2 traffic light phases:

- **Phase 1**: Green light for **North-South** directions (simultaneously)
- **Phase 2**: Green light for **East-West** directions (simultaneously)

Each phase timing is optimized based on actual traffic density.

## Applications

- **Traffic Planning**: Analyze 4-way intersection flow to optimize light timing
- **Research**: Collect multi-directional traffic data for research
- **Education**: Learn about Computer Vision and AI in complex traffic scenarios
- **Performance Evaluation**: Compare effectiveness of different traffic light settings
- **Urban Management**: Optimize traffic at important intersections

## Notes

- **Video Files**: Place your traffic videos in the `data/` folder
- **Webcam Alternative**: You can modify `config.json` to use webcam (set to "0") for testing
- **Performance**: The system may experience lag with 4 simultaneous video streams
- **Logs**: Check `traffic_analysis.log` and `traffic_stats.csv` for detailed analysis
