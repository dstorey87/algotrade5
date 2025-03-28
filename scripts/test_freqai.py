#!/usr/bin/env python
"""
FreqAI Test Runner

This script provides an easy way to test the FreqAI implementation.
It can run unit tests, integration tests, or start the FreqAI server locally.
"""

import os
import sys
import argparse
import unittest
import subprocess
from pathlib import Path

def run_unit_tests():
    """Run all FreqAI unit tests"""
    print("Running FreqAI unit tests...")
    
    # Get the directory of this script
    script_dir = Path(__file__).resolve().parent
    
    # Find the tests directory
    tests_dir = script_dir.parent.parent / "tests" / "unit" / "freqai"
    
    if not tests_dir.exists():
        print(f"Error: Tests directory not found at {tests_dir}")
        return False
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.discover(str(tests_dir), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_integration_tests():
    """Run FreqAI integration tests"""
    print("Running FreqAI integration tests...")
    
    # Get the directory of this script
    script_dir = Path(__file__).resolve().parent
    
    # Find the integration test file
    test_file = script_dir.parent.parent / "tests" / "unit" / "freqai" / "test_freqai_integration.py"
    
    if not test_file.exists():
        print(f"Error: Integration test file not found at {test_file}")
        return False
    
    # Run the tests
    result = subprocess.run([sys.executable, str(test_file)], capture_output=True, text=True)
    print(result.stdout)
    
    if result.stderr:
        print(f"Errors:\n{result.stderr}")
    
    return result.returncode == 0

def start_freqai_server():
    """Start the FreqAI server locally for testing"""
    print("Starting FreqAI server locally...")
    
    # Get the directory of this script
    script_dir = Path(__file__).resolve().parent
    
    # Find the main FreqAI interface module
    freqai_module = script_dir.parent.parent / "src" / "freqai_interface.py"
    
    if not freqai_module.exists():
        print(f"Error: FreqAI interface module not found at {freqai_module}")
        return False
    
    # Set required environment variables
    os.environ["MODEL_DIR"] = str(script_dir.parent.parent / "models")
    os.environ["INITIAL_CAPITAL"] = "10.0"
    os.environ["FREQAI_CONFIG_PATH"] = str(script_dir.parent.parent / "freqai_config.json")
    os.environ["ML_MODELS_PATH"] = str(script_dir.parent.parent / "models")
    
    # Create logs directory if it doesn't exist
    logs_dir = script_dir.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Start the server
    try:
        print(f"Starting FreqAI server with module {freqai_module}")
        print("Press Ctrl+C to stop the server")
        
        # Change working directory to the project root
        os.chdir(script_dir.parent.parent)
        
        # Run the server using uvicorn
        result = subprocess.run([
            "uvicorn", 
            "src.freqai_interface:app", 
            "--host", "0.0.0.0", 
            "--port", "8001",
            "--reload"
        ])
        
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\nServer stopped")
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

def verify_freqai_components():
    """Verify that all FreqAI components are properly installed"""
    print("Verifying FreqAI components...")
    
    # Check Python packages
    required_packages = [
        "numpy", "pandas", "scikit-learn", "fastapi", "uvicorn", 
        "torch", "transformers", "xgboost", "lightgbm", "catboost"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements-freqai-custom.txt")
        return False
    
    # Check freqai_config.json
    script_dir = Path(__file__).resolve().parent
    config_file = script_dir.parent.parent / "freqai_config.json"
    
    if not config_file.exists():
        print(f"Error: freqai_config.json not found at {config_file}")
        return False
    
    # Check for models directory
    models_dir = script_dir.parent.parent / "models"
    if not models_dir.exists() or not models_dir.is_dir():
        print(f"Warning: Models directory not found at {models_dir}")
        print("Models directory is required for FreqAI to function properly")
    
    print("FreqAI components verified successfully")
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="FreqAI Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--server", action="store_true", help="Start FreqAI server")
    parser.add_argument("--verify", action="store_true", help="Verify FreqAI components")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    # Default to --verify if no arguments provided
    if not any(vars(args).values()):
        args.verify = True
    
    # Run all tests if --all is specified
    if args.all:
        args.unit = True
        args.integration = True
        args.verify = True
    
    # Track success status
    success = True
    
    # Run selected operations
    if args.verify:
        success = verify_freqai_components() and success
    
    if args.unit:
        success = run_unit_tests() and success
    
    if args.integration:
        success = run_integration_tests() and success
    
    if args.server:
        return start_freqai_server()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())