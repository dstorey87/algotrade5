import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Card, Title, Grid } from '@tremor/react';
import { websocketService } from '@/services/websocket';
import { setConnection, updateTrades } from '@/store/slices/tradingSlice';
import { RiskManager } from './RiskManager';
import { TradeMonitor } from './TradeMonitor';
import { PerformanceMetrics } from './PerformanceMetrics';

const RealTimeMonitoring: React.FC = () => {
  const dispatch = useDispatch();
  const { realTimeEnabled } = useSelector((state: any) => state.trading);

  useEffect(() => {
    if (realTimeEnabled) {
      websocketService.connect();
      
      const handleMessage = (message: any) => {
        if (message.type === 'trades') {
          dispatch(updateTrades(message.data));
        }
      };

      websocketService.addMessageListener(handleMessage);

      const handleDisconnect = () => dispatch(setConnection(false));
      window.addEventListener('offline', handleDisconnect);

      return () => {
        websocketService.removeMessageListener(handleMessage);
        window.removeEventListener('offline', handleDisconnect);
        websocketService.disconnect();
      };
    }
  }, [realTimeEnabled, dispatch]);

  return (
    <Grid numItems={1} numItemsMd={2} className="gap-6">
      <Card>
        <Title>Real-Time Trade Monitor</Title>
        <TradeMonitor />
      </Card>
      <Card>
        <Title>Performance Metrics</Title>
        <PerformanceMetrics />
      </Card>
      <Card>
        <Title>Risk Management</Title>
        <RiskManager />
      </Card>
    </Grid>
  );
};

export default RealTimeMonitoring;