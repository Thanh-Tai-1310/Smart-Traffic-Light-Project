import tkinter as tk
from tkinter import ttk
import cv2
import json
import threading
import queue
import numpy as np

class TrafficControlGUI:
    def __init__(self, config_file='config.json'):
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = json.load(f)
            
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Phân tích và Gợi ý Thời gian Đèn giao thông - Ngã 4")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create frames
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.analysis_frame = ttk.Frame(self.root)
        self.analysis_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky='nsew')
        
        # Configure grid weights
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create video displays in 2x2 grid
        self.create_video_grid()
        
        # Create control buttons
        self.create_controls()
        
        # Create analysis display
        self.create_analysis_display()
        
        # Initialize variables
        self.is_running = False
        self.is_paused = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.status_queue = queue.Queue(maxsize=10)
        
    def create_video_grid(self):
        """Create 2x2 grid of video displays for 4 directions"""
        # North video (top)
        self.video_label_north = ttk.Label(self.video_frame, text="Hướng Bắc", font=('Arial', 10, 'bold'))
        self.video_label_north.grid(row=0, column=1, padx=5, pady=5)
        
        # South video (bottom)
        self.video_label_south = ttk.Label(self.video_frame, text="Hướng Nam", font=('Arial', 10, 'bold'))
        self.video_label_south.grid(row=2, column=1, padx=5, pady=5)
        
        # East video (right)
        self.video_label_east = ttk.Label(self.video_frame, text="Hướng Đông", font=('Arial', 10, 'bold'))
        self.video_label_east.grid(row=1, column=2, padx=5, pady=5)
        
        # West video (left)
        self.video_label_west = ttk.Label(self.video_frame, text="Hướng Tây", font=('Arial', 10, 'bold'))
        self.video_label_west.grid(row=1, column=0, padx=5, pady=5)
        
        # Center intersection indicator
        center_label = ttk.Label(self.video_frame, text="⛔", font=('Arial', 20))
        center_label.grid(row=1, column=1, padx=5, pady=5)
        
    def create_controls(self):
        """Create control buttons and sliders"""
        # Playback controls
        ttk.Button(self.control_frame, text="Bắt đầu", command=self.start).grid(row=0, column=0, padx=5)
        ttk.Button(self.control_frame, text="Tạm dừng/Tiếp tục", command=self.toggle_pause).grid(row=0, column=1, padx=5)
        ttk.Button(self.control_frame, text="Dừng", command=self.stop).grid(row=0, column=2, padx=5)
        
        # Speed control
        ttk.Label(self.control_frame, text="Tốc độ phát:").grid(row=1, column=0, padx=5)
        self.speed_scale = ttk.Scale(self.control_frame, from_=0.25, to=2.0, orient=tk.HORIZONTAL)
        self.speed_scale.set(1.0)
        self.speed_scale.grid(row=1, column=1, columnspan=2, padx=5, sticky='ew')
        
    def create_analysis_display(self):
        """Create traffic light timing analysis display for 4-way intersection"""
        # Title
        title_label = ttk.Label(self.analysis_frame, text="PHÂN TÍCH NGÃ 4 GIAO THÔNG", 
                               font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Current phase section
        ttk.Label(self.analysis_frame, text="Pha đèn hiện tại:", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=(10,5), sticky='w')
        
        self.current_phase_label = tk.StringVar(value="Pha 1: Bắc-Nam")
        ttk.Label(self.analysis_frame, textvariable=self.current_phase_label, 
                 foreground='green', font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, sticky='w')
        
        # Current timing section
        ttk.Label(self.analysis_frame, text="Thời gian đèn hiện tại:", 
                 font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # North current timing
        ttk.Label(self.analysis_frame, text="Hướng Bắc:").grid(row=4, column=0, sticky='w')
        self.north_current = tk.StringVar(value="30s")
        ttk.Label(self.analysis_frame, textvariable=self.north_current, foreground='green').grid(row=4, column=1, sticky='w')
        
        # South current timing
        ttk.Label(self.analysis_frame, text="Hướng Nam:").grid(row=5, column=0, sticky='w')
        self.south_current = tk.StringVar(value="30s")
        ttk.Label(self.analysis_frame, textvariable=self.south_current, foreground='green').grid(row=5, column=1, sticky='w')
        
        # East current timing
        ttk.Label(self.analysis_frame, text="Hướng Đông:").grid(row=6, column=0, sticky='w')
        self.east_current = tk.StringVar(value="30s")
        ttk.Label(self.analysis_frame, textvariable=self.east_current, foreground='green').grid(row=6, column=1, sticky='w')
        
        # West current timing
        ttk.Label(self.analysis_frame, text="Hướng Tây:").grid(row=7, column=0, sticky='w')
        self.west_current = tk.StringVar(value="30s")
        ttk.Label(self.analysis_frame, textvariable=self.west_current, foreground='green').grid(row=7, column=1, sticky='w')
        
        # Suggested timing section
        ttk.Label(self.analysis_frame, text="Thời gian đèn gợi ý:", 
                 font=('Arial', 10, 'bold')).grid(row=8, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # North suggested timing
        ttk.Label(self.analysis_frame, text="Hướng Bắc:").grid(row=9, column=0, sticky='w')
        self.north_suggested = tk.StringVar(value="--")
        ttk.Label(self.analysis_frame, textvariable=self.north_suggested, foreground='blue').grid(row=9, column=1, sticky='w')
        
        # South suggested timing
        ttk.Label(self.analysis_frame, text="Hướng Nam:").grid(row=10, column=0, sticky='w')
        self.south_suggested = tk.StringVar(value="--")
        ttk.Label(self.analysis_frame, textvariable=self.south_suggested, foreground='blue').grid(row=10, column=1, sticky='w')
        
        # East suggested timing
        ttk.Label(self.analysis_frame, text="Hướng Đông:").grid(row=11, column=0, sticky='w')
        self.east_suggested = tk.StringVar(value="--")
        ttk.Label(self.analysis_frame, textvariable=self.east_suggested, foreground='blue').grid(row=11, column=1, sticky='w')
        
        # West suggested timing
        ttk.Label(self.analysis_frame, text="Hướng Tây:").grid(row=12, column=0, sticky='w')
        self.west_suggested = tk.StringVar(value="--")
        ttk.Label(self.analysis_frame, textvariable=self.west_suggested, foreground='blue').grid(row=12, column=1, sticky='w')
        
        # Traffic density section
        ttk.Label(self.analysis_frame, text="Mật độ giao thông:", 
                 font=('Arial', 10, 'bold')).grid(row=13, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # North density
        ttk.Label(self.analysis_frame, text="Hướng Bắc:").grid(row=14, column=0, sticky='w')
        self.north_density = tk.StringVar(value="0.000")
        ttk.Label(self.analysis_frame, textvariable=self.north_density).grid(row=14, column=1, sticky='w')
        
        # South density
        ttk.Label(self.analysis_frame, text="Hướng Nam:").grid(row=15, column=0, sticky='w')
        self.south_density = tk.StringVar(value="0.000")
        ttk.Label(self.analysis_frame, textvariable=self.south_density).grid(row=15, column=1, sticky='w')
        
        # East density
        ttk.Label(self.analysis_frame, text="Hướng Đông:").grid(row=16, column=0, sticky='w')
        self.east_density = tk.StringVar(value="0.000")
        ttk.Label(self.analysis_frame, textvariable=self.east_density).grid(row=16, column=1, sticky='w')
        
        # West density
        ttk.Label(self.analysis_frame, text="Hướng Tây:").grid(row=17, column=0, sticky='w')
        self.west_density = tk.StringVar(value="0.000")
        ttk.Label(self.analysis_frame, textvariable=self.west_density).grid(row=17, column=1, sticky='w')
        
        # Vehicle counts
        ttk.Label(self.analysis_frame, text="Số lượng xe:", 
                 font=('Arial', 10, 'bold')).grid(row=18, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # North vehicles
        ttk.Label(self.analysis_frame, text="Hướng Bắc:").grid(row=19, column=0, sticky='w')
        self.north_vehicles = tk.StringVar(value="0")
        ttk.Label(self.analysis_frame, textvariable=self.north_vehicles).grid(row=19, column=1, sticky='w')
        
        # South vehicles
        ttk.Label(self.analysis_frame, text="Hướng Nam:").grid(row=20, column=0, sticky='w')
        self.south_vehicles = tk.StringVar(value="0")
        ttk.Label(self.analysis_frame, textvariable=self.south_vehicles).grid(row=20, column=1, sticky='w')
        
        # East vehicles
        ttk.Label(self.analysis_frame, text="Hướng Đông:").grid(row=21, column=0, sticky='w')
        self.east_vehicles = tk.StringVar(value="0")
        ttk.Label(self.analysis_frame, textvariable=self.east_vehicles).grid(row=21, column=1, sticky='w')
        
        # West vehicles
        ttk.Label(self.analysis_frame, text="Hướng Tây:").grid(row=22, column=0, sticky='w')
        self.west_vehicles = tk.StringVar(value="0")
        ttk.Label(self.analysis_frame, textvariable=self.west_vehicles).grid(row=22, column=1, sticky='w')
        
        # Current status section
        ttk.Label(self.analysis_frame, text="Trạng thái hiện tại:", 
                 font=('Arial', 10, 'bold')).grid(row=23, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # Time remaining
        ttk.Label(self.analysis_frame, text="Thời gian còn lại:").grid(row=24, column=0, sticky='w')
        self.time_remaining = tk.StringVar(value="0s")
        ttk.Label(self.analysis_frame, textvariable=self.time_remaining, foreground='red').grid(row=24, column=1, sticky='w')
        
        # Recommendations section
        ttk.Label(self.analysis_frame, text="Gợi ý điều chỉnh:", 
                 font=('Arial', 10, 'bold')).grid(row=25, column=0, columnspan=2, pady=(15,5), sticky='w')
        
        # Create text widget for recommendations
        self.recommendations_text = tk.Text(self.analysis_frame, height=6, width=40, wrap=tk.WORD)
        self.recommendations_text.grid(row=26, column=0, columnspan=2, pady=(5,0), sticky='ew')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.analysis_frame, orient="vertical", command=self.recommendations_text.yview)
        scrollbar.grid(row=26, column=2, sticky='ns')
        self.recommendations_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights for analysis frame
        self.analysis_frame.columnconfigure(1, weight=1)
        
    def update_frame(self, frames):
        """Update video displays for all 4 directions"""
        # frames should be a dict with keys: 'north', 'south', 'east', 'west'
        if not frames:
            return
            
        # Calculate display size for each video
        width = self.config['display']['window_size']['width'] // 3
        height = self.config['display']['window_size']['height'] // 3
        
        # Update each direction
        for direction in ['north', 'south', 'east', 'west']:
            if direction in frames:
                frame = cv2.resize(frames[direction], (width, height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert OpenCV frame to tkinter PhotoImage
                img = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
                
                # Update corresponding label
                if direction == 'north':
                    self.video_label_north.configure(image=img, text="")
                    self.video_label_north.imgtk = img
                elif direction == 'south':
                    self.video_label_south.configure(image=img, text="")
                    self.video_label_south.imgtk = img
                elif direction == 'east':
                    self.video_label_east.configure(image=img, text="")
                    self.video_label_east.imgtk = img
                elif direction == 'west':
                    self.video_label_west.configure(image=img, text="")
                    self.video_label_west.imgtk = img
        
    def update_stats(self, status):
        """Update analysis display with current status for 4 directions"""
        # Update current phase
        phase_text = f"Pha {status['current_phase'][-1]}: {'-'.join(status['current_directions'])}"
        self.current_phase_label.set(phase_text)
        
        # Update current timing (all directions get same phase time)
        phase_time = status.get('current_phase_time', 30)
        self.north_current.set(f"{phase_time}s")
        self.south_current.set(f"{phase_time}s")
        self.east_current.set(f"{phase_time}s")
        self.west_current.set(f"{phase_time}s")
        
        # Update density and vehicle counts for all directions
        self.north_density.set(f"{status['densities']['north']:.3f}")
        self.south_density.set(f"{status['densities']['south']:.3f}")
        self.east_density.set(f"{status['densities']['east']:.3f}")
        self.west_density.set(f"{status['densities']['west']:.3f}")
        
        self.north_vehicles.set(str(status['vehicle_counts']['north']))
        self.south_vehicles.set(str(status['vehicle_counts']['south']))
        self.east_vehicles.set(str(status['vehicle_counts']['east']))
        self.west_vehicles.set(str(status['vehicle_counts']['west']))
        
        # Update current status
        self.time_remaining.set(f"{int(status['time_remaining'])}s")
        
    def update_recommendations(self, recommendations):
        """Update recommendations display"""
        self.recommendations_text.delete(1.0, tk.END)
        for rec in recommendations:
            self.recommendations_text.insert(tk.END, f"• {rec}\n")
        
    def update_suggested_timing(self, suggested_times):
        """Update suggested timing display for all 4 directions"""
        self.north_suggested.set(f"{suggested_times['north']}s")
        self.south_suggested.set(f"{suggested_times['south']}s")
        self.east_suggested.set(f"{suggested_times['east']}s")
        self.west_suggested.set(f"{suggested_times['west']}s")
        
    def start(self):
        """Start video processing"""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.process_thread = threading.Thread(target=self.process_video)
            self.process_thread.start()
            
    def stop(self):
        """Stop video processing"""
        self.is_running = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join()
            
    def toggle_pause(self):
        """Pause/Resume video processing"""
        self.is_paused = not self.is_paused
        
    def on_closing(self):
        """Handle window closing"""
        self.stop()
        self.root.destroy()
        
    def process_video(self):
        """Video processing thread"""
        # This method should be implemented in the main application
        pass
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
