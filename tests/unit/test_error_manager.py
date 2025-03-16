"""Unit tests for error management"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from src.core.error_manager import (
    ErrorLog,
    ErrorManager,
    ErrorSeverity,
    get_error_summary,
    log_error,
)


@pytest.fixture
def error_manager():
    """Fixture that provides an ErrorManager instance"""
    return ErrorManager()


@pytest.fixture
def test_db_path(tmp_path):
    """Create a temporary database path"""
    return tmp_path / "errors.db"


def test_error_severity_enum():
    """Test error severity enum values"""
    assert ErrorSeverity.LOW.value == "LOW"
    assert ErrorSeverity.MEDIUM.value == "MEDIUM"
    assert ErrorSeverity.HIGH.value == "HIGH"
    assert ErrorSeverity.CRITICAL.value == "CRITICAL"


def test_error_log_creation():
    """Test error log data class"""
    error = ErrorLog(
        timestamp=datetime.now().isoformat(),
        message="Test error",
        severity=ErrorSeverity.HIGH.value,
        component="test",
        trace="test trace",
    )
    assert error.message == "Test error"
    assert error.severity == ErrorSeverity.HIGH.value
    assert not error.handled
    assert error.trace == "test trace"


def test_error_logging(error_manager):
    """Test basic error logging"""
    error_manager.log_error(
        "Test error", ErrorSeverity.HIGH.value, "TestComponent", "Test trace"
    )

    # Check error history
    assert len(error_manager.error_history) == 1
    latest = error_manager.error_history[0]
    assert latest.message == "Test error"
    assert latest.severity == ErrorSeverity.HIGH.value
    assert latest.component == "TestComponent"


def test_critical_error_threshold(error_manager):
    """Test critical error threshold handling"""
    # Log multiple critical errors
    for i in range(error_manager.max_critical_errors):
        error_manager.log_error(
            f"Critical error {i}", ErrorSeverity.CRITICAL.value, "TestComponent"
        )

    assert error_manager.critical_errors == error_manager.max_critical_errors


def test_error_database(error_manager, tmp_path):
    """Test error database operations"""
    # Log some errors
    error_manager.log_error(
        "Database test error", ErrorSeverity.MEDIUM.value, "Database"
    )

    # Check database content
    with sqlite3.connect(error_manager.error_db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM error_logs")
        rows = c.fetchall()
        assert len(rows) > 0


def test_error_summary(error_manager):
    """Test error summary generation"""
    # Log different types of errors
    error_manager.log_error("Low severity error", ErrorSeverity.LOW.value, "Component1")
    error_manager.log_error(
        "High severity error", ErrorSeverity.HIGH.value, "Component2"
    )
    error_manager.log_error(
        "Critical error", ErrorSeverity.CRITICAL.value, "Component1"
    )

    summary = error_manager.get_error_summary()
    assert "severity_distribution" in summary
    assert "component_distribution" in summary
    assert summary["total_errors"] == len(error_manager.error_history)


def test_mark_error_handled(error_manager):
    """Test marking errors as handled"""
    # Log an error
    timestamp = datetime.now().isoformat()
    error_manager.log_error(
        "Test error", ErrorSeverity.HIGH.value, "TestComponent", timestamp=timestamp
    )

    # Mark as handled
    result = error_manager.mark_error_handled(timestamp, "Error resolved by test")
    assert result is True


def test_clear_error_history(error_manager):
    """Test clearing old error history"""
    # Log some errors
    error_manager.log_error("Old error", ErrorSeverity.LOW.value, "TestComponent")

    # Clear history
    result = error_manager.clear_error_history(days_to_keep=1)
    assert result is True


def test_global_functions():
    """Test global helper functions"""
    # Test global error logging
    log_error("Global test error", ErrorSeverity.MEDIUM.value, "TestComponent")

    # Test global summary
    summary = get_error_summary()
    assert isinstance(summary, dict)
    assert "severity_distribution" in summary
