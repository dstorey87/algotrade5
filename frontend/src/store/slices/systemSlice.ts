import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

export interface SystemMetrics {
  cpuUsage: number;
  memoryUsage: number;
  gpuUsage: number;
  diskUsage: number;
  networkLatency: number;
}

export interface AIModelStatus {
  name: string;
  status: 'active' | 'standby' | 'error';
  accuracy: number;
  lastUpdated: string;
  predictions: number;
}

export interface SystemState {
  status: 'operational' | 'degraded' | 'maintenance' | 'error';
  uptime: number;
  lastBackup: string;
  metrics: SystemMetrics;
  aiModels: AIModelStatus[];
  databaseStatus: 'connected' | 'error' | 'syncing';
  logs: { timestamp: string; level: string; message: string }[];
  isLoading: boolean;
  error: string | null;
}

const initialState: SystemState = {
  status: 'operational',
  uptime: 0,
  lastBackup: '',
  metrics: {
    cpuUsage: 0,
    memoryUsage: 0,
    gpuUsage: 0,
    diskUsage: 0,
    networkLatency: 0,
  },
  aiModels: [],
  databaseStatus: 'connected',
  logs: [],
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchSystemStatus = createAsyncThunk(
  'system/fetchSystemStatus',
  async (_, { rejectWithValue }) => {
    try {
      // In a real app, this would call your API
      // const response = await api.get('/system/status');
      // return response.data;
      
      // Mock response for development
      return {
        status: 'operational',
        uptime: 126543, // in seconds
        lastBackup: '2024-03-14T12:00:00Z',
        metrics: {
          cpuUsage: 32.5,
          memoryUsage: 45.2,
          gpuUsage: 78.1,
          diskUsage: 56.3,
          networkLatency: 24.7,
        },
        aiModels: [
          { name: 'QuantumStrategy1', status: 'active', accuracy: 0.82, lastUpdated: '2024-03-14T10:30:00Z', predictions: 156 },
          { name: 'MarketRegimeClassifier', status: 'active', accuracy: 0.89, lastUpdated: '2024-03-14T09:45:00Z', predictions: 78 },
          { name: 'PatternDetector', status: 'standby', accuracy: 0.75, lastUpdated: '2024-03-14T08:15:00Z', predictions: 42 },
        ],
        databaseStatus: 'connected',
        logs: [
          { timestamp: '2024-03-14T15:45:32Z', level: 'INFO', message: 'Trade completed: BTC/USDT' },
          { timestamp: '2024-03-14T15:43:12Z', level: 'INFO', message: 'New pattern detected: Double Bottom' },
          { timestamp: '2024-03-14T15:40:05Z', level: 'WARN', message: 'API rate limit approaching' },
          { timestamp: '2024-03-14T15:35:18Z', level: 'INFO', message: 'Model retraining completed' },
        ],
      };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch system status');
    }
  }
);

export const runSystemBackup = createAsyncThunk(
  'system/runSystemBackup',
  async (_, { rejectWithValue }) => {
    try {
      // In a real app, this would call your API
      // const response = await api.post('/system/backup');
      // return response.data;
      
      // Mock response
      return { lastBackup: new Date().toISOString() };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create system backup');
    }
  }
);

export const retrainModels = createAsyncThunk(
  'system/retrainModels',
  async (_, { rejectWithValue }) => {
    try {
      // In a real app, this would call your API
      // const response = await api.post('/system/retrain-models');
      // return response.data;
      
      // Mock response (would normally return updated model info)
      return {
        aiModels: [
          { name: 'QuantumStrategy1', status: 'active', accuracy: 0.85, lastUpdated: new Date().toISOString(), predictions: 156 },
          { name: 'MarketRegimeClassifier', status: 'active', accuracy: 0.91, lastUpdated: new Date().toISOString(), predictions: 78 },
          { name: 'PatternDetector', status: 'active', accuracy: 0.79, lastUpdated: new Date().toISOString(), predictions: 42 },
        ],
      };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to retrain models');
    }
  }
);

// Create slice
const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    clearLogs: (state) => {
      state.logs = [];
    },
    resetError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchSystemStatus
      .addCase(fetchSystemStatus.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSystemStatus.fulfilled, (state, action) => {
        state.isLoading = false;
        state.status = action.payload.status;
        state.uptime = action.payload.uptime;
        state.lastBackup = action.payload.lastBackup;
        state.metrics = action.payload.metrics;
        state.aiModels = action.payload.aiModels;
        state.databaseStatus = action.payload.databaseStatus;
        state.logs = action.payload.logs;
      })
      .addCase(fetchSystemStatus.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // runSystemBackup
      .addCase(runSystemBackup.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(runSystemBackup.fulfilled, (state, action) => {
        state.isLoading = false;
        state.lastBackup = action.payload.lastBackup;
      })
      .addCase(runSystemBackup.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // retrainModels
      .addCase(retrainModels.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(retrainModels.fulfilled, (state, action) => {
        state.isLoading = false;
        state.aiModels = action.payload.aiModels;
      })
      .addCase(retrainModels.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearLogs, resetError } = systemSlice.actions;

export default systemSlice.reducer;