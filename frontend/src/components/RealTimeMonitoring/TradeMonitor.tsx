import React, { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Trade, WSMessage } from '@/types';
import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';

interface TradeMonitorProps {
  wsEndpoint: string;
}

export const RealTimeTradeMonitor: React.FC<TradeMonitorProps> = ({ wsEndpoint }) => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const { lastMessage, readyState, isConnected, error } = useWebSocket({
    url: wsEndpoint,
    onMessage: (message: WSMessage) => {
      if (message.type === 'trade') {
        setTrades(prev => [...prev, message.data as Trade].slice(-100));
      }
    }
  });

  return (
    <Card>
      <CardContent>
        <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="h6">Live Trades</Typography>
          {!isConnected && <CircularProgress size={20} />}
          {error && (
            <Typography color="error" variant="body2">
              Connection Error
            </Typography>
          )}
        </Box>
        
        {trades.length === 0 ? (
          <Typography color="text.secondary">No trades yet</Typography>
        ) : (
          <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
            {trades.map((trade) => (
              <Box key={trade.id} sx={{ mb: 1, p: 1, borderRadius: 1, bgcolor: 'background.paper' }}>
                <Typography variant="subtitle2">
                  {trade.pair} - {trade.type.toUpperCase()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Amount: {trade.amount} @ {trade.price}
                </Typography>
                {trade.profit !== undefined && (
                  <Typography
                    variant="body2"
                    color={trade.profit >= 0 ? 'success.main' : 'error.main'}
                  >
                    Profit: {trade.profit.toFixed(2)}%
                  </Typography>
                )}
              </Box>
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};