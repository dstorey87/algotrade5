import React from 'react';
import { WebSocketErrorBoundary } from '../components/ErrorBoundary/WebSocketErrorBoundary';
import { TradeMonitor } from '../components/RealTimeMonitoring/TradeMonitor';
import { Container } from '@mui/material';

export default function Home() {
  return (
    <Container maxWidth={false} sx={{ height: '100vh', py: 3 }}>
      <WebSocketErrorBoundary>
        <TradeMonitor />
      </WebSocketErrorBoundary>
    </Container>
  );
}