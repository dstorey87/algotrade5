import { useState, useEffect, useCallback, useRef } from 'react';
import { PerformanceMetrics } from '../services/websocket';

interface ComponentMetrics {
  componentRenderTime: number;
  lastUpdateTimestamp: number;
  memoryUsage?: number;
}

export interface PerformanceData extends PerformanceMetrics, ComponentMetrics {}

export const usePerformanceMonitor = (componentName: string) => {
  const [metrics, setMetrics] = useState<PerformanceData>({
    messageProcessingRate: 0,
    batchSize: 0,
    compressionRatio: 0,
    latency: 0,
    componentRenderTime: 0,
    lastUpdateTimestamp: Date.now()
  });

  const frameRef = useRef<number>();
  const startTimeRef = useRef<number>(performance.now());

  const measureRenderTime = useCallback(() => {
    const renderTime = performance.now() - startTimeRef.current;
    
    setMetrics(prev => ({
      ...prev,
      componentRenderTime: renderTime,
      lastUpdateTimestamp: Date.now()
    }));

    // Reset for next render
    startTimeRef.current = performance.now();
  }, []);

  const updateMetrics = useCallback((wsMetrics: Partial<PerformanceMetrics>) => {
    setMetrics(prev => ({
      ...prev,
      ...wsMetrics,
      lastUpdateTimestamp: Date.now()
    }));
  }, []);

  useEffect(() => {
    const measurePerformance = () => {
      // Skip measurement if document is hidden
      if (document.hidden) {
        return;
      }

      const currentMemory = (performance as any).memory?.usedJSHeapSize;
      
      // Update performance metrics
      setMetrics(prev => ({
        ...prev,
        memoryUsage: currentMemory,
        lastUpdateTimestamp: Date.now()
      }));

      frameRef.current = requestAnimationFrame(measurePerformance);
    };

    frameRef.current = requestAnimationFrame(measurePerformance);

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, []);

  // Log performance data periodically for debugging
  useEffect(() => {
    const logInterval = setInterval(() => {
      console.debug(`[${componentName}] Performance Metrics:`, metrics);
    }, 5000); // Log every 5 seconds

    return () => clearInterval(logInterval);
  }, [componentName, metrics]);

  return {
    metrics,
    measureRenderTime,
    updateMetrics
  };
};