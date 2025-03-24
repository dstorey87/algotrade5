import apiSettings from '@/config/api';

class MLService {
  private readonly API_BASE = apiSettings.apiUrl('ml');

  async loadModel(modelId: string): Promise<any> {
    const response = await fetch(`${this.API_BASE}/models/${modelId}/load`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to load model ${modelId}: ${response.statusText}`);
    }

    return response.json();
  }

  async unloadModel(modelId: string): Promise<void> {
    const response = await fetch(`${this.API_BASE}/models/${modelId}/unload`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error(`Failed to unload model ${modelId}: ${response.statusText}`);
    }
  }

  async getModelStatus(modelId: string): Promise<any> {
    const response = await fetch(`${this.API_BASE}/models/${modelId}/status`);
    
    if (!response.ok) {
      throw new Error(`Failed to get model status for ${modelId}: ${response.statusText}`);
    }

    return response.json();
  }
}

export const mlService = new MLService();