import React, { useEffect } from 'react';
import { Card, CardContent, Typography, Grid, CircularProgress } from '@mui/material';
import { useWebSocket } from '../../hooks/useWebSocket';
import { usePerformanceMonitor } from '../../hooks/usePerformanceMonitor';

interface MetricCardProps {
  title: string;
  value: number | string;
  unit?: string;
  color?: string;
  threshold?: number;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, unit, color, threshold }) => {
  const isWarning = threshold && typeof value === 'number' && value > threshold;
  
  return (
    <Card sx={{ 
      minWidth: 275, 
      bgcolor: isWarning ? 'warning.main' : 'background.paper',
      transition: 'background-color 0.3s ease'
    }}>
      <CardContent>
        <Typography variant="h6" component="div" color={color}>
          {title}
        </Typography>
        <Typography variant="h4" component="div" color={color}>
          {typeof value === 'number' ? value.toFixed(2) : value}
          {unit && <Typography variant="caption" component="span"> {unit}</Typography>}
        </Typography>
      </CardContent>
    </Card>
  );
};

export const PerformanceMetricsDashboard: React.FC = () => {
  const { connected, metrics: wsMetrics } = useWebSocket();
  const { metrics: perfMetrics, measureRenderTime } = usePerformanceMonitor('PerformanceMetricsDashboard');

  // Measure render time on each update
  useEffect(() => {
    measureRenderTime();
  });

  return (
    <div>
      <Typography variant="h5" gutterBottom>
        System Performance
        {!connected && (
          <CircularProgress 
            size={20} 
            sx={{ ml: 2, verticalAlign: 'middle', color: 'error.main' }} 
          />
        )}
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Message Processing Rate"
            value={wsMetrics.messageProcessingRate}
            unit="msg/s"
            threshold={1000}
            color={wsMetrics.messageProcessingRate > 1000 ? 'error.main' : 'primary.main'}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Batch Size"
            value={wsMetrics.batchSize}
            threshold={500}
            color={wsMetrics.batchSize > 500 ? 'warning.main' : 'primary.main'}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Compression Ratio"
            value={wsMetrics.compressionRatio}
            unit="x"
            color="primary.main"
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Latency"
            value={wsMetrics.latency}
            unit="ms"
            threshold={100}
            color={wsMetrics.latency > 100 ? 'error.main' : 'primary.main'}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Component Render Time"
            value={perfMetrics.componentRenderTime}
            unit="ms"
            threshold={16.67} // 60fps threshold
            color={perfMetrics.componentRenderTime > 16.67 ? 'warning.main' : 'primary.main'}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Memory Usage"
            value={perfMetrics.memoryUsage ? Math.round(perfMetrics.memoryUsage / (1024 * 1024)) : 'N/A'}
            unit="MB"
            threshold={100}
            color={perfMetrics.memoryUsage && perfMetrics.memoryUsage > 100 * 1024 * 1024 ? 'warning.main' : 'primary.main'}
          />
        </Grid>
      </Grid>
    </div>
  );
};