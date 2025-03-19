import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api/v1';

export const strategyApi = {
  getActiveStrategy: async () => {
    const response = await axios.get(`${BASE_URL}/strategy/current`);
    return response.data;
  },

  updateStrategy: async (strategyConfig: any) => {
    const response = await axios.post(`${BASE_URL}/strategy/update`, strategyConfig);
    return response.data;
  },

  listAvailableStrategies: async () => {
    const response = await axios.get(`${BASE_URL}/strategy/list`);
    return response.data;
  },

  getStrategyPerformance: async (strategyName: string) => {
    const response = await axios.get(`${BASE_URL}/strategy/${strategyName}/performance`);
    return response.data;
  }
};

export default strategyApi;