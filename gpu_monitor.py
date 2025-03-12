#!/usr/bin/env python3
"""GPU Monitoring for AlgoTradPro5"""
import os
import sys
import logging
import json
import time
import psutil
from pathlib import Path
from typing import Dict, Optional
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to get torch for CUDA detection
TORCH_AVAILABLE = False
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    pass

class GPUMonitor:
    def __init__(self):
        self.running = False
        self.monitor_thread = None
        self.cuda_version = os.environ.get('CUDA_VERSION', '11.8')  # Default to 11.8
        self.cuda_path = os.environ.get('CUDA_PATH', r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8')
        self._setup_gpu_environment()
        
    def _setup_gpu_environment(self):
        """Setup GPU environment with correct CUDA paths"""
        if os.path.exists(self.cuda_path):
            os.environ['CUDA_PATH'] = self.cuda_path
            os.environ['CUDA_HOME'] = self.cuda_path
            cuda_bin = os.path.join(self.cuda_path, 'bin')
            if cuda_bin not in os.environ['PATH']:
                os.environ['PATH'] = cuda_bin + os.pathsep + os.environ['PATH']
            logger.info(f"GPU environment set to CUDA {self.cuda_version}")
        else:
            logger.warning(f"CUDA installation not found at {self.cuda_path}")

    def start_monitoring(self):
        """Start GPU monitoring in background thread"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                daemon=True
            )
            self.monitor_thread.start()
            logger.info("GPU monitoring started")

    def stop_monitoring(self):
        """Stop GPU monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("GPU monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        metrics_file = Path("gpu_metrics.json")
        
        while self.running:
            try:
                # Get current metrics
                metrics = self._get_gpu_metrics()
                
                # Update metrics file
                self._update_metrics_file(metrics, metrics_file)
                
                # Sleep briefly
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in GPU monitoring: {e}")
                time.sleep(5)  # Sleep longer on error

    def _get_gpu_metrics(self) -> Dict:
        """Get current GPU metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'gpu_detected': False,
            'cuda_version': self.cuda_version,
            'cuda_path': self.cuda_path
        }
        
        try:
            # Get NVIDIA-smi metrics if available
            gpu_info = self._get_nvidia_smi_metrics()
            if gpu_info:
                metrics.update(gpu_info)
                metrics['gpu_detected'] = True
            
            # Get PyTorch metrics if available
            if TORCH_AVAILABLE and torch.cuda.is_available():
                torch_metrics = {
                    'device_name': torch.cuda.get_device_name(0),
                    'device_count': torch.cuda.device_count(),
                    'cuda_version': torch.version.cuda,
                    'memory': {
                        'allocated': torch.cuda.memory_allocated(),
                        'reserved': torch.cuda.memory_reserved()
                    }
                }
                metrics['torch'] = torch_metrics
                metrics['gpu_detected'] = True
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting GPU metrics: {e}")
            return metrics

    def _get_nvidia_smi_metrics(self) -> Optional[Dict]:
        """Get metrics using nvidia-smi"""
        try:
            # Use nvidia-smi executable from CUDA path first
            nvidia_smi = os.path.join(self.cuda_path, 'bin', 'nvidia-smi.exe')
            if not os.path.exists(nvidia_smi):
                # Try system path
                nvidia_smi = 'nvidia-smi'
            
            # Run nvidia-smi
            import subprocess
            result = subprocess.run(
                [nvidia_smi, '--query-gpu=memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu',
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse metrics
                values = result.stdout.strip().split(',')
                return {
                    'nvidia_smi': {
                        'memory_total_mb': float(values[0]),
                        'memory_used_mb': float(values[1]),
                        'memory_free_mb': float(values[2]),
                        'temperature_c': float(values[3]),
                        'utilization_percent': float(values[4])
                    }
                }
            
        except Exception as e:
            logger.debug(f"Could not get nvidia-smi metrics: {e}")
        
        return None

    def _update_metrics_file(self, metrics: Dict, file_path: Path):
        """Update GPU metrics file"""
        try:
            # Create parent directory if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write metrics to file
            with open(file_path, 'w') as f:
                json.dump(metrics, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error updating metrics file: {e}")

    def get_current_metrics(self) -> Dict:
        """Get current GPU metrics"""
        try:
            return self._get_gpu_metrics()
        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'gpu_detected': False,
                'error': str(e)
            }
            
    # Fix missing methods that are called in run_algotradpro5.py
    def get_gpu_info(self) -> Dict:
        """Get information about the GPU"""
        metrics = self.get_current_metrics()
        if TORCH_AVAILABLE and torch.cuda.is_available():
            return {
                'device_name': torch.cuda.get_device_name(0),
                'device_count': torch.cuda.device_count(),
                'cuda_version': torch.version.cuda,
                'gpu_detected': True
            }
        elif 'nvidia_smi' in metrics:
            return {
                'device_name': "NVIDIA GPU",
                'gpu_detected': True,
                'memory_total_mb': metrics['nvidia_smi']['memory_total_mb']
            }
        else:
            return {
                'device_name': "No GPU detected",
                'gpu_detected': False,
                'error': "No CUDA-capable GPU found"
            }
    
    def get_memory_stats(self) -> Dict:
        """Get GPU memory statistics"""
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {
                'allocated': 0,
                'cached': 0,
                'free': 0
            }
            
        try:
            allocated = torch.cuda.memory_allocated()
            cached = torch.cuda.memory_reserved()
            total = 0
            
            metrics = self.get_current_metrics()
            if 'nvidia_smi' in metrics:
                total = metrics['nvidia_smi']['memory_total_mb'] * 1024 * 1024
            
            return {
                'allocated': allocated,
                'cached': cached,
                'free': total - allocated if total > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {
                'allocated': 0,
                'cached': 0,
                'free': 0,
                'error': str(e)
            }

if __name__ == "__main__":
    # Test GPU monitoring
    monitor = GPUMonitor()
    monitor.start_monitoring()
    
    try:
        # Run for 60 seconds
        time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop_monitoring()