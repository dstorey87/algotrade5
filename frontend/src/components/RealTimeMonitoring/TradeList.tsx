import React, { useMemo } from 'react';
import { Box, List, ListItem, ListItemText, Typography } from '@mui/material';
import { Trade } from '@/types/trade';
import { format } from 'date-fns';

interface TradeListProps {
  trades: Trade[];
}

export const TradeList: React.FC<TradeListProps> = ({ trades }) => {
  const sortedTrades = useMemo(() => {
    return [...trades].sort((a, b) => b.timestamp - a.timestamp).slice(0, 100);
  }, [trades]);

  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 2,
      maximumFractionDigits: 6
    }).format(amount);
  };

  return (
    <Box sx={{ 
      height: '100%', 
      overflow: 'auto',
      '&::-webkit-scrollbar': {
        width: '8px',
      },
      '&::-webkit-scrollbar-track': {
        background: 'transparent',
      },
      '&::-webkit-scrollbar-thumb': {
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '4px',
      },
    }}>
      <List disablePadding>
        {sortedTrades.map((trade) => (
          <ListItem 
            key={trade.id}
            sx={{ 
              py: 1,
              borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
              '&:last-child': { borderBottom: 'none' }
            }}
          >
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                    {trade.pair}
                  </Typography>
                  <Typography 
                    variant="body2"
                    sx={{ 
                      color: trade.type === 'buy' ? 'success.main' : 'error.main',
                      fontWeight: 'medium'
                    }}
                  >
                    {trade.type.toUpperCase()}
                  </Typography>
                </Box>
              }
              secondary={
                <Box sx={{ mt: 0.5 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2" color="text.secondary">
                      Amount
                    </Typography>
                    <Typography variant="body2">
                      {formatAmount(trade.amount)}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2" color="text.secondary">
                      Price
                    </Typography>
                    <Typography variant="body2">
                      {formatAmount(trade.price)}
                    </Typography>
                  </Box>
                  {trade.profitLoss !== undefined && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">
                        P/L
                      </Typography>
                      <Typography 
                        variant="body2"
                        sx={{ 
                          color: trade.profitLoss >= 0 ? 'success.main' : 'error.main',
                          fontWeight: 'medium'
                        }}
                      >
                        {formatAmount(trade.profitLoss)}
                      </Typography>
                    </Box>
                  )}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
                    <Typography variant="caption" color="text.secondary">
                      {format(trade.timestamp, 'HH:mm:ss')}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {trade.strategy}
                    </Typography>
                  </Box>
                </Box>
              }
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};