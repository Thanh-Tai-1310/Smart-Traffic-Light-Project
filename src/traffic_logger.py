import logging
import pandas as pd
from datetime import datetime
import os
import json

class TrafficLogger:
    def __init__(self, config_file='config.json'):
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Set up logging
        if self.config['logging']['enabled']:
            logging.basicConfig(
                filename=self.config['logging']['log_file'],
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        
        # Initialize statistics storage
        self.stats = []
        
    def log_traffic_status(self, status):
        """Log traffic status and statistics for 4-way intersection"""
        timestamp = datetime.now()
        
        # Create statistics record for 4 directions
        record = {
            'timestamp': timestamp,
            'north_density': status['densities']['north'],
            'south_density': status['densities']['south'],
            'east_density': status['densities']['east'],
            'west_density': status['densities']['west'],
            'north_vehicles': status['vehicle_counts']['north'],
            'south_vehicles': status['vehicle_counts']['south'],
            'east_vehicles': status['vehicle_counts']['east'],
            'west_vehicles': status['vehicle_counts']['west'],
            'current_phase': status['current_phase'],
            'current_directions': '-'.join(status['current_directions']),
            'time_remaining': status['time_remaining'],
            'current_phase_time': status.get('current_phase_time', 0),
            'elapsed_time': status.get('elapsed_time', 0)
        }
        
        # Add to statistics
        self.stats.append(record)
        
        # Log to file if enabled
        if self.config['logging']['enabled']:
            logging.info(f"=== PHÂN TÍCH NGÃ 4 GIAO THÔNG - {timestamp} ===")
            logging.info(f"Hướng Bắc: {status['vehicle_counts']['north']} xe (mật độ: {status['densities']['north']:.3f})")
            logging.info(f"Hướng Nam: {status['vehicle_counts']['south']} xe (mật độ: {status['densities']['south']:.3f})")
            logging.info(f"Hướng Đông: {status['vehicle_counts']['east']} xe (mật độ: {status['densities']['east']:.3f})")
            logging.info(f"Hướng Tây: {status['vehicle_counts']['west']} xe (mật độ: {status['densities']['west']:.3f})")
            logging.info(f"Pha hiện tại: {status['current_phase']} ({'-'.join(status['current_directions'])})")
            logging.info(f"Thời gian còn lại: {int(status['time_remaining'])}s")
            logging.info(f"Thời gian pha hiện tại: {status.get('current_phase_time', 0)}s")
            logging.info(f"Thời gian đã trôi: {status.get('elapsed_time', 0):.1f}s")
    
    def log_recommendation(self, recommendations):
        """Log timing recommendations"""
        if self.config['logging']['enabled']:
            logging.info("=== GỢI Ý ĐIỀU CHỈNH THỜI GIAN ĐÈN NGÃ 4 ===")
            for rec in recommendations:
                logging.info(f"• {rec}")
            logging.info("=" * 50)
    
    def log_timing_analysis(self, timing_comparison):
        """Log timing analysis comparison for 4-way intersection"""
        if self.config['logging']['enabled']:
            logging.info("=== PHÂN TÍCH THỜI GIAN ĐÈN NGÃ 4 ===")
            logging.info(f"Thời gian hiện tại:")
            logging.info(f"  - Hướng Bắc: {timing_comparison['current']['north']}s")
            logging.info(f"  - Hướng Nam: {timing_comparison['current']['south']}s")
            logging.info(f"  - Hướng Đông: {timing_comparison['current']['east']}s")
            logging.info(f"  - Hướng Tây: {timing_comparison['current']['west']}s")
            logging.info(f"Thời gian gợi ý:")
            logging.info(f"  - Hướng Bắc: {timing_comparison['suggested']['north']}s")
            logging.info(f"  - Hướng Nam: {timing_comparison['suggested']['south']}s")
            logging.info(f"  - Hướng Đông: {timing_comparison['suggested']['east']}s")
            logging.info(f"  - Hướng Tây: {timing_comparison['suggested']['west']}s")
            logging.info(f"Chênh lệch:")
            logging.info(f"  - Hướng Bắc: {timing_comparison['differences']['north']:+d}s")
            logging.info(f"  - Hướng Nam: {timing_comparison['differences']['south']:+d}s")
            logging.info(f"  - Hướng Đông: {timing_comparison['differences']['east']:+d}s")
            logging.info(f"  - Hướng Tây: {timing_comparison['differences']['west']:+d}s")
    
    def save_statistics(self):
        """Save collected statistics to CSV file"""
        if self.config['logging']['save_statistics'] and self.stats:
            df = pd.DataFrame(self.stats)
            df.to_csv(self.config['logging']['statistics_file'], index=False)
            if self.config['logging']['enabled']:
                logging.info(f"Thống kê đã được lưu vào {self.config['logging']['statistics_file']}")
    
    def generate_report(self):
        """Generate a summary report from collected statistics for 4-way intersection"""
        if not self.stats:
            return "Không có dữ liệu thống kê"
            
        df = pd.DataFrame(self.stats)
        
        report = "BÁO CÁO PHÂN TÍCH NGÃ 4 GIAO THÔNG\n"
        report += "=" * 50 + "\n"
        report += f"Thời gian: {df['timestamp'].min()} đến {df['timestamp'].max()}\n\n"
        
        # Average densities for all directions
        report += "Mật độ giao thông trung bình:\n"
        report += f"Hướng Bắc: {df['north_density'].mean():.3f}\n"
        report += f"Hướng Nam: {df['south_density'].mean():.3f}\n"
        report += f"Hướng Đông: {df['east_density'].mean():.3f}\n"
        report += f"Hướng Tây: {df['west_density'].mean():.3f}\n\n"
        
        # Peak traffic times for all directions
        report += "Thời điểm giao thông cao điểm:\n"
        peak_north = df.loc[df['north_density'].idxmax()]
        peak_south = df.loc[df['south_density'].idxmax()]
        peak_east = df.loc[df['east_density'].idxmax()]
        peak_west = df.loc[df['west_density'].idxmax()]
        
        report += f"Hướng Bắc: {peak_north['timestamp']} (mật độ: {peak_north['north_density']:.3f})\n"
        report += f"Hướng Nam: {peak_south['timestamp']} (mật độ: {peak_south['south_density']:.3f})\n"
        report += f"Hướng Đông: {peak_east['timestamp']} (mật độ: {peak_east['east_density']:.3f})\n"
        report += f"Hướng Tây: {peak_west['timestamp']} (mật độ: {peak_west['west_density']:.3f})\n\n"
        
        # Total vehicle counts for all directions
        report += "Tổng số xe:\n"
        report += f"Hướng Bắc: {df['north_vehicles'].sum()}\n"
        report += f"Hướng Nam: {df['south_vehicles'].sum()}\n"
        report += f"Hướng Đông: {df['east_vehicles'].sum()}\n"
        report += f"Hướng Tây: {df['west_vehicles'].sum()}\n\n"
        
        # Traffic light analysis
        if 'current_phase_time' in df.columns:
            report += "Phân tích đèn giao thông:\n"
            report += f"Thời gian pha trung bình: {df['current_phase_time'].mean():.1f}s\n"
            report += f"Thời gian đèn xanh trung bình: {(df['current_phase_time'].mean() - 3):.1f}s\n"  # Assuming 3s yellow
            
            # Phase distribution
            if 'current_phase' in df.columns:
                phase_counts = df['current_phase'].value_counts()
                report += f"Phân bố pha: {dict(phase_counts)}\n"
        
        # Direction comparison
        total_vehicles_by_direction = {
            'Bắc': df['north_vehicles'].sum(),
            'Nam': df['south_vehicles'].sum(),
            'Đông': df['east_vehicles'].sum(),
            'Tây': df['west_vehicles'].sum()
        }
        
        busiest_direction = max(total_vehicles_by_direction, key=total_vehicles_by_direction.get)
        least_busy_direction = min(total_vehicles_by_direction, key=total_vehicles_by_direction.get)
        
        report += f"\nHướng đông nhất: {busiest_direction} ({total_vehicles_by_direction[busiest_direction]} xe)\n"
        report += f"Hướng ít đông nhất: {least_busy_direction} ({total_vehicles_by_direction[least_busy_direction]} xe)\n"
        
        return report
