import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

interface SystemState {
  isLoading: boolean
  error: string | null
  status: 'running' | 'stopped' | 'error'
  version: string
  uptime: string
  dryRun: boolean
  tradingMode: string
  gpuUtilization: number
  memoryUsage: number
  systemHealth: {
    freqtrade: boolean
    database: boolean
    models: boolean
    quantum: boolean
  }
  logs: Array<{
    timestamp: string
    level: string
    message: string
  }>
}

const initialState: SystemState = {
  isLoading: false,
  error: null,
  status: 'stopped',
  version: '',
  uptime: '',
  dryRun: true,
  tradingMode: 'spot',
  gpuUtilization: 0,
  memoryUsage: 0,
  systemHealth: {
    freqtrade: false,
    database: false,
    models: false,
    quantum: false,
  },
  logs: []
}

export const fetchSystemStatus = createAsyncThunk(
  'system/fetchStatus',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/system/status')
      if (!response.ok) throw new Error('Failed to fetch system status')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch system status')
    }
  }
)

const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    clearLogs: (state) => {
      state.logs = []
    },
    resetError: (state) => {
      state.error = null
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSystemStatus.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchSystemStatus.fulfilled, (state, action) => {
        state.isLoading = false
        Object.assign(state, action.payload)
      })
      .addCase(fetchSystemStatus.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
  }
})

export const { clearLogs, resetError } = systemSlice.actions
export default systemSlice.reducer