import os
from pathlib import Path

import pytest

from src.core.config_manager import ConfigManager


def test_config_manager_initialization():
    config = ConfigManager()
    assert config is not None


def test_db_url_construction():
    config = ConfigManager()
    db_url = config.get_db_url()
    assert "postgresql://" in db_url
    assert os.getenv("DB_USER") in db_url


def test_model_paths_validation():
    config = ConfigManager()
    paths = config.get_model_paths()
    assert Path(paths["base"]).exists()
    assert Path(paths["llm"]).exists()
    assert Path(paths["ml"]).exists()


def test_trade_limits():
    config = ConfigManager()
    limits = config.get_trade_limits()
    assert "max_open_trades" in limits
    assert "stake_amount" in limits
    assert "max_drawdown" in limits
