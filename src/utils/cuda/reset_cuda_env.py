#!/usr/bin/env python3
"""
Reset CUDA Environment for AlgoTradPro5
This script uninstalls and reinstalls CUDA-dependent packages to ensure correct versions
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_cuda_env():
    """Set CUDA environment variables"""
    cuda_path = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8"
    if not os.path.exists(cuda_path):
        raise RuntimeError(f"CUDA 11.8 not found at: {cuda_path}")

    # Set environment variables
    os.environ["CUDA_PATH"] = cuda_path
    os.environ["CUDA_HOME"] = cuda_path
    os.environ["CUDA_VERSION"] = "11.8"

    # Update PATH
    cuda_bin = os.path.join(cuda_path, "bin")
    if cuda_bin not in os.environ["PATH"]:
        os.environ["PATH"] = cuda_bin + os.pathsep + os.environ["PATH"]

    # Set CUDA toolkit env vars
    os.environ["CUDACXX"] = os.path.join(cuda_bin, "nvcc.exe")
    os.environ["CUDA_TOOLKIT_ROOT_DIR"] = cuda_path

    return cuda_path


def reset_cuda_environment():
    """Reset and reconfigure CUDA environment"""
    try:
        # Set CUDA environment first
        cuda_path = set_cuda_env()
        logger.info(f"Set CUDA environment to version 11.8 at {cuda_path}")

        # Uninstall existing CUDA-dependent packages
        packages_to_remove = [
            "torch",
            "torchvision",
            "torchaudio",
            "cupy-cuda*",
            "pennylane-lightning-gpu",
            "stable-baselines3",  # Temporarily remove to avoid conflicts
        ]

        logger.info("Removing existing CUDA packages...")
        for package in packages_to_remove:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "uninstall", "-y", package],
                    check=False,
                )  # Don't check return code as some might not be installed
            except Exception as e:
                logger.warning(f"Error removing {package}: {e}")

        # Install specific CUDA 11.8 versions
        logger.info("Installing CUDA 11.8 compatible packages...")

        # Install PyTorch ecosystem
        torch_command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",  # Install without dependencies first to avoid conflicts
            "torch==2.1.0+cu118",
            "torchvision==0.16.0+cu118",
            "torchaudio==2.1.0+cu118",
            "--index-url",
            "https://download.pytorch.org/whl/cu118",
        ]
        subprocess.run(torch_command, check=True)

        # Install dependencies separately
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "filelock",
                "typing-extensions",
                "sympy",
                "networkx",
                "jinja2",
                "fsspec",
                "numpy",
                "pillow",
            ],
            check=True,
        )

        # Install CuPy section
        logger.info("Installing CuPy...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-cache-dir",  # Skip cache to force fresh download
                    "cupy-cuda118==11.6.0",  # Use specific older version known to work
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            logger.warning(
                "Failed to install CuPy via pip, trying alternative source..."
            )
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--no-cache-dir",
                        "--index-url",
                        "https://pypi.anaconda.org/skipper/simple",
                        "cupy-cuda118",
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError:
                logger.error(
                    "Could not install CuPy. Some GPU operations may be slower."
                )

        # Install PennyLane GPU components
        logger.info("Installing PennyLane components...")
        pennylane_command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "pennylane==0.33.0",
            "pennylane-lightning==0.33.0",
        ]
        subprocess.run(pennylane_command, check=True)

        # Install PennyLane GPU support separately
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "pennylane-lightning-gpu==0.33.0",
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            logger.warning(
                "Could not install pennylane-lightning-gpu. GPU acceleration for quantum operations may not be available."
            )

        # Reinstall stable-baselines3 with the correct torch version
        logger.info("Reinstalling stable-baselines3...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "stable-baselines3==2.5.0"],
            check=True,
        )

        # Verify installation
        logger.info("Verifying CUDA setup...")
        verify_command = [sys.executable, "validate_cuda.py"]
        subprocess.run(verify_command, check=True)

        return True

    except Exception as e:
        logger.error(f"Error resetting CUDA environment: {e}")
        return False


if __name__ == "__main__":
    print("\n=== Resetting AlgoTradPro5 CUDA Environment ===\n")
    success = reset_cuda_environment()
    sys.exit(0 if success else 1)
