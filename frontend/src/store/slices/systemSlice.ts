import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface SystemHealth {
  freqtrade: boolean
  database: boolean
  models: boolean
  quantum: boolean
}

interface SystemState {
  gpuUtilization: number
  memoryUsage: number
  modelAccuracy: number
  modelConfidence: number
  quantumCircuitStatus: string
  systemHealth: SystemHealth
}

const initialState: SystemState = {
  gpuUtilization: 0,
  memoryUsage: 0,
  modelAccuracy: 0,
  modelConfidence: 0,
  quantumCircuitStatus: 'Not Ready',
  systemHealth: {
    freqtrade: false,
    database: false,
    models: false,
    quantum: false
  }
}

const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    updateResourceUsage(state, action: PayloadAction<{ gpu: number; memory: number }>) {
      state.gpuUtilization = action.payload.gpu
      state.memoryUsage = action.payload.memory
    },
    updateModelMetrics(state, action: PayloadAction<{ accuracy: number; confidence: number }>) {
      state.modelAccuracy = action.payload.accuracy
      state.modelConfidence = action.payload.confidence
    },
    updateQuantumStatus(state, action: PayloadAction<string>) {
      state.quantumCircuitStatus = action.payload
    },
    updateSystemHealth(state, action: PayloadAction<Partial<SystemHealth>>) {
      state.systemHealth = { ...state.systemHealth, ...action.payload }
    }
  }
})

export const { 
  updateResourceUsage, 
  updateModelMetrics, 
  updateQuantumStatus, 
  updateSystemHealth 
} = systemSlice.actions

export default systemSlice.reducer