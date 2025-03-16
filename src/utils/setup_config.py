#!/usr/bin/env python3
"""Setup script for AlgoTradPro5 configuration"""

import json
import os
import secrets
import shutil
from pathlib import Path

from freqtrade.configuration.configuration import Configuration
from freqtrade.configuration.directory_operations import create_userdata_dir
from freqtrade.configuration.load_config import load_config_file
from freqtrade.util.template_renderer import render_template


def setup_configuration(strategy_name: str = "QuantumHybridStrategy") -> None:
    """Generate configuration from template"""
    template_path = Path("freqtrade/templates/quantum_strategy.json.j2")
    config_path = Path("freqtrade/config.json")

    # Generate random strings for security
    context = {"strategy": strategy_name, "random_string": secrets.token_hex(32)}

    # Render template with context
    config_text = render_template(template_path.read_text(), context)

    # Save configuration
    config_path.write_text(config_text)
    print(f"Configuration generated at {config_path}")

    # Create user data directory structure
    create_userdata_dir(str(config_path.parent), "user_data")

    # Validate configuration
    config = Configuration.from_files([str(config_path)])
    config.validate()
    print("Configuration validated successfully")


if __name__ == "__main__":
    setup_configuration()
