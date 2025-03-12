#!/usr/bin/env python3
"""
System Integration for AlgoTradPro5
Connects all components together for unified operation
"""
import logging
import os
import sys
import json
import asyncio
import signal
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/system_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Import local components
try:
    from config_manager import ConfigManager
    from ai_model_manager import AIModelManager
    from quantum_optimizer import QuantumOptimizer
    from risk_manager import RiskManager
    from trade_journal import TradeJournal
    from strategy_engine import StrategyEngine
    from system_health_checker import SystemHealthChecker
    from freqai_interface import FreqAIInterface
except ImportError as e:
    logger.error(f"Error importing components: {e}")
    sys.exit(1)

class SystemIntegration:
    """Integrates all AlgoTradPro5 components for unified operation"""
    
    def __init__(self, config_path: str = None):
        """Initialize the system integration"""
        try:
            # Set base directory
            self.base_dir = Path("c:/AlgoTradPro5")

            # Load configuration
            self.config_manager = ConfigManager(config_path)

            # Create logs directory
            (self.base_dir / "logs").mkdir(exist_ok=True)

            # Configure logging with absolute path
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(str(self.base_dir / "logs/system_integration.log")),
                    logging.StreamHandler()
                ]
            )
            
            # Verify configuration
            if not self.config_manager.validate():
                logger.error("Invalid configuration")
                sys.exit(1)
            
            # Initialize system health checker
            self.health_checker = SystemHealthChecker()
            
            # Initialize components
            self._initialize_components()
            
            # Runtime state
            self.running = False
            self.shutdown_event = threading.Event()
            
            logger.info("System integration initialized")
            
        except Exception as e:
            logger.error(f"Error initializing system integration: {e}")
            raise
    
    def _initialize_components(self):
        """Initialize all system components"""
        try:
            logger.info("Initializing system components...")
            
            # Initialize AI Model Manager
            self.ai_manager = AIModelManager(self.config_manager)
            
            # Initialize Quantum Optimizer
            quantum_settings = {
                'n_qubits': self.config_manager.get('quantum.n_qubits', 4),
                'shots': self.config_manager.get('quantum.shots', 1000),
                'optimization_level': self.config_manager.get('quantum.optimization_level', 2)
            }
            self.quantum_optimizer = QuantumOptimizer(**quantum_settings)
            
            # Initialize Risk Manager
            initial_capital = self.config_manager.get('trading.stake_amount', 10.0)
            self.risk_manager = RiskManager(initial_capital=initial_capital)
            
            # Initialize Trade Journal
            self.trade_journal = TradeJournal()
            
            # Initialize Strategy Engine
            self.strategy_engine = StrategyEngine(self.config_manager)
            
            # Initialize FreqAI Interface
            self.freqai_interface = FreqAIInterface()
            
            logger.info("All system components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    async def start(self):
        """Start all system components"""
        try:
            logger.info("Starting system integration...")
            
            # Initialize system health
            if not self.health_checker.initialize_system():
                logger.error("System health check failed")
                return False
                
            # Initialize AI models asynchronously
            logger.info("Initializing AI models...")
            await self.ai_manager.initialize_models_async()
            
            # Initialize FreqAI Interface
            logger.info("Initializing FreqAI Interface...")
            await self.freqai_interface.initialize_async()
            
            # Start Strategy Engine
            logger.info("Starting Strategy Engine...")
            self.strategy_engine.start()
            
            # Set running state
            self.running = True
            
            # Start monitoring thread
            self._start_monitoring()
            
            logger.info("System integration started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting system integration: {e}")
            await self.stop()
            return False
    
    async def stop(self):
        """Stop all system components"""
        try:
            logger.info("Stopping system integration...")
            
            # Set shutdown flag
            self.running = False
            self.shutdown_event.set()
            
            # Stop Strategy Engine
            logger.info("Stopping Strategy Engine...")
            self.strategy_engine.stop()
            
            # Clean up FreqAI Interface
            logger.info("Cleaning up FreqAI Interface...")
            await self.freqai_interface.cleanup()
            
            # Clean up AI Manager
            logger.info("Cleaning up AI Manager...")
            await self.ai_manager.cleanup()
            
            # Stop health checker
            logger.info("Stopping health checker...")
            self.health_checker.stop()
            
            logger.info("System integration stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping system integration: {e}")
            return False
    
    def _start_monitoring(self):
        """Start monitoring thread for system health"""
        monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        monitoring_thread.start()
    
    def _monitoring_loop(self):
        """Monitor system health and components"""
        check_interval = 60  # seconds
        
        while not self.shutdown_event.is_set():
            try:
                # Check system health
                system_status = self.health_checker.get_system_status()
                
                # Get strategy status
                strategy_status = self.strategy_engine.get_status()
                
                # Check for critical conditions
                self._check_critical_conditions(system_status, strategy_status)
                
                # Log system state periodically
                self._log_system_state(system_status, strategy_status)
                
                # Sleep until next check
                self.shutdown_event.wait(check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Sleep shorter on error
    
    def _check_critical_conditions(self, system_status, strategy_status):
        """Check for critical system conditions"""
        try:
            # Check system status
            if system_status['status'] == 'critical':
                logger.critical("CRITICAL SYSTEM STATUS DETECTED")
                self._emergency_procedures()
                return
                
            # Check risk status
            risk_status = strategy_status.get('risk_status', {})
            if risk_status.get('consecutive_losses', 0) >= 2:
                logger.warning("Multiple consecutive losses detected")
                
            # Check performance vs requirements
            compliance = strategy_status.get('strategy_compliance', {})
            failed_metrics = [m for m, data in compliance.items() if not data['passed']]
            if failed_metrics:
                logger.warning(f"Strategy not meeting requirements for: {failed_metrics}")
                
        except Exception as e:
            logger.error(f"Error checking critical conditions: {e}")
    
    def _emergency_procedures(self):
        """Handle emergency situations"""
        try:
            logger.critical("Executing emergency procedures")
            
            # Trigger stop in a non-blocking way
            asyncio.create_task(self.stop())
            
            # Notify via all available channels
            self._send_emergency_notifications()
            
        except Exception as e:
            logger.error(f"Error in emergency procedures: {e}")
    
    def _send_emergency_notifications(self):
        """Send emergency notifications through all channels"""
        message = f"EMERGENCY: Critical system condition detected at {datetime.now().isoformat()}"
        
        try:
            # Log to file with absolute path
            with open(str(self.base_dir / "logs/emergency.log"), "a") as f:
                f.write(f"{message}\n")
                
            # Send to Telegram if configured
            if self.config_manager.get('telegram.enabled', False):
                try:
                    # This would normally use the telegram client
                    logger.info("Would send Telegram notification")
                except Exception as telegram_err:
                    logger.error(f"Failed to send Telegram notification: {telegram_err}")
                    
            logger.critical(message)
            
        except Exception as e:
            logger.error(f"Error sending emergency notifications: {e}")
    
    def _log_system_state(self, system_status, strategy_status):
        """Log system state periodically"""
        try:
            # Every 10 minutes (approx) log detailed state
            if int(time.time()) % 600 < 60:
                state = {
                    'timestamp': datetime.now().isoformat(),
                    'system': system_status,
                    'strategy': strategy_status,
                }
                
                # Save to state log with absolute path
                with open(str(self.base_dir / "logs/system_state.json"), "w") as f:
                    json.dump(state, f, indent=2)
                
                # Log summary
            health_status = self.health_checker.get_system_status()
            if health_status['status'] == 'error':
                logger.error("Health check failed")
                return False
                
            # Test AI Manager
            logger.info("Testing AI Manager...")
            test_data = {
                'symbol': 'BTC/USDT',
                'timeframe': '1h',
                'timestamp': datetime.now().isoformat(),
                'open': [100, 101, 99, 102, 103, 101, 104, 105, 103, 106],
                'high': [102, 103, 101, 104, 105, 103, 106, 107, 105, 108],
                'low': [99, 100, 98, 101, 102, 100, 103, 104, 102, 105],
                'close': [101, 99, 102, 103, 101, 104, 105, 103, 106, 107],
                'volume': [1000, 1100, 900, 1200, 1300, 1100, 1400, 1500, 1200, 1600]
            }
            analysis = self.ai_manager.get_combined_analysis(test_data)
            if not analysis:
                logger.error("AI Manager analysis failed")
                return False
                
            # Test FreqAI Interface
            logger.info("Testing FreqAI Interface...")
            import pandas as pd
            import numpy as np
            
            dates = pd.date_range(start='2023-01-01', periods=10, freq='1h')
            df = pd.DataFrame({
                'open': np.array(test_data['open']),
                'high': np.array(test_data['high']),
                'low': np.array(test_data['low']),
                'close': np.array(test_data['close']),
                'volume': np.array(test_data['volume'])
            }, index=dates)
            
            result = await self.freqai_interface.analyze_dataframe_async(df, 'BTC/USDT', '1h')
            if result is None:
                logger.error("FreqAI Interface analysis failed")
                return False
                
            # Test Strategy Engine
            logger.info("Testing Strategy Engine...")
            self.strategy_engine.submit_market_data(test_data)
            strategy_status = self.strategy_engine.get_status()
            if not strategy_status:
                logger.error("Strategy Engine test failed")
                return False
                
            logger.info("Integration test completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Integration test error: {e}")
            return False

def handle_signals():
    """Handle system signals"""
    integration = None
    
    def signal_handler(sig, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {sig}, shutting down")
        if integration:
            asyncio.create_task(integration.stop())
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    return integration

async def main():
    """Main function"""
    try:
        # Initialize system integration
        integration = SystemIntegration()
        
        # Run integration test
        test_success = await integration.run_integration_test()
        if not test_success:
            logger.error("Integration test failed, exiting")
            return 1
            
        # Start system
        start_success = await integration.start()
        if not start_success:
            logger.error("System start failed, exiting")
            return 1
            
        # Keep system running
        while integration.running:
            await asyncio.sleep(1)
            
        return 0
        
    except Exception as e:
        logger.error(f"System error: {e}")
        return 1

if __name__ == "__main__":
    # Set up signal handlers
    handle_signals()
    
    # Run main async function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)