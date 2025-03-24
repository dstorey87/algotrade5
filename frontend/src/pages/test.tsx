import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import { TradeMonitor } from '@/components/RealTimeMonitoring/TradeMonitor';
import websocketService from '@/services/websocket';

// Mock data generator for testing the components
function generateMockTrades(count: number) {
  const pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT'];
  const types = ['buy', 'sell'];
  
  return Array.from({ length: count }, (_, i) => ({
    id: `trade-${i}`,
    pair: pairs[Math.floor(Math.random() * pairs.length)],
    type: types[Math.floor(Math.random() * types.length)] as 'buy' | 'sell',
    amount: Math.random() * 0.5,
    price: 20000 + Math.random() * 10000,
    timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
    status: Math.random() > 0.3 ? 'open' : 'closed',
    profit: Math.random() > 0.4 ? Math.random() * 5 : -Math.random() * 3,
    strategy: 'quantum-ml-hybrid',
    confidence: 0.7 + Math.random() * 0.3
  }));
}

// Mock WebSocket messages for simulating real-time updates
function simulateWebSocketActivity() {
  // Simulate receiving trade updates
  setInterval(() => {
    const mockMessage = {
      type: 'trade_update',
      data: generateMockTrades(10)[0],
      timestamp: new Date().toISOString()
    };
    
    // Use our compression implementation
    const event = {
      data: JSON.stringify(mockMessage)
    } as unknown as MessageEvent;
    
    // Call the handler directly to simulate WebSocket message
    // @ts-ignore - private method access for testing
    websocketService.handleMessage(event);
  }, 1000); // Simulate one update per second
}

export default function TestPage() {
  React.useEffect(() => {
    // Initialize mock data in the Redux store
    // This would normally happen through API calls or WebSocket
    
    // Start simulating WebSocket activity
    simulateWebSocketActivity();
    
    // Cleanup function
    return () => {
      // Clear any intervals or timers
    };
  }, []);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          AlgoTradePro5 Performance Test
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          This page demonstrates the optimized real-time monitoring components with simulated data.
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <TradeMonitor />
        </Box>
      </Box>
    </Container>
  );
}