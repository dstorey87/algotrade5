"""
AI Model Setup Script
=================

CRITICAL REQUIREMENTS:
- HuggingFace model downloads
- Model validation
- Version tracking
- Memory optimization

SETUP SEQUENCE:
1. Environment validation
2. Model downloads
3. Validation checks
4. Optimization

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

# REMOVED_UNUSED_CODE: import hashlib
import json
import logging
# REMOVED_UNUSED_CODE: import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Dict, List, Optional

# REMOVED_UNUSED_CODE: import torch
# REMOVED_UNUSED_CODE: from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.config_manager import get_config
from core.error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)


class ModelSetup:
    """AI model setup and validation"""

    def __init__(self):
        """Initialize model setup"""
        self.error_manager = ErrorManager()
        self.config = get_config()

        # Load model configuration
        self.models_path = Path(
            self.config.get("models_path", "C:/AlgoTradPro5/models")
        )
        self.models_config = self._load_models_config()

        # Setup status
        self.setup_status: Dict[str, bool] = {}
        self.model_info: Dict = {}

        # Model categories
        self.categories = ["llm", "ml", "quantum"]

    def setup(self) -> bool:
        """
        Run model setup process

        Returns:
            bool: True if setup successful
        """
        try:
            logger.info("Starting model setup process...")

            # 1. Prepare directories
            if not self._prepare_directories():
                return False

            # 2. Download models
            if not self._download_models():
                return False

            # 3. Validate models
            if not self._validate_models():
                return False

            # 4. Optimize storage
            if not self._optimize_storage():
                return False

            logger.info("✅ Model setup complete")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Model setup failed: {e}", ErrorSeverity.CRITICAL.value, "Models"
            )
            return False

    def _load_models_config(self) -> Dict:
        """Load model configuration"""
        config_path = self.models_path / "config.json"

        if not config_path.exists():
            # Create default configuration
            default_config = {
                "models": {
                    "llm": [
                        {
                            "name": "phi-2",
                            "repo": "microsoft/phi-2",
                            "type": "pytorch",
                            "required": True,
                        },
                        {
                            "name": "mixtral",
                            "repo": "mistralai/Mixtral-8x7B-v0.1",
                            "type": "pytorch",
                            "required": False,
                        },
                    ],
                    "ml": [
                        {
                            "name": "quantum_base",
                            "repo": "local/quantum_base",
                            "type": "pytorch",
                            "required": True,
                        }
                    ],
                    "quantum": [
                        {
                            "name": "q_optimizer",
                            "repo": "local/q_optimizer",
                            "type": "pytorch",
                            "required": True,
                        }
                    ],
                },
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
            }

            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)

            return default_config

        with open(config_path) as f:
            return json.load(f)

    def _prepare_directories(self) -> bool:
        """Prepare model directories"""
        try:
            # Create category directories
            for category in self.categories:
                category_path = self.models_path / category
                category_path.mkdir(parents=True, exist_ok=True)

            self.setup_status["directories"] = True
            logger.info("✅ Model directories prepared")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Directory preparation failed: {e}", ErrorSeverity.HIGH.value, "Models"
            )
            return False

    def _download_models(self) -> bool:
        """Download required models"""
        try:
            from huggingface_hub import snapshot_download

            # Track successful downloads
            downloaded = []

            # Process each category
            for category in self.categories:
                if category not in self.models_config["models"]:
                    continue

                for model in self.models_config["models"][category]:
                    try:
                        if model["type"] != "pytorch":
                            continue

                        model_path = self.models_path / category / model["name"]

                        # Skip if already downloaded
                        if model_path.exists() and list(model_path.glob("*.bin")):
                            logger.info(f"Model {model['name']} already exists")
                            downloaded.append(model["name"])
                            continue

                        # Download from HuggingFace
                        if not model["repo"].startswith("local/"):
                            logger.info(f"Downloading {model['name']}...")
                            snapshot_download(
                                repo_id=model["repo"],
                                local_dir=model_path,
                                local_dir_use_symlinks=False,
                            )
                            downloaded.append(model["name"])

                    except Exception as e:
                        if model.get("required", False):
                            raise RuntimeError(
                                f"Failed to download required model {model['name']}: {e}"
                            )
                        else:
                            logger.warning(
                                f"Failed to download optional model {model['name']}: {e}"
                            )

            self.model_info["downloaded"] = downloaded
            self.setup_status["downloads"] = True
            logger.info(f"✅ Downloaded {len(downloaded)} models")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Model download failed: {e}", ErrorSeverity.HIGH.value, "Models"
            )
            return False

    def _validate_models(self) -> bool:
        """Validate downloaded models"""
        try:
            validated = []

            for category in self.categories:
                category_path = self.models_path / category
                if not category_path.exists():
                    continue

                for model_dir in category_path.iterdir():
                    if not model_dir.is_dir():
                        continue

                    try:
                        # Check for required files
                        if not list(model_dir.glob("*.bin")):
                            raise ValueError("No model weights found")

                        # Load and validate config
                        config_file = model_dir / "config.json"
                        if config_file.exists():
                            with open(config_file) as f:
                                config = json.load(f)

                            # Store model details
                            self.model_info[model_dir.name] = {
                                "config": config,
                                "size": sum(
                                    f.stat().st_size for f in model_dir.glob("*")
                                ),
                                "files": len(list(model_dir.glob("*"))),
                                "validated": datetime.now().isoformat(),
                            }

                        validated.append(model_dir.name)

                    except Exception as e:
                        logger.warning(f"Validation failed for {model_dir.name}: {e}")

            self.model_info["validated"] = validated
            self.setup_status["validation"] = True
            logger.info(f"✅ Validated {len(validated)} models")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Model validation failed: {e}", ErrorSeverity.HIGH.value, "Models"
            )
            return False

    def _optimize_storage(self) -> bool:
        """Optimize model storage"""
        try:
            optimized = []

            for category in self.categories:
                category_path = self.models_path / category
                if not category_path.exists():
                    continue

                for model_dir in category_path.iterdir():
                    if not model_dir.is_dir():
                        continue

                    try:
                        # Remove unnecessary files
                        for pattern in ["*.md", "*.txt", "*.git*"]:
                            for f in model_dir.glob(pattern):
                                f.unlink()

                        # Clean cache files
                        cache_dir = model_dir / ".cache"
                        if cache_dir.exists():
                            shutil.rmtree(cache_dir)

                        optimized.append(model_dir.name)

                    except Exception as e:
                        logger.warning(f"Optimization failed for {model_dir.name}: {e}")

            self.model_info["optimized"] = optimized
            self.setup_status["optimization"] = True
            logger.info(f"✅ Optimized {len(optimized)} models")
            return True

        except Exception as e:
            self.error_manager.log_error(
                f"Storage optimization failed: {e}",
                ErrorSeverity.MEDIUM.value,
                "Models",
            )
            return False

    def get_setup_status(self) -> Dict:
        """Get current setup status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "status": all(self.setup_status.values()),
            "steps": self.setup_status.copy(),
            "model_info": self.model_info.copy(),
        }

# REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE:         """Cleanup temporary files"""
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Clean temporary downloads
# REMOVED_UNUSED_CODE:             temp_dir = self.models_path / "temp"
# REMOVED_UNUSED_CODE:             if temp_dir.exists():
# REMOVED_UNUSED_CODE:                 shutil.rmtree(temp_dir)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.info("Model setup cleanup complete")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             self.error_manager.log_error(
# REMOVED_UNUSED_CODE:                 f"Model cleanup failed: {e}", ErrorSeverity.MEDIUM.value, "Models"
# REMOVED_UNUSED_CODE:             )


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Run setup
    setup = ModelSetup()
    success = setup.setup()

    if success:
        print("\n✅ Model setup completed successfully!")
        status = setup.get_setup_status()
        print("\nModel Information:")
        print(f"Downloaded: {len(status['model_info'].get('downloaded', []))}")
        print(f"Validated: {len(status['model_info'].get('validated', []))}")
        print(f"Optimized: {len(status['model_info'].get('optimized', []))}")
    else:
        print("\n❌ Model setup failed - check logs for details")
        sys.exit(1)
