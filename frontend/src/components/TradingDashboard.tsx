import React, { useEffect, useState } from 'react';
import { Typography, Alert, CircularProgress } from '@mui/material';
import api, { tradingApi } from '../services/api';
import { TradingMetrics } from '../types/trading';

const TradingDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<TradingMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      // Use the tradingApi.getMetrics method instead of api.get
      const data = await tradingApi.getMetrics();
      
      // Validate required AI metrics fields
      if (!data.aiConfidence || !data.predictionAccuracy) {
        throw new Error('Invalid metrics data received');
      }
      
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch trading metrics');
      console.error('Error fetching metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    // Refresh metrics every 30 seconds
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!metrics) {
    return <Typography>No metrics data available</Typography>;
  }

  return (
    <div>
      <Typography variant="h4">Trading Dashboard</Typography>
      <Typography>AI Confidence: {metrics.aiConfidence}%</Typography>
      <Typography>Prediction Accuracy: {metrics.predictionAccuracy}%</Typography>
      {metrics.quantum?.loopStatus && (
        <Typography>Quantum Loop Status: {metrics.quantum.loopStatus}</Typography>
      )}
      {/* ...existing metrics display code... */}
    </div>
  );
};

export default TradingDashboard;