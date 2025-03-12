import os
import sys
import logging

# Ensure all dependencies are installed before proceeding
try:
    from dependency_manager import ensure_dependencies
    # For integration testing we need all components
    ensure_dependencies(components=["quantitative", "ai", "quantum", "api"])
except ImportError:
    print("Warning: Dependency manager not found. Installing core dependencies...")
    try:
        # Try to install core dependencies manually
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "torch", "pennylane"])
        print("Core dependencies installed successfully.")
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        print("Some tests may fail due to missing dependencies.")

import numpy as np
from pathlib import Path
from quantum_optimizer import QuantumOptimizer
from gpu_monitor import GPUMonitor
from initialize_system import SystemInitializer

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_quantum_circuit():
    """Test quantum circuit optimization"""
    # Updated to match the actual constructor parameters
    optimizer = QuantumOptimizer(n_qubits=4, shots=1000, optimization_level=2)
    
    # Generate synthetic test data
    n_samples = 100
    input_data = np.random.random((n_samples, 4))
    
    # Test pattern analysis
    results = optimizer.analyze_pattern(input_data)
    
    assert "pattern_score" in results, "Analysis results missing pattern_score"
    assert "confidence" in results, "Analysis results missing confidence"
    assert "regime" in results, "Analysis results missing regime"
    assert 0 <= results["pattern_score"] <= 1, "Pattern score should be between 0 and 1"
    
    # Test with different data shape
    test_input = np.random.random((10, 4))
    new_results = optimizer.analyze_pattern(test_input)
    
    assert "pattern_score" in new_results, "Analysis results missing pattern_score for new data"
    
    return True

def test_gpu_monitoring():
    """Test GPU monitoring functionality"""
    monitor = GPUMonitor()
    
    # Get initial metrics
    gpu_metrics = monitor.get_gpu_metrics()
    system_metrics = monitor.get_system_metrics()
    
    assert isinstance(gpu_metrics, dict), "GPU metrics should be a dictionary"
    assert isinstance(system_metrics, dict), "System metrics should be a dictionary"
    
    return True

def test_system_initialization():
    """Test system initialization"""
    initializer = SystemInitializer()
    
    # Test initialization
    success = initializer.initialize_system()
    assert success, "System initialization failed"
    
    # Verify quantum device setup
    quantum_device = initializer.setup_quantum_device()
    assert quantum_device is not None, "Failed to setup quantum device"
    
    return True

def run_integration_tests():
    """Run all integration tests"""
    logger.info("Starting integration tests...")
    
    test_results = {
        "quantum_circuit": False,
        "gpu_monitoring": False,
        "system_initialization": False
    }
    
    try:
        test_results["quantum_circuit"] = test_quantum_circuit()
        logger.info("Quantum circuit test passed")
    except Exception as e:
        logger.error(f"Quantum circuit test failed: {e}")
        
    try:
        test_results["gpu_monitoring"] = test_gpu_monitoring()
        logger.info("GPU monitoring test passed")
    except Exception as e:
        logger.error(f"GPU monitoring test failed: {e}")
        
    try:
        test_results["system_initialization"] = test_system_initialization()
        logger.info("System initialization test passed")
    except Exception as e:
        logger.error(f"System initialization test failed: {e}")
        
    return all(test_results.values())

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("AlgoTradPro5 - Integration Test Suite".center(80))
    print("=" * 80 + "\n")
    
    # Ensure dependencies are installed before running tests
    try:
        from dependency_manager import ensure_dependencies
        ensure_dependencies(components=["quantum"])
    except ImportError:
        print("Dependency manager not fully configured. Proceeding with available packages.")
    
    success = run_integration_tests()
    
    if success:
        print("\n✅ All integration tests passed successfully!")
    else:
        print("\n❌ Some integration tests failed. Check the logs for details.")
    
    sys.exit(0 if success else 1)