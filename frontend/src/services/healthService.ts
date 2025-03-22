import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const healthService = {
    getHealthStatus: async () => {
        const response = await axiosInstance.get('/health');
        return response.data;
    },

    getSystemStatus: async () => {
        const response = await axiosInstance.get('/system/status');
        return response.data;
    },

    getResourceUsage: async () => {
        const response = await axiosInstance.get('/system/resources');
        return response.data;
    },

    getComponentHealth: async (componentType?: string) => {
        const response = await axiosInstance.get('/health/components', {
            params: { type: componentType }
        });
        return response.data;
    },

    updateHealthCheck: async (checkId: string, config: any) => {
        return axiosInstance.put(`/health/checks/${checkId}`, config);
    },

    getHealthHistory: async (componentId: string) => {
        const response = await axiosInstance.get(`/health/history/${componentId}`);
        return response.data;
    },

    checkComponentHealth: async (componentId: string) => {
        return axiosInstance.post(`/health/check/${componentId}`);
    }
};