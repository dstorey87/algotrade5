import React, { useEffect, useState } from 'react';
import { Card, CardContent, Grid, Typography } from '@mui/material';
import websocketService from '@/services/websocket';

interface MetricsSnapshot {
  avgProcessingTime: number;
  avgBatchSize: number;
  avgCompressionRatio: number;
  timestamp: string;
  sampleSizes: {
    processing: number;
    batches: number;
    compression: number;
  };
}

export const PerformanceMetricsDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsSnapshot | null>(null);

  useEffect(() => {
    const updateMetrics = () => {
      const currentMetrics = websocketService.getPerformanceMetrics();
      setMetrics(currentMetrics);
    };

    // Update metrics every 5 seconds
    const interval = setInterval(updateMetrics, 5000);
    updateMetrics(); // Initial update

    return () => clearInterval(interval);
  }, []);

  if (!metrics) {
    return null;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Real-time Performance Metrics
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Card variant="outlined">
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Message Processing
                </Typography>
                <Typography variant="h5">
                  {metrics.avgProcessingTime.toFixed(2)}ms
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Sample size: {metrics.sampleSizes.processing}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={4}>
            <Card variant="outlined">
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Batch Size
                </Typography>
                <Typography variant="h5">
                  {metrics.avgBatchSize.toFixed(1)}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Sample size: {metrics.sampleSizes.batches}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={4}>
            <Card variant="outlined">
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Compression Ratio
                </Typography>
                <Typography variant="h5">
                  {metrics.avgCompressionRatio.toFixed(2)}x
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Sample size: {metrics.sampleSizes.compression}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        <Typography variant="caption" color="textSecondary" sx={{ mt: 2, display: 'block' }}>
          Last updated: {new Date(metrics.timestamp).toLocaleString()}
        </Typography>
      </CardContent>
    </Card>
  );
};