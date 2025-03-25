import { useState, useEffect, useCallback } from 'react';

interface ModelCache {
  [key: string]: {
    model: any;
    lastAccessed: number;
  };
}

const MAX_CACHE_SIZE = 5;
const modelCache: ModelCache = {};

export const useModelLoader = (modelName: string) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [model, setModel] = useState<any>(null);

  const loadModel = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Check cache first
      if (modelCache[modelName]) {
        modelCache[modelName].lastAccessed = Date.now();
        setModel(modelCache[modelName].model);
        setLoading(false);
        return;
      }

      // Simulate model loading - replace with actual model loading logic
      const response = await fetch(`/api/models/${modelName}`);
      if (!response.ok) {
        throw new Error(`Failed to load model ${modelName}`);
      }
      const loadedModel = await response.json();

      // Manage cache size using LRU strategy
      if (Object.keys(modelCache).length >= MAX_CACHE_SIZE) {
        const oldestModel = Object.entries(modelCache).reduce((oldest, [key, value]) => {
          return !oldest || value.lastAccessed < oldest.lastAccessed
            ? { key, lastAccessed: value.lastAccessed }
            : oldest;
        }, null as { key: string; lastAccessed: number } | null);

        if (oldestModel) {
          delete modelCache[oldestModel.key];
        }
      }

      // Add to cache
      modelCache[modelName] = {
        model: loadedModel,
        lastAccessed: Date.now()
      };

      setModel(loadedModel);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load model'));
    } finally {
      setLoading(false);
    }
  }, [modelName]);

  useEffect(() => {
    loadModel();
  }, [loadModel]);

  const reloadModel = useCallback(() => {
    // Remove from cache to force reload
    delete modelCache[modelName];
    return loadModel();
  }, [modelName, loadModel]);

  return {
    model,
    loading,
    error,
    reloadModel
  };
};