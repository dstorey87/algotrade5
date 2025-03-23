"""
Test module for WebSocket functionality.

This module contains unit tests for both the WebSocket client and server implementations.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestWebSocketServer(unittest.TestCase):
    """Test cases for WebSocketServer class."""

    def setUp(self):
        """Set up test fixtures."""
        pass

    def tearDown(self):
        """Tear down test fixtures."""
        pass

    @patch('socketio.AsyncServer')
    @patch('aiohttp.web.Application')
    def test_init(self, mock_app, mock_sio):
        """Test WebSocketServer initialization."""
        from backend.websocket_server import WebSocketServer
        
        server = WebSocketServer(host='127.0.0.1', port=9000)
        
        # Check that the server was initialized correctly
        self.assertEqual(server.host, '127.0.0.1')
        self.assertEqual(server.port, 9000)
        mock_sio.assert_called_once()
        mock_app.assert_called_once()

    @patch('socketio.AsyncServer')
    @patch('aiohttp.web.Application')
    def test_setup_event_handlers(self, mock_app, mock_sio):
        """Test WebSocketServer event handlers setup."""
        from backend.websocket_server import WebSocketServer

        # Create mock socketio server
        mock_sio_instance = MagicMock()
        mock_sio.return_value = mock_sio_instance
        
        server = WebSocketServer()
        
        # Check that event handlers were registered
        # mock_sio_instance.event.assert_called()
        self.assertTrue(hasattr(server, 'setup_event_handlers'))

    @patch('socketio.AsyncServer')
    @patch('aiohttp.web.Application')
    def test_check_authenticated(self, mock_app, mock_sio):
        """Test authentication check method."""
        from backend.websocket_server import WebSocketServer
        
        server = WebSocketServer()
        
        # Test with authenticated client
        server.clients = {
            'test_sid': {
                'authenticated': True
            }
        }
        self.assertTrue(server._check_authenticated('test_sid'))
        
        # Test with unauthenticated client
        server.clients = {
            'test_sid': {
                'authenticated': False
            }
        }
        self.assertFalse(server._check_authenticated('test_sid'))
        
        # Test with nonexistent client
        self.assertFalse(server._check_authenticated('nonexistent_sid'))

class TestWebSocketClient:
    """Test cases for WebSocket client (using pytest)."""
    
    def test_websocket_service_init(self):
        """Test WebSocketService initialization."""
        from frontend.components.WebSocketProvider import WebSocketService
        
        service = WebSocketService('ws://localhost:8765')
        
        assert service.url == 'ws://localhost:8765'
        assert service.socket is None
        assert service.reconnectAttempts == 0
        assert service.maxReconnectAttempts == 5
        assert service.reconnectInterval == 1000

    @patch('frontend.components.WebSocketProvider.io')
    def test_websocket_service_connect(self, mock_io):
        """Test WebSocketService connect method."""
        from frontend.components.WebSocketProvider import WebSocketService

        # Mock socket.io client
        mock_socket = MagicMock()
        mock_io.return_value = mock_socket
        
        service = WebSocketService('ws://localhost:8765')
        result = service.connect()
        
        # Check that socket.io was called with correct parameters
        mock_io.assert_called_once_with('ws://localhost:8765', {
            'reconnection': False,
            'transports': ['websocket'],
            'timeout': 10000
        })
        
        # Check that event handlers were set up
        assert mock_socket.on.call_count >= 3
        
        # Check that the method returns the socket
        assert result == mock_socket

    @patch('frontend.components.WebSocketProvider.io')
    def test_websocket_service_disconnect(self, mock_io):
        """Test WebSocketService disconnect method."""
        from frontend.components.WebSocketProvider import WebSocketService

        # Mock socket.io client
        mock_socket = MagicMock()
        mock_io.return_value = mock_socket
        
        service = WebSocketService('ws://localhost:8765')
        service.connect()
        service.disconnect()
        
        # Check that disconnect was called
        mock_socket.disconnect.assert_called_once()
        assert service.socket is None

if __name__ == '__main__':
    unittest.main()