import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '@/lib/store'
import { 
  fetchTradeData, 
  fetchCurrentTrades, 
  fetchTradeHistory,
  setRealTimeEnabled,
  updateSystemStatus,
  updateBalance,
  updateTrades,
  updatePerformanceStats
} from '@/store/slices/tradingSlice'
import websocketService from '@/services/websocket'
import apiSettings from '@/config/api'

export function useRealTimeUpdates(options: {
  enableWebSocket?: boolean;
  pollingInterval?: number;
} = {}) {
  const { 
    enableWebSocket = true, 
    pollingInterval = apiSettings.pollingInterval 
  } = options;
  
  const dispatch = useDispatch<AppDispatch>();
  const { realTimeEnabled } = useSelector((state: RootState) => state.trading);
  
  useEffect(() => {
    // Initial data fetch regardless of connection method
    dispatch(fetchTradeData());
    dispatch(fetchCurrentTrades());
    dispatch(fetchTradeHistory());
    
    let timer: NodeJS.Timeout | null = null;
    
    // Try to use WebSockets if enabled
    if (enableWebSocket) {
      try {
        websocketService.connect(dispatch);
        dispatch(setRealTimeEnabled(true));
        
        // If WebSocket is not connected after 3 seconds, fall back to polling
        const wsCheckTimer = setTimeout(() => {
          if (!websocketService.isConnected()) {
            console.log('WebSocket connection failed, falling back to polling');
            startPolling();
          }
        }, 3000);
        
        return () => {
          clearTimeout(wsCheckTimer);
          websocketService.disconnect();
          dispatch(setRealTimeEnabled(false));
          if (timer) {
            clearInterval(timer);
          }
        };
      } catch (error) {
        console.error('WebSocket initialization error:', error);
        startPolling();
      }
    } else {
      // Use polling if WebSockets are disabled
      startPolling();
    }
    
    function startPolling() {
      dispatch(setRealTimeEnabled(false));
      
      // Set up polling interval
      timer = setInterval(() => {
        dispatch(fetchTradeData());
        dispatch(fetchCurrentTrades());
        dispatch(fetchTradeHistory());
      }, pollingInterval);
    }
    
    // Clean up on unmount
    return () => {
      if (timer) {
        clearInterval(timer);
      }
      websocketService.disconnect();
      dispatch(setRealTimeEnabled(false));
    };
  }, [dispatch, enableWebSocket, pollingInterval]);
  
  return { realTimeEnabled };
}