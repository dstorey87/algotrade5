#!/usr/bin/env python3
"""
System Health Checker for AlgoTradPro5
Monitors system resources and health metrics
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import sys
import threading
import time
import logging
import psutil
import GPUtil
import json

# Set base directory to absolute path
BASE_DIR = Path("c:/AlgoTradPro5").resolve()

# Create logs directory with absolute path
(BASE_DIR / "logs").mkdir(exist_ok=True)

# Log to absolute path
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(BASE_DIR / "logs/system_init.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemHealthChecker:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.gpu_available = False
        self.monitoring_thread = None
        self.stop_monitoring = False
        self.metrics_history = []
        self.critical_errors = []
        self.system_status = "initializing"
        
        # Create logs directory with absolute path
        (self.base_dir / "logs").mkdir(exist_ok=True)
        
        # Try importing GPU monitoring
        try:
            GPUtil.getGPUs()  # Test if GPU monitoring is available
            self.gpu_available = True
            logger.info("GPU monitoring enabled")
        except ImportError:
            logger.warning("GPUtil not available - GPU monitoring disabled")
            
    def initialize_system(self) -> bool:
        """Initialize system and check core requirements"""
        try:
            logger.info("Initializing system health checker...")
            
            # Check Python version
            if not self._check_python_version():
                return False
                
            # Check system resources
            if not self._check_system_resources():
                return False
                
            # Check disk space
            if not self._check_disk_space():
                return False
                
            # Initialize GPU monitoring if available
            if self.gpu_available:
                if not self._initialize_gpu_monitoring():
                    logger.warning("GPU monitoring initialization failed")
                    
            # Start monitoring thread
            self._start_monitoring()
            
            self.system_status = "healthy"
            logger.info("System health checker initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            self.system_status = "error"
            return False
            
    def _check_python_version(self) -> bool:
        """Verify Python version meets requirements"""
        required_version = (3, 9)
        current_version = sys.version_info[:2]
        
        if current_version < required_version:
            logger.error(
                f"Python {required_version[0]}.{required_version[1]} or higher required. "
                f"Current: {current_version[0]}.{current_version[1]}"
            )
            return False
            
        return True
        
    def _check_system_resources(self) -> bool:
        """Check available system resources"""
        try:
            # Check CPU
            cpu_count = psutil.cpu_count()
            if cpu_count < 2:
                logger.warning("Minimum 2 CPU cores recommended")
                
            # Check RAM
            memory = psutil.virtual_memory()
            min_ram = 8 * 1024 * 1024 * 1024  # 8GB
            if memory.total < min_ram:
                logger.warning("Minimum 8GB RAM recommended")
                
            # Check if system is overloaded
            if memory.percent > 90:
                logger.error("System memory usage too high (>90%)")
                return False
                
            if psutil.cpu_percent(interval=1) > 90:
                logger.error("CPU usage too high (>90%)")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking system resources: {e}")
            return False
            
    def _check_disk_space(self) -> bool:
        """Check available disk space"""
        try:
            # Check current directory
            usage = psutil.disk_usage('.')
            min_space = 10 * 1024 * 1024 * 1024  # 10GB
            
            if usage.free < min_space:
                logger.error(f"Insufficient disk space. {usage.free / 1e9:.1f}GB available")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking disk space: {e}")
            return False
            
    def _initialize_gpu_monitoring(self) -> bool:
        """Initialize GPU monitoring if available"""
        try:
            gpus = GPUtil.getGPUs()
            
            if gpus:
                gpu = gpus[0]  # Use primary GPU
                logger.info(f"Found GPU: {gpu.name}")
                
                # Check GPU memory
                if gpu.memoryTotal < 4096:
                    logger.warning("GPU has less than 4GB memory")
                    return False
                    
                # Initialize metrics file with absolute path
                metrics_file = self.base_dir / "gpu_metrics.json"
                if not metrics_file.exists():
                    with open(metrics_file, 'w') as f:
                        json.dump({"gpu_metrics": []}, f)
                    
                return True
            else:
                logger.warning("No GPU devices found")
                return False
                
        except Exception as e:
            logger.error(f"GPU initialization error: {e}")
            return False
            
    def _start_monitoring(self):
        """Start system monitoring in background thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
            
        self.stop_monitoring = False
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while not self.stop_monitoring:
            try:
                metrics = self._collect_metrics()
                self._save_metrics(metrics)
                
                # Check for critical conditions
                self._check_critical_conditions(metrics)
                
                # Update system status
                self._update_system_status(metrics)
                
                # Sleep for a bit
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Sleep shorter on error
                
    def _collect_metrics(self) -> Dict:
        """Collect current system metrics"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': psutil.cpu_percent(interval=1),
                    'count': psutil.cpu_count(),
                    'load_avg': psutil.getloadavg()
                },
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent
                },
                'disk': {
                    'total': psutil.disk_usage('.').total,
                    'free': psutil.disk_usage('.').free,
                    'percent': psutil.disk_usage('.').percent
                }
            }
            
            # Add GPU metrics if available
            if self.gpu_available:
                try:
                    gpu = GPUtil.getGPUs()[0]  # Use primary GPU
                    metrics['gpu'] = {
                        'name': gpu.name,
                        'memory_total': gpu.memoryTotal,
                        'memory_used': gpu.memoryUsed,
                        'memory_used_percent': (gpu.memoryUsed / gpu.memoryTotal) * 100,
                        'temperature': gpu.temperature,
                        'load': gpu.load * 100
                    }
                except Exception as gpu_err:
                    logger.error(f"Error collecting GPU metrics: {gpu_err}")
                    
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
            
    def _save_metrics(self, metrics: Dict):
        """Save metrics to history"""
        try:
            self.metrics_history.append(metrics)
            
            # Keep last 1440 entries (24 hours at 1-minute intervals)
            if len(self.metrics_history) > 1440:
                self.metrics_history = self.metrics_history[-1440:]
                
            # Save to file periodically
            if len(self.metrics_history) % 30 == 0:
                self._write_metrics_to_file()
                
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def _write_metrics_to_file(self):
        """Write metrics to JSON file"""
        try:
            metrics_file = self.base_dir / "logs/system_metrics.json"
            with open(metrics_file, 'w') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'metrics_history': self.metrics_history[-100:]  # Save last 100 entries
                }, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error writing metrics to file: {e}")
            
    def _check_critical_conditions(self, metrics: Dict):
        """Check for critical system conditions"""
        try:
            # Check memory usage
            if metrics.get('memory', {}).get('percent', 0) > 90:
                self._add_critical_error("Memory usage critical (>90%)")
                
            # Check CPU usage
            if metrics.get('cpu', {}).get('percent', 0) > 90:
                self._add_critical_error("CPU usage critical (>90%)")
                
            # Check disk space
            if metrics.get('disk', {}).get('percent', 0) > 90:
                self._add_critical_error("Disk space critical (>90% used)")
                
            # Check GPU if available
            if 'gpu' in metrics:
                if metrics['gpu'].get('memory_used_percent', 0) > 90:
                    self._add_critical_error("GPU memory usage critical (>90%)")
                if metrics['gpu'].get('temperature', 0) > 85:
                    self._add_critical_error("GPU temperature critical (>85°C)")
                    
        except Exception as e:
            logger.error(f"Error checking critical conditions: {e}")
            
    def _add_critical_error(self, error: str):
        """Add critical error to list"""
        timestamp = datetime.now().isoformat()
        self.critical_errors.append({
            'timestamp': timestamp,
            'error': error
        })
        
        # Keep last 100 errors
        if len(self.critical_errors) > 100:
            self.critical_errors = self.critical_errors[-100:]
            
        logger.error(f"Critical condition: {error}")
        
    def _update_system_status(self, metrics: Dict):
        """Update overall system status"""
        try:
            if len(self.critical_errors) > 0:
                self.system_status = "critical"
                    
            elif (metrics.get('memory', {}).get('percent', 0) > 80 or 
                metrics.get('cpu', {}).get('percent', 0) > 80 or 
                metrics.get('disk', {}).get('percent', 0) > 80):
                self.system_status = "warning"
            else:
                self.system_status = "healthy"
                
        except Exception as e:
            logger.error(f"Error updating system status: {e}")
            self.system_status = "unknown"
            
    def get_system_status(self) -> Dict:
        """Get current system status and metrics"""
        try:
            current_metrics = self._collect_metrics()
            
            return {
                'status': self.system_status,
                'timestamp': datetime.now().isoformat(),
                'metrics': current_metrics,
                'critical_errors': self.critical_errors[-5:],  # Last 5 errors
                'gpu_available': self.gpu_available
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
            
    def stop(self):
        """Stop system monitoring"""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

if __name__ == "__main__":
    # Test the system health checker
    checker = SystemHealthChecker()
    
    if checker.initialize_system():
        print("\nSystem initialized successfully")
        print("\nCurrent system status:")
        status = checker.get_system_status()
        print(json.dumps(status, indent=2))
        
        # Run for a test period
        print("\nMonitoring system for 5 minutes...")
        time.sleep(300)
        
        checker.stop()
        print("\nMonitoring stopped")
    else:
        print("\nSystem initialization failed")