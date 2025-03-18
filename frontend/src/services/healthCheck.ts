import { useState, useEffect } from 'react';
import apiSettings from '@/config/api';

export interface HealthStatus {
  api: boolean;
  websocket: boolean;
  database: boolean;
  freqtrade: boolean;
  lastChecked: Date | null;
  error: string | null;
}

export interface ComponentHealth {
  name: string;
  status: 'online' | 'offline' | 'degraded' | 'unknown';
  latency?: number;
  lastChecked: Date | null;
  error?: string;
}

const initialHealthStatus: HealthStatus = {
  api: false,
  websocket: false,
  database: false,
  freqtrade: false,
  lastChecked: null,
  error: null
};

const initialComponentsHealth: Record<string, ComponentHealth> = {
  api: {
    name: 'API Server',
    status: 'unknown',
    lastChecked: null
  },
  websocket: {
    name: 'WebSocket',
    status: 'unknown',
    lastChecked: null
  },
  database: {
    name: 'Database',
    status: 'unknown',
    lastChecked: null
  },
  freqtrade: {
    name: 'FreqTrade',
    status: 'unknown',
    lastChecked: null
  },
};

/**
 * Service to check the health of various system components
 */
class HealthCheckService {
  private healthStatus: HealthStatus = { ...initialHealthStatus };
  private componentsHealth: Record<string, ComponentHealth> = { ...initialComponentsHealth };
  private checkInterval: ReturnType<typeof setInterval> | null = null;
  private listeners: Set<() => void> = new Set();

  /**
   * Start periodic health checks
   * @param interval Interval in milliseconds between checks
   */
  public startPeriodicChecks(interval: number = 30000): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }

    // Run an initial check immediately
    this.checkAllServices();

    // Set up periodic checks
    this.checkInterval = setInterval(() => {
      this.checkAllServices();
    }, interval);
  }

  /**
   * Stop periodic health checks
   */
  public stopPeriodicChecks(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
  }

  /**
   * Check all services health status
   */
  public async checkAllServices(): Promise<HealthStatus> {
    const startTime = Date.now();
    try {
      // Check API health
      const apiHealth = await this.checkApiHealth();
      this.updateComponentHealth('api', apiHealth ? 'online' : 'offline', Date.now() - startTime);

      // If API is healthy, check other services
      if (apiHealth) {
        const [wsHealth, dbHealth, ftHealth] = await Promise.all([
          this.checkWebSocketHealth(),
          this.checkDatabaseHealth(),
          this.checkFreqTradeHealth()
        ]);

        this.updateComponentHealth('websocket', wsHealth ? 'online' : 'offline');
        this.updateComponentHealth('database', dbHealth ? 'online' : 'offline');
        this.updateComponentHealth('freqtrade', ftHealth ? 'online' : 'offline');

        this.healthStatus = {
          api: apiHealth,
          websocket: wsHealth,
          database: dbHealth,
          freqtrade: ftHealth,
          lastChecked: new Date(),
          error: null
        };
      } else {
        // If API is down, mark all services as offline
        this.updateComponentHealth('websocket', 'offline');
        this.updateComponentHealth('database', 'offline');
        this.updateComponentHealth('freqtrade', 'offline');

        this.healthStatus = {
          api: false,
          websocket: false,
          database: false,
          freqtrade: false,
          lastChecked: new Date(),
          error: 'API server is unreachable'
        };
      }
    } catch (error) {
      this.healthStatus = {
        ...initialHealthStatus,
        lastChecked: new Date(),
        error: error instanceof Error ? error.message : String(error)
      };

      // Mark all services as degraded when there's an error
      Object.keys(this.componentsHealth).forEach(key => {
        this.updateComponentHealth(key, 'degraded', undefined, error instanceof Error ? error.message : String(error));
      });
    }

    // Notify all listeners of the health status change
    this.notifyListeners();
    
    return this.healthStatus;
  }

  /**
   * Check API health
   */
  private async checkApiHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${apiSettings.apiUrl('ping')}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        cache: 'no-store'
      });

      return response.ok;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  }

  /**
   * Check WebSocket health
   */
  private async checkWebSocketHealth(): Promise<boolean> {
    try {
      // We use the API to check WebSocket status since we can't directly check from client
      const response = await fetch(`${apiSettings.apiUrl('ws/status')}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        cache: 'no-store'
      });

      if (!response.ok) return false;
      
      const data = await response.json();
      return data.status === 'running';
    } catch (error) {
      console.error('WebSocket health check failed:', error);
      return false;
    }
  }

  /**
   * Check Database health
   */
  private async checkDatabaseHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${apiSettings.apiUrl('system/database')}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        cache: 'no-store'
      });

      if (!response.ok) return false;
      
      const data = await response.json();
      return data.status === 'ok';
    } catch (error) {
      console.error('Database health check failed:', error);
      return false;
    }
  }

  /**
   * Check FreqTrade health
   */
  private async checkFreqTradeHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${apiSettings.apiUrl('status')}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        cache: 'no-store'
      });

      return response.ok;
    } catch (error) {
      console.error('FreqTrade health check failed:', error);
      return false;
    }
  }

  /**
   * Update individual component health status
   */
  private updateComponentHealth(
    component: string, 
    status: 'online' | 'offline' | 'degraded' | 'unknown',
    latency?: number,
    error?: string
  ): void {
    if (this.componentsHealth[component]) {
      this.componentsHealth[component] = {
        ...this.componentsHealth[component],
        status,
        lastChecked: new Date(),
        latency,
        error
      };
    }
  }

  /**
   * Get current health status
   */
  public getHealthStatus(): HealthStatus {
    return { ...this.healthStatus };
  }

  /**
   * Get detailed component health status
   */
  public getComponentsHealth(): Record<string, ComponentHealth> {
    return { ...this.componentsHealth };
  }

  /**
   * Add a listener to be notified on health status changes
   */
  public subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  /**
   * Notify all listeners of health status changes
   */
  private notifyListeners(): void {
    this.listeners.forEach(listener => listener());
  }
}

// Create singleton instance
const healthCheckService = new HealthCheckService();
export default healthCheckService;

/**
 * Hook to use health check service in components
 */
export function useHealthCheck(autoCheck: boolean = true, interval: number = 30000) {
  const [health, setHealth] = useState<HealthStatus>(healthCheckService.getHealthStatus());
  const [componentsHealth, setComponentsHealth] = useState<Record<string, ComponentHealth>>(
    healthCheckService.getComponentsHealth()
  );

  useEffect(() => {
    // Handler for health updates
    const handleHealthUpdate = () => {
      setHealth(healthCheckService.getHealthStatus());
      setComponentsHealth(healthCheckService.getComponentsHealth());
    };

    // Subscribe to health updates
    const unsubscribe = healthCheckService.subscribe(handleHealthUpdate);

    // Start periodic checks if requested
    if (autoCheck) {
      healthCheckService.startPeriodicChecks(interval);
    }

    // Initial check
    healthCheckService.checkAllServices().then(handleHealthUpdate);

    // Cleanup
    return () => {
      unsubscribe();
      if (autoCheck) {
        healthCheckService.stopPeriodicChecks();
      }
    };
  }, [autoCheck, interval]);

  const checkHealth = async () => {
    const status = await healthCheckService.checkAllServices();
    setHealth(status);
    setComponentsHealth(healthCheckService.getComponentsHealth());
    return status;
  };

  return {
    health,
    componentsHealth,
    checkHealth,
    isHealthy: health.api && health.websocket && health.database && health.freqtrade,
    isPartiallyHealthy: health.api || health.websocket || health.database || health.freqtrade
  };
}