"""Unit tests for system initialization"""

# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from unittest.mock import MagicMock, patch

import pytest

from src.core.initialize_system import (
    SystemInitializer,
    get_initialization_status,
    initialize_system,
)


@pytest.fixture
def system_initializer():
    """Fixture that provides a SystemInitializer instance"""
    return SystemInitializer()


def test_initialization_order(system_initializer):
    """Test system initialization order and dependencies"""
    with (
        patch(
            "src.core.initialize_system.validate_system_requirements"
        ) as mock_validate,
        patch("src.core.initialize_system.ensure_dependencies") as mock_deps,
        patch(
            "src.core.initialize_system.DocumentationValidator.validate_documentation"
        ) as mock_docs,
    ):
        # All validations pass
# REMOVED_UNUSED_CODE:         mock_validate.return_value = True
# REMOVED_UNUSED_CODE:         mock_deps.return_value = True
# REMOVED_UNUSED_CODE:         mock_docs.return_value = True

        assert system_initializer._validate_requirements() is True
        mock_validate.assert_called_once()
        mock_deps.assert_called_once()
        mock_docs.assert_called_once()


def test_core_component_initialization(system_initializer):
    """Test core component initialization"""
    with (
# REMOVED_UNUSED_CODE:         patch("src.core.initialize_system.ConfigManager.get_config") as mock_config,
        patch("src.core.initialize_system.DataManager") as mock_data,
        patch("src.core.initialize_system.SystemMonitor") as mock_monitor,
    ):
# REMOVED_UNUSED_CODE:         mock_config.return_value = {"test": "config"}

        assert system_initializer._initialize_core_components() is True
        assert "data_manager" in system_initializer.initialized_components
        assert "system_monitor" in system_initializer.initialized_components

        mock_data.assert_called_once()
        mock_monitor.assert_called_once_with({"test": "config"})


def test_model_initialization(system_initializer):
    """Test AI model initialization"""
    with (
# REMOVED_UNUSED_CODE:         patch("src.core.initialize_system.ConfigManager.get_config") as mock_config,
        patch("src.core.initialize_system.AIModelManager") as mock_ai,
# REMOVED_UNUSED_CODE:         patch("pathlib.Path.exists") as mock_exists,
    ):
# REMOVED_UNUSED_CODE:         mock_config.return_value = {"test": "config"}
# REMOVED_UNUSED_CODE:         mock_exists.return_value = True

        assert system_initializer._initialize_data_and_models() is True
        assert "model_manager" in system_initializer.initialized_components

        mock_ai.assert_called_once_with({"test": "config"})


def test_trading_component_initialization(system_initializer):
    """Test trading component initialization"""
    with (
# REMOVED_UNUSED_CODE:         patch("src.core.initialize_system.ConfigManager.get_config") as mock_config,
        patch("src.core.initialize_system.RiskManager") as mock_risk,
        patch("src.core.initialize_system.TradeJournal") as mock_journal,
    ):
# REMOVED_UNUSED_CODE:         mock_config.return_value = {"test": "config"}

        assert system_initializer._initialize_trading_components() is True
        assert "risk_manager" in system_initializer.initialized_components
        assert "trade_journal" in system_initializer.initialized_components

        mock_risk.assert_called_once_with({"test": "config"})
        mock_journal.assert_called_once()


def test_system_health_verification(system_initializer):
    """Test system health verification"""
    with patch(
        "src.core.initialize_system.SystemHealthChecker.check_system_health"
# REMOVED_UNUSED_CODE:     ) as mock_health:
        # Initialize required components
        system_initializer.initialized_components = {
            "data_manager",
            "error_manager",
            "system_monitor",
            "model_manager",
            "risk_manager",
            "trade_journal",
        }

# REMOVED_UNUSED_CODE:         mock_health.return_value = True
        assert system_initializer._verify_system_health() is True


def test_failed_initialization(system_initializer):
    """Test handling of initialization failures"""
    with patch(
        "src.core.initialize_system.validate_system_requirements"
    ) as mock_validate:
# REMOVED_UNUSED_CODE:         mock_validate.return_value = False
        assert system_initializer.initialize_system() is False
        assert not system_initializer.system_ready


def test_initialization_status():
    """Test initialization status reporting"""
    status = get_initialization_status()
    assert isinstance(status, dict)
    assert "system_ready" in status
    assert "initialized_components" in status
    assert "timestamp" in status
    assert "error_summary" in status


def test_global_initialization():
    """Test global initialization function"""
    with patch(
        "src.core.initialize_system.SystemInitializer.initialize_system"
    ) as mock_init:
# REMOVED_UNUSED_CODE:         mock_init.return_value = True
        assert initialize_system() is True
        mock_init.assert_called_once()
