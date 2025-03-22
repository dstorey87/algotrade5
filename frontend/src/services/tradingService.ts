import axios from 'axios';

// Configure base URL from environment variable or default
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const tradingService = {
    getTradingStatus: async () => {
        const response = await axiosInstance.get('/status');
        return response.data;
    },

    getTrades: async () => {
        const response = await axiosInstance.get('/trades');
        return response.data;
    },

    getActiveTrades: async () => {
        const response = await axiosInstance.get('/trades/active');
        return response.data;
    },

    startTrading: async (strategyId?: string) => {
        return axiosInstance.post('/start', { strategy_id: strategyId });
    },

    stopTrading: async () => {
        return axiosInstance.post('/stop');
    },

    getStrategies: async () => {
        const response = await axiosInstance.get('/strategies');
        return response.data;
    },

    updateStrategy: async (strategyId: string, config: any) => {
        return axiosInstance.put(`/strategies/${strategyId}`, config);
    },

    getStrategyBacktest: async (strategyId: string, timeframe: string) => {
        const response = await axiosInstance.get(`/strategies/${strategyId}/backtest`, {
            params: { timeframe }
        });
        return response.data;
    },

    executeManualTrade: async (tradeData: any) => {
        return axiosInstance.post('/trades/manual', tradeData);
    }
};