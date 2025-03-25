import React from 'react';
import { Box, Grid, Typography } from '@mui/material';
import { TradeStats as TradeStatsType } from '@/types/trade';

interface TradeStatsProps {
  stats: TradeStatsType;
}

export const TradeStats: React.FC<TradeStatsProps> = ({ stats }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value / 100);
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={3}>
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Total Trades
          </Typography>
          <Typography variant="h6">
            {stats.totalTrades}
          </Typography>
        </Box>
      </Grid>
      
      <Grid item xs={3}>
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Win Rate
          </Typography>
          <Typography variant="h6">
            {formatPercentage(stats.winRate)}
          </Typography>
        </Box>
      </Grid>
      
      <Grid item xs={3}>
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Profit/Loss
          </Typography>
          <Typography 
            variant="h6" 
            sx={{ color: stats.profitLoss >= 0 ? 'success.main' : 'error.main' }}
          >
            {formatCurrency(stats.profitLoss)}
          </Typography>
        </Box>
      </Grid>
      
      <Grid item xs={3}>
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Max Drawdown
          </Typography>
          <Typography 
            variant="h6" 
            sx={{ color: 'error.main' }}
          >
            {formatPercentage(stats.drawdown)}
          </Typography>
        </Box>
      </Grid>
    </Grid>
  );
};