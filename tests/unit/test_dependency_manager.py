"""
Unit Tests for Dependency Management System
========================================

Tests validate:
- Package validation
- CUDA verification
- Model availability
- System resources
- Docker installation
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import torch
import json

from src.core.dependency_manager import DependencyManager

@pytest.fixture
def mock_config():
    return {
        'models_path': 'C:/AlgoTradPro5/models',
        'data_path': 'C:/AlgoTradPro5/data'
    }

@pytest.fixture
def dependency_manager(mock_config):
    with patch('src.core.dependency_manager.get_config', return_value=mock_config):
        return DependencyManager()

# Add required fixtures
@pytest.fixture
def caplog():
    """Capture log messages"""
    return pytest.LogCaptureFixture()

@pytest.fixture
def mocker():
    """Provide mocker fixture"""
    return pytest.MockFixture()

def test_initialization(dependency_manager):
    """Test dependency manager initialization"""
    assert dependency_manager is not None
    assert dependency_manager.requirements['python_version'] == '>=3.9'
    assert dependency_manager.requirements['cuda_version'] == '>=11.0'

@patch('pkg_resources.require')
def test_validate_python_packages(mock_require, dependency_manager):
    """Test Python package validation"""
    # Mock successful validation
    mock_require.return_value = True
    assert dependency_manager.validate_python_packages() is True
    
    # Mock missing package
    mock_require.side_effect = Exception("Package not found")
    assert dependency_manager.validate_python_packages() is False

@patch('torch.cuda.is_available')
@patch('torch.version.cuda')
def test_validate_cuda(mock_cuda_version, mock_cuda_available, dependency_manager):
    """Test CUDA validation"""
    # Test CUDA available with valid version
    mock_cuda_available.return_value = True
    mock_cuda_version.return_value = "11.7"
    assert dependency_manager.validate_cuda() is True
    
    # Test CUDA available but version too low
    mock_cuda_version.return_value = "10.2"
    assert dependency_manager.validate_cuda() is False
    
    # Test CUDA not available
    mock_cuda_available.return_value = False
    assert dependency_manager.validate_cuda() is False

@patch('pathlib.Path.exists')
def test_validate_models(mock_exists, dependency_manager):
    """Test model validation"""
    # Test all models available
    mock_exists.return_value = True
    assert dependency_manager.validate_models() is True
    
    # Test models directory missing
    mock_exists.return_value = False
    assert dependency_manager.validate_models() is False

@patch('psutil.virtual_memory')
@patch('GPUtil.getGPUs')
def test_validate_system_resources(mock_gpus, mock_memory, dependency_manager):
    """Test system resource validation"""
    # Mock system memory
    mock_memory_info = MagicMock()
    mock_memory_info.total = 32 * (1024**3)  # 32GB
    mock_memory.return_value = mock_memory_info
    
    # Mock GPU
    mock_gpu = MagicMock()
    mock_gpu.memoryTotal = 16 * 1024  # 16GB
    mock_gpus.return_value = [mock_gpu]
    
    assert dependency_manager.validate_system_resources() is True
    
    # Test insufficient memory
    mock_memory_info.total = 8 * (1024**3)  # 8GB
    assert dependency_manager.validate_system_resources() is False

@patch('subprocess.run')
def test_validate_docker(mock_run, dependency_manager):
    """Test Docker validation"""
    # Mock successful docker commands
    mock_run.return_value = MagicMock(returncode=0)
    assert dependency_manager.validate_docker() is True
    
    # Mock docker not installed
    mock_run.return_value = MagicMock(returncode=1)
    assert dependency_manager.validate_docker() is False

def test_ensure_dependencies(dependency_manager, caplog):
    """Test overall dependency validation"""
    with patch.multiple(dependency_manager,
                       validate_python_packages=MagicMock(return_value=True),
                       validate_cuda=MagicMock(return_value=True),
                       validate_models=MagicMock(return_value=True),
                       validate_system_resources=MagicMock(return_value=True),
                       validate_docker=MagicMock(return_value=True)):
        assert dependency_manager.ensure_dependencies() is True
        
        # Test specific components
        assert dependency_manager.ensure_dependencies(['python', 'cuda']) is True
        
        # Test with invalid component
        dependency_manager.ensure_dependencies(['invalid_component'])
        assert 'Unknown component' in caplog.text

def test_cache_operations(dependency_manager, tmp_path, mocker):
    """Test dependency cache operations"""
    # Mock cache file
    cache_data = {'test': 'data'}
    cache_file = tmp_path / "dependency_cache.json"
    
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = True
        with patch('builtins.open', mocker.mock_open(read_data=json.dumps(cache_data))):
            dependency_manager._initialize_cache()
            assert dependency_manager.cache == cache_data
            
    # Test cache saving
    with patch('builtins.open', mocker.mock_open()) as mock_file:
        dependency_manager._save_cache()
        mock_file.assert_called_once()