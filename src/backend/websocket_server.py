"""
WebSocket server for AlgoTradePro5 backend.

This module implements the server-side WebSocket functionality for real-time data streaming.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Set

import socketio
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket_server")

class WebSocketServer:
    """WebSocket server for AlgoTradePro5."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        """Initialize the WebSocket server.
        
        Args:
            host: Host address to bind the server to
            port: Port to bind the server to
        """
        self.host = host
        self.port = port
        self.sio = socketio.AsyncServer(
            async_mode='aiohttp',
            cors_allowed_origins='*',
            pingInterval=25000,
            pingTimeout=5000
        )
        self.app = web.Application()
        self.sio.attach(self.app)
        self.clients: Dict[str, Dict[str, Any]] = {}
        self.channels: Dict[str, Set[str]] = {}
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        """Set up WebSocket event handlers."""
        @self.sio.event
        async def connect(sid, environ):
            """Handle client connection."""
            logger.info(f"Client connected: {sid}")
            self.clients[sid] = {
                "connected_at": asyncio.get_event_loop().time(),
                "subscriptions": set(),
                "authenticated": False,
                "user_id": None
            }
            await self.sio.emit('connection_success', {"status": "connected"}, room=sid)
        
        @self.sio.event
        async def disconnect(sid):
            """Handle client disconnection."""
            logger.info(f"Client disconnected: {sid}")
            # Clean up subscriptions
            if sid in self.clients:
                for channel in self.clients[sid]["subscriptions"]:
                    if channel in self.channels and sid in self.channels[channel]:
                        self.channels[channel].remove(sid)
                del self.clients[sid]
        
        @self.sio.event
        async def authenticate(sid, data):
            """Handle client authentication."""
            token = data.get("token")
            if not token:
                await self.sio.emit('auth_error', {"error": "No token provided"}, room=sid)
                return
            
            # Validate token (in a real implementation, you'd verify the JWT)
            if token == "valid_token":  # Replace with actual token validation
                self.clients[sid]["authenticated"] = True
                self.clients[sid]["user_id"] = "user123"  # Replace with actual user ID
                await self.sio.emit('auth_success', {"status": "authenticated"}, room=sid)
            else:
                await self.sio.emit('auth_error', {"error": "Invalid token"}, room=sid)
        
        @self.sio.event
        async def subscribe(sid, data):
            """Handle channel subscription."""
            if not self._check_authenticated(sid):
                await self.sio.emit('subscription_error', {"error": "Not authenticated"}, room=sid)
                return
            
            channel = data.get("channel")
            if not channel:
                await self.sio.emit('subscription_error', {"error": "No channel specified"}, room=sid)
                return
            
            # Add client to channel
            if channel not in self.channels:
                self.channels[channel] = set()
            self.channels[channel].add(sid)
            self.clients[sid]["subscriptions"].add(channel)
            
            await self.sio.emit('subscription_success', {
                "channel": channel,
                "status": "subscribed"
            }, room=sid)
            
            logger.info(f"Client {sid} subscribed to channel: {channel}")
        
        @self.sio.event
        async def unsubscribe(sid, data):
            """Handle channel unsubscription."""
            channel = data.get("channel")
            if not channel:
                await self.sio.emit('unsubscription_error', {"error": "No channel specified"}, room=sid)
                return
            
            # Remove client from channel
            if channel in self.channels and sid in self.channels[channel]:
                self.channels[channel].remove(sid)
                if sid in self.clients and channel in self.clients[sid]["subscriptions"]:
                    self.clients[sid]["subscriptions"].remove(channel)
                
                await self.sio.emit('unsubscription_success', {
                    "channel": channel,
                    "status": "unsubscribed"
                }, room=sid)
                
                logger.info(f"Client {sid} unsubscribed from channel: {channel}")
    
    def _check_authenticated(self, sid: str) -> bool:
        """Check if a client is authenticated.
        
        Args:
            sid: Client session ID
            
        Returns:
            bool: True if authenticated, False otherwise
        """
        return sid in self.clients and self.clients[sid]["authenticated"]
    
    async def broadcast(self, channel: str, event: str, data: Any):
        """Broadcast data to all clients subscribed to a channel.
        
        Args:
            channel: Channel to broadcast to
            event: Event name
            data: Data to send
        """
        if channel not in self.channels:
            logger.warning(f"Attempted to broadcast to non-existent channel: {channel}")
            return
        
        count = len(self.channels[channel])
        if count == 0:
            logger.info(f"No clients subscribed to channel: {channel}")
            return
        
        logger.info(f"Broadcasting to {count} clients on channel {channel}")
        for sid in self.channels[channel]:
            await self.sio.emit(event, data, room=sid)
    
    async def publish_market_data(self, market_data: Dict[str, Any]):
        """Publish market data to subscribed clients.
        
        Args:
            market_data: Market data to publish
        """
        await self.broadcast('market_update', 'market_update', market_data)
    
    async def publish_trade_update(self, trade_data: Dict[str, Any]):
        """Publish trade update to subscribed clients.
        
        Args:
            trade_data: Trade data to publish
        """
        await self.broadcast('trade_update', 'trade_update', trade_data)
    
    async def publish_system_status(self, status_data: Dict[str, Any]):
        """Publish system status to subscribed clients.
        
        Args:
            status_data: System status data to publish
        """
        await self.broadcast('system_status', 'system_status', status_data)
    
    async def start(self):
        """Start the WebSocket server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"WebSocket server started at ws://{self.host}:{self.port}")
        
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour
    
    def run(self):
        """Run the WebSocket server in the current event loop."""
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        finally:
            loop.close()


if __name__ == "__main__":
    server = WebSocketServer()
    server.run()