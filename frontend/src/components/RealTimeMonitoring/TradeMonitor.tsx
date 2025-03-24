import React, { useCallback, useMemo } from 'react';
import { useSelector } from 'react-redux';
import { Card, CardContent, Stack } from '@mui/material';
import { RootState } from '@/lib/store';
import { useRealTimeUpdates } from '@/hooks/useRealTimeUpdates';
import { VirtualizedTradeList } from './VirtualizedTradeList';
import { PerformanceMetricsDashboard } from './PerformanceMetricsDashboard';
import { useModelLoader } from '@/hooks/useModelLoader';
import { Trade } from '@/types';

const REQUIRED_MODELS = ['trade_analyzer', 'risk_calculator'];

export const TradeMonitor: React.FC = React.memo(() => {
  // Set up real-time updates with WebSocket
  useRealTimeUpdates({ enableWebSocket: true });

  // Initialize model loader with preloading
  const { loadModel } = useModelLoader({
    preloadModels: REQUIRED_MODELS,
    maxCacheSize: 10
  });

  // Memoized selectors
  const trades = useSelector((state: RootState) => state.trading.trades);
  const performance = useSelector((state: RootState) => state.trading.performanceStats);

  // Memoized performance calculations
  const performanceMetrics = useMemo(() => ({
    winRate: (performance.wins / (performance.wins + performance.losses)) * 100 || 0,
    profitFactor: performance.totalProfit / Math.abs(performance.totalLoss) || 0,
    avgProfit: performance.totalProfit / performance.trades || 0
  }), [performance]);

  // Memoized trade analysis
  const analyzeRisk = useCallback(async (trade: Trade) => {
    const analyzer = await loadModel('trade_analyzer');
    return analyzer.analyzeRisk(trade);
  }, [loadModel]);

  return (
    <Stack spacing={2}>
      <PerformanceMetricsDashboard />
      
      <Card>
        <CardContent>
          <div className="monitor-grid">
            {/* Performance Metrics */}
            <div className="metrics-panel">
              <div>Win Rate: {performanceMetrics.winRate.toFixed(2)}%</div>
              <div>Profit Factor: {performanceMetrics.profitFactor.toFixed(2)}</div>
              <div>Avg Profit: {performanceMetrics.avgProfit.toFixed(2)}</div>
            </div>
            
            {/* Virtualized Trade List */}
            <div className="trades-panel" style={{ height: '500px' }}>
              <VirtualizedTradeList trades={trades} />
            </div>
          </div>
        </CardContent>
      </Card>
    </Stack>
  );
});