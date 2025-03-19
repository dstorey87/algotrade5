import { TradingMetrics } from '../types/trading';

class MetricsCache {
  private cache: Map<string, { data: TradingMetrics; timestamp: number }> = new Map();
  private readonly TTL = 10000; // 10 seconds cache TTL

  set(key: string, data: TradingMetrics): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });
  }

  get(key: string): TradingMetrics | null {
    const cached = this.cache.get(key);
    if (!cached) return null;

    if (Date.now() - cached.timestamp > this.TTL) {
      this.cache.delete(key);
      return null;
    }

    return cached.data;
  }

  clear(): void {
    this.cache.clear();
  }
}

export const metricsCache = new MetricsCache();
export default metricsCache;