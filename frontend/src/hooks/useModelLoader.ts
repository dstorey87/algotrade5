import { useState, useRef, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { ModelType, ModelStatus } from '@/types';

interface UseModelLoaderOptions {
  preloadModels?: string[];
  cacheTimeout?: number;
  maxCacheSize?: number;
}

interface ModelCache {
  data: any;
  loadedAt: number;
  lastUsed: number;
}

export function useModelLoader({
  preloadModels = [],
  cacheTimeout = 5 * 60 * 1000, // 5 minutes
  maxCacheSize = 5
}: UseModelLoaderOptions = {}) {
  const queryClient = useQueryClient();
  const modelCache = useRef<Map<string, ModelCache>>(new Map());
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const preloadQueue = useRef<string[]>([...preloadModels]);

  // LRU Cache management
  const updateModelCache = useCallback((modelId: string, data: any) => {
    // Implement LRU eviction if cache is full
    if (modelCache.current.size >= maxCacheSize) {
      let oldestKey = '';
      let oldestTime = Date.now();
      
      modelCache.current.forEach((value, key) => {
        if (value.lastUsed < oldestTime) {
          oldestTime = value.lastUsed;
          oldestKey = key;
        }
      });

      if (oldestKey) {
        modelCache.current.delete(oldestKey);
      }
    }

    // Update cache with new data
    modelCache.current.set(modelId, {
      data,
      loadedAt: Date.now(),
      lastUsed: Date.now()
    });
  }, [maxCacheSize]);

  // Load and cache model
  const loadModel = useCallback(async (modelId: string, type: ModelType = 'ml') => {
    setLoading(prev => ({ ...prev, [modelId]: true }));

    try {
      // Check cache first
      const cached = modelCache.current.get(modelId);
      if (cached) {
        cached.lastUsed = Date.now();
        return cached.data;
      }

      // Load model through React Query
      const data = await queryClient.fetchQuery({
        queryKey: ['model', modelId],
        queryFn: () => fetch(`/api/models/${type}/${modelId}`).then(res => res.json()),
        staleTime: cacheTimeout,
        gcTime: cacheTimeout // Use gcTime instead of deprecated cacheTime
      });

      updateModelCache(modelId, data);
      return data;

    } finally {
      setLoading(prev => ({ ...prev, [modelId]: false }));
    }
  }, [queryClient, cacheTimeout, updateModelCache]);

  // Preload models in background
  const preloadModel = useCallback((modelId: string) => {
    if (!modelCache.current.has(modelId) && !loading[modelId]) {
      preloadQueue.current.push(modelId);
      void loadModel(modelId);
    }
  }, [loading, loadModel]);

  // Get model status
  const getModelStatus = useCallback((modelId: string): ModelStatus => {
    const cached = modelCache.current.get(modelId);
    return {
      isLoaded: !!cached,
      isLoading: loading[modelId] || false,
      loadedAt: cached?.loadedAt,
      lastUsed: cached?.lastUsed
    };
  }, [loading]);

  // Clear cache
  const clearCache = useCallback((modelId?: string) => {
    if (modelId) {
      modelCache.current.delete(modelId);
    } else {
      modelCache.current.clear();
    }
  }, []);

  return {
    loadModel,
    preloadModel,
    getModelStatus,
    clearCache,
    loading
  };
}