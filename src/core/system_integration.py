"""
System Integration Module
=====================

CRITICAL REQUIREMENTS:
- Component coordination
- System state management
- Service discovery
- Health monitoring
- System shutdown handling

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import signal
import threading
from typing import Dict, List, Optional
from datetime import datetime

from src.core.config_manager import get_config
from src.core.error_manager import ErrorManager, ErrorSeverity
from src.core.initialize_system import initialize_system, get_system_status
from src.core.data_manager import DataManager
from src.core.ai_model_manager import AIModelManager
from src.monitoring.gpu_monitor import GPUMonitor
from src.monitoring.system_health_checker import check_system_health

logger = logging.getLogger(__name__)

class SystemIntegration:
    """System-wide integration and coordination"""
    
    def __init__(self):
        """Initialize system integration"""
        self.config = get_config()
        self.error_manager = ErrorManager()
        self.data_manager = DataManager()
        self.ai_manager = AIModelManager()
        self.gpu_monitor = GPUMonitor()
        
        # Component states
        self._running = False
        self._components_status: Dict[str, bool] = {}
        self._active_threads: List[threading.Thread] = []
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
    def start_system(self) -> bool:
        """Start all system components in correct order"""
        try:
            logger.info("Starting system integration...")
            
            # Initialize core system
            if not initialize_system():
                return False
                
            self._running = True
            
            # Start monitoring threads
            self._start_monitoring()
            
            # Initialize AI models
            if not self.ai_manager.initialize_models():
                self.error_manager.log_error(
                    "Failed to initialize AI models",
                    ErrorSeverity.HIGH.value,
                    "AIModels"
                )
                return False
                
            # Start data processing
            if not self.data_manager.start_processing():
                self.error_manager.log_error(
                    "Failed to start data processing",
                    ErrorSeverity.HIGH.value,
                    "DataProcessing"
                )
                return False
                
            logger.info("System integration complete")
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"System integration failed: {e}",
                ErrorSeverity.CRITICAL.value,
                "Integration"
            )
            return False
            
    def _start_monitoring(self) -> None:
        """Start monitoring threads"""
        monitor_thread = threading.Thread(
            target=self._monitor_system_health,
            daemon=True
        )
        monitor_thread.start()
        self._active_threads.append(monitor_thread)
        
        gpu_thread = threading.Thread(
            target=self._monitor_gpu,
            daemon=True
        )
        gpu_thread.start()
        self._active_threads.append(gpu_thread)
        
    def _monitor_system_health(self) -> None:
        """Monitor overall system health"""
        while self._running:
            try:
                if not check_system_health():
                    self.error_manager.log_error(
                        "System health check failed",
                        ErrorSeverity.HIGH.value,
                        "SystemHealth"
                    )
                    
                # Update component states
                self._components_status.update({
                    'data_manager': self.data_manager.is_healthy(),
                    'ai_manager': self.ai_manager.is_healthy(),
                    'gpu': self.gpu_monitor.is_healthy()
                })
                
            except Exception as e:
                self.error_manager.log_error(
                    f"Health monitoring error: {e}",
                    ErrorSeverity.MEDIUM.value,
                    "Monitoring"
                )
                
            # Sleep for monitoring interval
            threading.Event().wait(
                float(self.config.get('MONITOR_INTERVAL', 5))
            )
            
    def _monitor_gpu(self) -> None:
        """Monitor GPU health and resource usage"""
        while self._running:
            try:
                self.gpu_monitor.check_gpu_health()
            except Exception as e:
                self.error_manager.log_error(
                    f"GPU monitoring error: {e}",
                    ErrorSeverity.MEDIUM.value,
                    "GPU"
                )
                
            # Sleep for GPU check interval
            threading.Event().wait(
                float(self.config.get('GPU_CHECK_INTERVAL', 10))
            )
            
    def _handle_shutdown(self, signum: int, frame) -> None:
        """Handle system shutdown gracefully"""
        logger.info("Initiating system shutdown...")
        self._running = False
        
        try:
            # Stop all components
            self.data_manager.stop_processing()
            self.ai_manager.cleanup()
            
            # Wait for monitoring threads
            for thread in self._active_threads:
                thread.join(timeout=5.0)
                
            logger.info("System shutdown complete")
            
        except Exception as e:
            self.error_manager.log_error(
                f"Error during shutdown: {e}",
                ErrorSeverity.HIGH.value,
                "Shutdown"
            )
            
    def get_system_metrics(self) -> Dict:
        """Get system-wide metrics and status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system_status': get_system_status(),
            'components': self._components_status,
            'gpu_metrics': self.gpu_monitor.get_metrics(),
            'errors': self.error_manager.get_error_summary()
        }

# Create global instance
_system_integration = SystemIntegration()

def get_system_integration() -> SystemIntegration:
    """Global function to get system integration instance"""
    return _system_integration