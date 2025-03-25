import React, { useEffect, useState, useCallback } from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { useWebSocket } from '@/hooks/useWebSocket';
import { TradeList } from '../TradeList';
import { TradeStats } from '../TradeStats';
import { TradeChart } from '../TradeChart';
import { Trade, TradeStats as TradeStatsType } from '@/types/trade';

export const TradeMonitor: React.FC = () => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [stats, setStats] = useState<TradeStatsType>({
    totalTrades: 0,
    winRate: 0,
    profitLoss: 0,
    drawdown: 0
  });

  const handleMessage = useCallback((message: any) => {
    if (message.type === 'trade') {
      setTrades(prev => [...prev, message.data]);
    } else if (message.type === 'stats') {
      setStats(message.data);
    }
  }, []);

  const { lastMessage, sendMessage, connectionStatus } = useWebSocket({
    url: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080/ws',
    onMessage: handleMessage
  });

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Trade Monitor
          <Typography 
            component="span" 
            sx={{ 
              ml: 2,
              color: connectionStatus === 'connected' ? 'success.main' : 'error.main'
            }}
          >
            {connectionStatus === 'connected' ? 'Connected' : 'Disconnected'}
          </Typography>
        </Typography>
        <TradeStats stats={stats} />
      </Paper>
      
      <Box sx={{ flex: 1, minHeight: 0, display: 'flex', gap: 2 }}>
        <Paper sx={{ flex: 1, p: 2, display: 'flex', flexDirection: 'column' }}>
          <Typography variant="h6" gutterBottom>Trade Activity</Typography>
          <Box sx={{ flex: 1, minHeight: 0 }}>
            <TradeChart trades={trades} />
          </Box>
        </Paper>
        
        <Paper sx={{ width: 400, p: 2, display: 'flex', flexDirection: 'column' }}>
          <Typography variant="h6" gutterBottom>Recent Trades</Typography>
          <Box sx={{ flex: 1, minHeight: 0 }}>
            <TradeList trades={trades} />
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};