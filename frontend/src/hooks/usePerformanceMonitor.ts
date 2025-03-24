import { useEffect, useRef } from 'react';

interface PerformanceMetrics {
  messageProcessingTime: number[];
  batchSize: number[];
  renderTime: number[];
  timestamp: number;
}

export function usePerformanceMonitor(componentName: string) {
  const metrics = useRef<PerformanceMetrics>({
    messageProcessingTime: [],
    batchSize: [],
    renderTime: [],
    timestamp: Date.now()
  });

  const logMetric = (type: keyof Omit<PerformanceMetrics, 'timestamp'>, value: number) => {
    metrics.current[type].push(value);
    
    // Keep only last 100 measurements
    if (metrics.current[type].length > 100) {
      metrics.current[type].shift();
    }
  };

  const getAverageMetrics = () => {
    const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
    
    return {
      avgProcessingTime: avg(metrics.current.messageProcessingTime),
      avgBatchSize: avg(metrics.current.batchSize),
      avgRenderTime: avg(metrics.current.renderTime)
    };
  };

  // Report metrics every minute
  useEffect(() => {
    const interval = setInterval(() => {
      const avgMetrics = getAverageMetrics();
      console.log(`Performance metrics for ${componentName}:`, {
        ...avgMetrics,
        timestamp: new Date().toISOString(),
        sampleSize: metrics.current.messageProcessingTime.length
      });
    }, 60000);

    return () => clearInterval(interval);
  }, [componentName]);

  return {
    logMessageProcessing: (time: number) => logMetric('messageProcessingTime', time),
    logBatchSize: (size: number) => logMetric('batchSize', size),
    logRenderTime: (time: number) => logMetric('renderTime', time),
    getAverageMetrics
  };
}