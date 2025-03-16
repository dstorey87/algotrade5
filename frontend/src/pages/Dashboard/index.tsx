import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Grid, Paper, Typography, Box, Card, CardContent, Divider, useTheme } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TimelineIcon from '@mui/icons-material/Timeline';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import PercentIcon from '@mui/icons-material/Percent';
import { ResponsiveLine } from '@nivo/line';
import { ResponsivePie } from '@nivo/pie';

import { RootState } from '../../store';
import { fetchDashboardData, fetchTradeData } from '../../store/slices/tradingSlice';
import TradingControls from '../../components/TradingControls';
import StrategyStats from '../../components/StrategyStats';
import TradeLog from '../../components/TradeLog';

// Metric card component for displaying individual metrics
const MetricCard = ({ title, value, icon, change, color }: { title: string, value: string, icon: React.ReactNode, change?: string, color?: string }) => {
  const theme = useTheme();

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Box sx={{
            p: 1,
            borderRadius: 1,
            mr: 2,
            bgcolor: color || theme.palette.primary.main,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            {icon}
          </Box>
          <Typography variant="h6" color="textSecondary">{title}</Typography>
        </Box>
        <Typography variant="h4" component="div" sx={{ my: 2, fontWeight: 'bold' }}>
          {value}
        </Typography>
        {change && (
          <Box sx={{
            display: 'flex',
            alignItems: 'center',
            color: change.startsWith('+') ? 'success.main' : 'error.main'
          }}>
            {change.startsWith('+') ? <TrendingUpIcon fontSize="small" /> : <TrendingDownIcon fontSize="small" />}
            <Typography variant="body2" sx={{ ml: 0.5 }}>
              {change} since yesterday
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const { dashboardData, loading } = useSelector((state: RootState) => state.trading);

  useEffect(() => {
    dispatch(fetchDashboardData() as any);
  }, [dispatch]);

  useEffect(() => {
    // Fetch initial data
    dispatch(fetchTradeData() as any)

    // Set up polling for updates every 5 seconds
    const interval = setInterval(() => {
      dispatch(fetchTradeData() as any)
    }, 5000)

    return () => clearInterval(interval)
  }, [dispatch])

  // Placeholder data for charts
  const equityCurveData = [
    {
      id: 'equity',
      color: theme.palette.primary.main,
      data: [
        { x: '2023-01-01', y: 10 },
        { x: '2023-01-02', y: 12 },
        { x: '2023-01-03', y: 11 },
        { x: '2023-01-04', y: 15 },
        { x: '2023-01-05', y: 18 },
        { x: '2023-01-06', y: 17 },
        { x: '2023-01-07', y: 22 },
      ],
    },
  ];

  const strategyPerformanceData = [
    { id: 'BTC/USDT', label: 'BTC/USDT', value: 35, color: theme.palette.primary.main },
    { id: 'ETH/USDT', label: 'ETH/USDT', value: 25, color: theme.palette.secondary.main },
    { id: 'SOL/USDT', label: 'SOL/USDT', value: 20, color: theme.palette.success.main },
    { id: 'DOT/USDT', label: 'DOT/USDT', value: 15, color: theme.palette.warning.main },
    { id: 'DOGE/USDT', label: 'DOGE/USDT', value: 5, color: theme.palette.error.main },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Trading Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Trading Controls */}
        <Grid item xs={12}>
          <TradingControls />
        </Grid>

        {/* Strategy Stats */}
        <Grid item xs={12} md={4}>
          <StrategyStats />
        </Grid>

        {/* Trade Log */}
        <Grid item xs={12} md={8}>
          <TradeLog />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
