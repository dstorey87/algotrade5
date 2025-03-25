import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { TradeStats as TradeStatsType } from '@/types/trade';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import TimelineIcon from '@mui/icons-material/Timeline';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color?: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color = 'primary.main' }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
      <Box sx={{ color, mr: 1 }}>{icon}</Box>
      <Typography variant="subtitle2" color="text.secondary">
        {title}
      </Typography>
    </Box>
    <Typography variant="h4" component="div">
      {value}
    </Typography>
  </Paper>
);

interface TradeStatsProps {
  stats: TradeStatsType;
}

export const TradeStats: React.FC<TradeStatsProps> = ({ stats }) => {
  return (
    <Grid container spacing={2}>
      <Grid item xs={3}>
        <StatCard
          title="Total Trades"
          value={stats.totalTrades}
          icon={<TimelineIcon />}
        />
      </Grid>
      <Grid item xs={3}>
        <StatCard
          title="Win Rate"
          value={`${stats.winRate.toFixed(1)}%`}
          icon={<TrendingUpIcon />}
          color={stats.winRate >= 50 ? 'success.main' : 'error.main'}
        />
      </Grid>
      <Grid item xs={3}>
        <StatCard
          title="Profit/Loss"
          value={`${stats.profitLoss >= 0 ? '+' : ''}${stats.profitLoss.toFixed(2)}%`}
          icon={<ShowChartIcon />}
          color={stats.profitLoss >= 0 ? 'success.main' : 'error.main'}
        />
      </Grid>
      <Grid item xs={3}>
        <StatCard
          title="Max Drawdown"
          value={`${stats.drawdown.toFixed(2)}%`}
          icon={<TrendingDownIcon />}
          color="error.main"
        />
      </Grid>
    </Grid>
  );
};