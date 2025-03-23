"""
Core System Setup Script
=====================

CRITICAL REQUIREMENTS:
- Environment validation
- Path configuration
- Package installation
- Database initialization
- Model directory setup

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

from src.core.error_manager import ErrorSeverity, get_error_manager


def check_python_version() -> bool:
    """Check if Python version meets requirements"""
    return sys.version_info >= (3, 9)


def setup_virtual_env() -> bool:
    """Create and configure virtual environment"""
    try:
        venv_path = Path(".venv")
        if not venv_path.exists():
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

        # Get venv Python path
        if os.name == "nt":  # Windows
            python_path = venv_path / "Scripts" / "python.exe"
        else:  # Unix
            python_path = venv_path / "bin" / "python"

        # Install core requirements
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )

        return True

    except subprocess.CalledProcessError as e:
        get_error_manager().log_error(
            f"Virtual environment setup failed: {e}", ErrorSeverity.HIGH.value, "Setup"
        )
        return False


def setup_directories() -> bool:
    """Create required directories"""
    try:
        dirs = [
            "data",
            "models/ml",
            "models/quantum",
            "logs",
            "backups",
            "config",
            "src/monitoring",
            "src/utils/setup",
            "src/utils/cuda",
            "tests/unit",
            "tests/integration",
        ]

        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        return True

    except Exception as e:
        get_error_manager().log_error(
            f"Directory setup failed: {e}", ErrorSeverity.HIGH.value, "Setup"
        )
        return False


def initialize_env_file() -> bool:
    """Initialize .env file if not exists"""
    try:
        env_path = Path(".env")
        if not env_path.exists():
            template_path = Path("config/env.template")
            if template_path.exists():
                shutil.copy2(template_path, env_path)
            else:
                # Create basic .env file
                with open(env_path, "w") as f:
                    f.write("""# AlgoTradePro5 Environment Configuration
MODELS_DIR=C:/AlgoTradPro5/models
LOG_DIR=C:/AlgoTradPro5/logs
BACKUP_DIR=C:/AlgoTradPro5/backups
DATA_RETENTION_DAYS=30
MONITOR_INTERVAL=5
""")

        return True

    except Exception as e:
        get_error_manager().log_error(
            f"Environment file setup failed: {e}", ErrorSeverity.HIGH.value, "Setup"
        )
        return False


def validate_setup() -> Dict[str, bool]:
    """Validate system setup"""
    return {
        "python_version": check_python_version(),
        "directories": all(
            Path(d).exists() for d in ["data", "models", "logs", "config"]
        ),
        "env_file": Path(".env").exists(),
        "requirements": Path("requirements.txt").exists(),
    }


def main() -> int:
    """Main setup function"""
    error_manager = get_error_manager()

    print("Starting AlgoTradePro5 setup...")

    # Check Python version
    if not check_python_version():
        error_manager.log_error(
            "Python 3.9 or higher required", ErrorSeverity.CRITICAL.value, "Setup"
        )
        return 1

    # Setup virtual environment
    if not setup_virtual_env():
        return 1

    # Create directories
    if not setup_directories():
        return 1

    # Initialize .env file
    if not initialize_env_file():
        return 1

    # Validate setup
    validation = validate_setup()
    if not all(validation.values()):
        failed = [k for k, v in validation.items() if not v]
        error_manager.log_error(
            f"Setup validation failed for: {', '.join(failed)}",
            ErrorSeverity.HIGH.value,
            "Setup",
        )
        return 1

    print("Setup completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
