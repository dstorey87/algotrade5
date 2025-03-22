import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface QuantumMetrics {
  confidence: number;
  stability: number;
  coherence: number;
  entanglement: number;
}

interface QuantumState {
  isProcessing: boolean;
  circuitDepth: number;
  autoOptimize: boolean;
  metrics: QuantumMetrics;
  timeseriesData: Array<{ x: string; y: number }>;
  error: string | null;
}

const initialState: QuantumState = {
  isProcessing: false,
  circuitDepth: 3,
  autoOptimize: true,
  metrics: {
    confidence: 0,
    stability: 0,
    coherence: 0,
    entanglement: 0
  },
  timeseriesData: [],
  error: null
};

export const startQuantumLoop = createAsyncThunk(
  'quantum/startLoop',
  async (config: { circuitDepth: number; autoOptimize: boolean }) => {
    const response = await axios.post('/api/quantum/start', config);
    return response.data;
  }
);

export const stopQuantumLoop = createAsyncThunk(
  'quantum/stopLoop',
  async () => {
    const response = await axios.post('/api/quantum/stop');
    return response.data;
  }
);

export const fetchQuantumMetrics = createAsyncThunk(
  'quantum/fetchMetrics',
  async () => {
    const response = await axios.get('/api/quantum/metrics');
    return response.data;
  }
);

const quantumSlice = createSlice({
  name: 'quantum',
  initialState,
  reducers: {
    updateCircuitDepth: (state, action) => {
      state.circuitDepth = action.payload;
    },
    updateAutoOptimize: (state, action) => {
      state.autoOptimize = action.payload;
    },
    addTimeseriesDataPoint: (state, action) => {
      state.timeseriesData.push(action.payload);
      if (state.timeseriesData.length > 50) {
        state.timeseriesData.shift();
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(startQuantumLoop.pending, (state) => {
        state.isProcessing = true;
        state.error = null;
      })
      .addCase(startQuantumLoop.fulfilled, (state) => {
        state.error = null;
      })
      .addCase(startQuantumLoop.rejected, (state, action) => {
        state.isProcessing = false;
        state.error = action.error.message || 'Failed to start quantum loop';
      })
      .addCase(stopQuantumLoop.fulfilled, (state) => {
        state.isProcessing = false;
        state.error = null;
      })
      .addCase(fetchQuantumMetrics.fulfilled, (state, action) => {
        state.metrics = action.payload.metrics;
        // Instead of calling the reducer directly, just modify the state
        state.timeseriesData.push({
          x: new Date().toLocaleTimeString(),
          y: action.payload.metrics.confidence
        });
        // Maintain the array size
        if (state.timeseriesData.length > 50) {
          state.timeseriesData.shift();
        }
      })
      .addCase(fetchQuantumMetrics.rejected, (state, action) => {
        state.error = action.error.message || 'Failed to fetch quantum metrics';
      });
  }
});

export const {
  updateCircuitDepth,
  updateAutoOptimize,
  addTimeseriesDataPoint
} = quantumSlice.actions;

export default quantumSlice.reducer;
