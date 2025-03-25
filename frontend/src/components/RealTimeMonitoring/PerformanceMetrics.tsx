import React from 'react';
import { Card, Grid, Text, Title, Metric } from '@tremor/react';
import { useSelector } from 'react-redux';

interface PerformanceMetricsProps {
  messageProcessingRate?: number;
  batchSize?: number;
  compressionRatio?: number;
  latency?: number;
}

export const PerformanceMetrics: React.FC<PerformanceMetricsProps> = ({
  messageProcessingRate = 0,
  batchSize = 0,
  compressionRatio = 0,
  latency = 0
}) => {
  const metrics = useSelector((state: any) => state.trading.performanceMetrics);

  return (
    <div data-testid="performance-metrics">
      <Grid numItems={2} numItemsMd={4} className="gap-4">
        <Card>
          <Title>Message Processing Rate</Title>
          <Metric>{metrics?.messageProcessingRate || messageProcessingRate}/s</Metric>
        </Card>
        <Card>
          <Title>Batch Size</Title>
          <Metric>{metrics?.batchSize || batchSize}</Metric>
        </Card>
        <Card>
          <Title>Compression Ratio</Title>
          <Metric>{((metrics?.compressionRatio || compressionRatio) * 100).toFixed(1)}%</Metric>
        </Card>
        <Card>
          <Title>Processing Latency</Title>
          <Metric>{metrics?.latency || latency}ms</Metric>
        </Card>
      </Grid>
    </div>
  );
};