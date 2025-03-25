import React from 'react';
import { Box, List, ListItem, ListItemText, Typography } from '@mui/material';
import { Trade } from '@/types/trade';

interface TradeListProps {
  trades: Trade[];
}

export const TradeList: React.FC<TradeListProps> = ({ trades }) => {
  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const formatProfit = (profit?: number) => {
    if (profit === undefined) return '--';
    return `${profit >= 0 ? '+' : ''}${profit.toFixed(2)}%`;
  };

  return (
    <List sx={{ height: '100%', overflow: 'auto' }}>
      {trades.slice().reverse().map((trade) => (
        <ListItem 
          key={trade.id}
          sx={{
            borderLeft: 4,
            borderColor: trade.type === 'buy' ? 'success.main' : 'error.main',
            mb: 1,
            bgcolor: 'background.paper',
          }}
        >
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="subtitle1">{trade.pair}</Typography>
                <Typography 
                  variant="subtitle1"
                  color={trade.profitLoss && trade.profitLoss >= 0 ? 'success.main' : 'error.main'}
                >
                  {formatProfit(trade.profitLoss)}
                </Typography>
              </Box>
            }
            secondary={
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2">
                  {trade.type.toUpperCase()} @ {trade.price}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formatTimestamp(trade.timestamp)}
                </Typography>
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};