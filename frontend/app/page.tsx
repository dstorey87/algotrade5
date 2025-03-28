'use client';

import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Container, 
  Grid, 
  Paper, 
  Card, 
  CardContent,
  Button,
  LinearProgress,
  Alert
} from '@mui/material';

// Simple logger for development
const logger = {
  info: (message: string, data?: any) => console.info(`[INFO] ${message}`, data || ''),
  debug: (message: string, data?: any) => console.debug(`[DEBUG] ${message}`, data || ''),
  error: (message: string, data?: any) => console.error(`[ERROR] ${message}`, data || '')
};

/**
 * Home Page Component for AlgoTradePro5 Dashboard
 */
export default function Home() {
  const [loading, setLoading] = useState(true);

  // Simple initialization effect 
  useEffect(() => {
    logger.info('Dashboard page mounted', { route: '/' });
    
    // Simple timeout to ensure the page loads
    const timer = setTimeout(() => {
      setLoading(false);
    }, 500);
    
    return () => {
      clearTimeout(timer);
      logger.debug('Dashboard page unmounted');
    };
  }, []);

  if (loading) {
    return (
      <Container maxWidth="sm" sx={{ mt: 10, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#3f8cff' }}>
          AlgoTradePro5
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <LinearProgress sx={{ width: '50%' }} />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Page Header */}
      <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
        AlgoTradePro5 Dashboard
      </Typography>
      
      <Typography variant="subtitle1" gutterBottom sx={{ mb: 4 }}>
        AI-driven cryptocurrency trading system with quantum loop backtesting
      </Typography>
      
      {/* Summary Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Initial Investment Card */}
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h5" color="primary">£10.00</Typography>
              <Typography variant="body2" color="textSecondary">Initial Investment</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Current Balance Card */}
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h5" color="primary">£0.00</Typography>
              <Typography variant="body2" color="textSecondary">Current Balance</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Profit/Loss Card */}
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h5" color="error">0.00%</Typography>
              <Typography variant="body2" color="textSecondary">Profit/Loss</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Win/Loss Ratio Card */}
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h5" color="primary">0/0</Typography>
              <Typography variant="body2" color="textSecondary">Win/Loss Ratio</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Real-Time Trade Monitor Panel */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Real-Time Trade Monitoring</Typography>
            <Alert 
              severity="info" 
              sx={{ my: 2 }}
              action={
                <Button 
                  color="inherit" 
                  size="small" 
                  onClick={() => {
                    logger.info('User clicked to connect trading server');
                    alert('Trading connection feature will be available in the next update');
                  }}
                >
                  CONNECT
                </Button>
              }
            >
              Real-time trade monitoring is available when a trading server is connected.
              <Typography variant="body2" sx={{ mt: 1 }}>
                Use the FreqTrade REST API endpoint to monitor live trading.
              </Typography>
            </Alert>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
              <Box>
                <Typography variant="body2" color="textSecondary">Signal Status</Typography>
                <Typography variant="body1">No Active Signals</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="textSecondary">Last Update</Typography>
                <Typography variant="body1">{new Date().toLocaleTimeString()}</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="textSecondary">API Status</Typography>
                <Typography variant="body1" color="error">Disconnected</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      {/* Main Dashboard Content */}
      <Grid container spacing={3}>
        {/* AI Strategy Status Panel */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>AI Strategy Status</Typography>
            
            {/* Quantum Loop Progress Bar */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Quantum Loop Progress
              </Typography>
              <LinearProgress variant="determinate" value={0} sx={{ height: 10, borderRadius: 5 }} />
              <Typography variant="caption" color="textSecondary" align="right" display="block">
                0%
              </Typography>
            </Box>
            
            {/* Strategy Status Indicators */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Strategy Generation:</Typography>
              <Typography variant="body2" color="textSecondary">Initializing</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Backtesting Status:</Typography>
              <Typography variant="body2" color="textSecondary">Pending</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">LLM Analysis:</Typography>
              <Typography variant="body2" color="textSecondary">Ready</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Trading Status:</Typography>
              <Typography variant="body2" color="error">Offline</Typography>
            </Box>
            
            {/* Action Button */}
            <Button variant="contained" color="primary" sx={{ mt: 2 }}>
              Initialize Trading
            </Button>
          </Paper>
        </Grid>
        
        {/* Recent Activity Panel */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Typography variant="h6" gutterBottom>Recent Activity</Typography>
            
            <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
              No recent trading activity to display. Start trading to view performance metrics and transaction history.
            </Typography>
            
            <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Button variant="outlined" color="primary">
                View Trading History
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        {/* System Status Panel */}
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>System Status</Typography>
            
            <Grid container spacing={2}>
              {/* FreqTrade Status */}
              <Grid item xs={12} sm={4}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">FreqTrade:</Typography>
                  <Typography variant="body2" color="error">Offline</Typography>
                </Box>
              </Grid>
              
              {/* AI Models Status */}
              <Grid item xs={12} sm={4}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">AI Models:</Typography>
                  <Typography variant="body2" color="success.main">Online</Typography>
                </Box>
              </Grid>
              
              {/* Database Status */}
              <Grid item xs={12} sm={4}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Database:</Typography>
                  <Typography variant="body2" color="success.main">Connected</Typography>
                </Box>
              </Grid>
            </Grid>

            <Box sx={{ mt: 2, textAlign: 'right' }}>
              <Typography variant="caption" color="textSecondary">
                Last System Check: {new Date().toLocaleString()}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}