import React, { useState, useEffect } from 'react';
import { healthService } from '../../services/api';

// Types
interface SystemComponent {
  id: string;
  name: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  lastChecked: string;
  metrics: {
    responseTime?: number;
    memoryUsage?: number;
    cpuUsage?: number;
    errorRate?: number;
    queueSize?: number;
    [key: string]: number | undefined;
  };
  details: string;
}

interface SystemStatus {
  overall: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  components: SystemComponent[];
  lastUpdated: string;
}

interface ResourceUsage {
  cpu: number;
  memory: number;
  disk: number;
  gpu?: number;
  network: {
    sent: number;
    received: number;
  };
}

interface AiDiagnosis {
  issue: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  analysis: string;
  recommendation: string;
  potentialImpact: string;
}

const SystemHealthDashboard: React.FC = () => {
  // State management
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [resourceUsage, setResourceUsage] = useState<ResourceUsage | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);
  const [componentDetails, setComponentDetails] = useState<SystemComponent | null>(null);
  const [aiDiagnosis, setAiDiagnosis] = useState<AiDiagnosis | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [feedback, setFeedback] = useState({ message: '', isError: false });
  const [autoRefresh, setAutoRefresh] = useState(false);
  
  // Load initial data
  useEffect(() => {
    fetchSystemStatus();
  }, []);
  
  // Set up auto-refresh
  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    
    if (autoRefresh) {
      intervalId = setInterval(() => {
        fetchSystemStatus(false);
      }, 10000); // Refresh every 10 seconds
    }
    
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [autoRefresh]);
  
  // Fetch component details when selection changes
  useEffect(() => {
    if (selectedComponent && systemStatus) {
      const component = systemStatus.components.find(c => c.id === selectedComponent);
      if (component) {
        setComponentDetails(component);
        // Reset AI diagnosis when changing components
        setAiDiagnosis(null);
      }
    } else {
      setComponentDetails(null);
    }
  }, [selectedComponent, systemStatus]);
  
  // Fetch system status
  const fetchSystemStatus = async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
      }
      
      // Fetch overall system status
      const statusResponse = await healthService.getSystemStatus();
      setSystemStatus(statusResponse.data);
      
      // Fetch resource usage
      const resourceResponse = await healthService.getResourceUsage();
      setResourceUsage(resourceResponse.data);
      
      setFeedback({ message: '', isError: false });
    } catch (error) {
      console.error('Error fetching system status:', error);
      setFeedback({
        message: 'Failed to fetch system status. Check API connection.',
        isError: true
      });
    } finally {
      if (showLoading) {
        setIsLoading(false);
      }
    }
  };
  
  // Get AI diagnosis for a component
  const diagnoseProblem = async () => {
    if (!selectedComponent) return;
    
    try {
      setIsDiagnosing(true);
      setFeedback({ message: 'Diagnosing component issues...', isError: false });
      
      const response = await healthService.getDiagnosis(selectedComponent);
      setAiDiagnosis(response.data.diagnosis || null);
      
      setFeedback({ message: 'Diagnosis complete', isError: false });
    } catch (error) {
      console.error(`Error diagnosing component ${selectedComponent}:`, error);
      setFeedback({
        message: 'Failed to diagnose issues. AI service may be unavailable.',
        isError: true
      });
    } finally {
      setIsDiagnosing(false);
    }
  };
  
  // Toggle auto-refresh
  const toggleAutoRefresh = () => {
    setAutoRefresh(prevState => !prevState);
  };
  
  // Format timestamp
  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };
  
  // Get status color class
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500';
      case 'degraded':
        return 'bg-yellow-500';
      case 'unhealthy':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };
  
  // Get status text color class
  const getStatusTextColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-700';
      case 'degraded':
        return 'text-yellow-700';
      case 'unhealthy':
        return 'text-red-700';
      default:
        return 'text-gray-700';
    }
  };
  
  // Get status text
  const getStatusText = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };
  
  // Format bytes to readable format
  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };
  
  // Format percentage
  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">System Health Monitor</h1>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <label htmlFor="auto-refresh" className="mr-2 text-sm text-gray-700">Auto-refresh</label>
            <div className="relative inline-block w-10 mr-2 align-middle select-none">
              <input
                type="checkbox"
                id="auto-refresh"
                checked={autoRefresh}
                onChange={toggleAutoRefresh}
                className="sr-only"
              />
              <div className={`block h-6 rounded-full w-10 ${autoRefresh ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
              <div className={`absolute left-1 top-1 bg-white rounded-full h-4 w-4 transition-transform ${autoRefresh ? 'transform translate-x-4' : ''}`}></div>
            </div>
          </div>
          
          <button
            onClick={() => fetchSystemStatus(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Refresh
          </button>
        </div>
      </div>
      
      {/* Feedback message */}
      {feedback.message && (
        <div className={`mb-4 p-3 rounded ${feedback.isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {feedback.message}
        </div>
      )}
      
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-700"></div>
        </div>
      ) : systemStatus ? (
        <div className="space-y-6">
          {/* System Overview */}
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">System Overview</h2>
              <div className="flex items-center space-x-2">
                <div className={`h-3 w-3 rounded-full ${getStatusColor(systemStatus.overall)}`}></div>
                <span className={`text-sm font-medium ${getStatusTextColor(systemStatus.overall)}`}>
                  {getStatusText(systemStatus.overall)}
                </span>
                <span className="text-xs text-gray-500">
                  Updated at {formatTime(systemStatus.lastUpdated)}
                </span>
              </div>
            </div>
            
            {/* Resource Usage */}
            {resourceUsage && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-500">CPU Usage</div>
                  <div className="mt-1 relative pt-1">
                    <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200">
                      <div
                        style={{ width: `${resourceUsage.cpu}%` }}
                        className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
                          resourceUsage.cpu > 90 ? 'bg-red-500' :
                          resourceUsage.cpu > 70 ? 'bg-yellow-500' :
                          'bg-green-500'
                        }`}
                      ></div>
                    </div>
                  </div>
                  <div className="text-lg font-semibold mt-1">{formatPercentage(resourceUsage.cpu)}</div>
                </div>
                
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-500">Memory Usage</div>
                  <div className="mt-1 relative pt-1">
                    <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200">
                      <div
                        style={{ width: `${resourceUsage.memory}%` }}
                        className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
                          resourceUsage.memory > 90 ? 'bg-red-500' :
                          resourceUsage.memory > 70 ? 'bg-yellow-500' :
                          'bg-green-500'
                        }`}
                      ></div>
                    </div>
                  </div>
                  <div className="text-lg font-semibold mt-1">{formatPercentage(resourceUsage.memory)}</div>
                </div>
                
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-500">Disk Usage</div>
                  <div className="mt-1 relative pt-1">
                    <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200">
                      <div
                        style={{ width: `${resourceUsage.disk}%` }}
                        className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
                          resourceUsage.disk > 90 ? 'bg-red-500' :
                          resourceUsage.disk > 70 ? 'bg-yellow-500' :
                          'bg-green-500'
                        }`}
                      ></div>
                    </div>
                  </div>
                  <div className="text-lg font-semibold mt-1">{formatPercentage(resourceUsage.disk)}</div>
                </div>
                
                {resourceUsage.gpu !== undefined ? (
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-sm text-gray-500">GPU Usage</div>
                    <div className="mt-1 relative pt-1">
                      <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200">
                        <div
                          style={{ width: `${resourceUsage.gpu}%` }}
                          className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${
                            resourceUsage.gpu > 90 ? 'bg-red-500' :
                            resourceUsage.gpu > 70 ? 'bg-yellow-500' :
                            'bg-green-500'
                          }`}
                        ></div>
                      </div>
                    </div>
                    <div className="text-lg font-semibold mt-1">{formatPercentage(resourceUsage.gpu)}</div>
                  </div>
                ) : (
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-sm text-gray-500">Network</div>
                    <div className="flex justify-between">
                      <div>
                        <div className="text-xs text-gray-500">↓ Down</div>
                        <div className="text-sm font-medium">{formatBytes(resourceUsage.network.received)}/s</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500">↑ Up</div>
                        <div className="text-sm font-medium">{formatBytes(resourceUsage.network.sent)}/s</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Component List */}
            <div className="md:col-span-1 bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold mb-4">System Components</h2>
              
              <div className="space-y-2 max-h-[500px] overflow-y-auto">
                {systemStatus.components.map(component => (
                  <div
                    key={component.id}
                    onClick={() => setSelectedComponent(component.id)}
                    className={`p-3 rounded-lg flex items-center cursor-pointer ${
                      selectedComponent === component.id
                        ? 'bg-blue-50 border border-blue-200'
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                  >
                    <div className={`h-3 w-3 rounded-full mr-3 ${getStatusColor(component.status)}`}></div>
                    <div className="flex-1">
                      <div className="font-medium">{component.name}</div>
                      <div className="text-xs text-gray-500">
                        Last checked: {formatTime(component.lastChecked)}
                      </div>
                    </div>
                    <div className={`text-sm font-medium ${getStatusTextColor(component.status)}`}>
                      {getStatusText(component.status)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Component Details */}
            <div className="md:col-span-2">
              {componentDetails ? (
                <div className="bg-white rounded-lg shadow p-4">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-semibold">{componentDetails.name} Details</h2>
                    <div className="flex items-center space-x-2">
                      <div className={`h-3 w-3 rounded-full ${getStatusColor(componentDetails.status)}`}></div>
                      <span className={`text-sm font-medium ${getStatusTextColor(componentDetails.status)}`}>
                        {getStatusText(componentDetails.status)}
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-gray-700 mb-4">{componentDetails.details}</p>
                  
                  {/* Component Metrics */}
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                    {Object.entries(componentDetails.metrics).map(([key, value]) => (
                      value !== undefined && (
                        <div key={key} className="bg-gray-50 p-3 rounded-lg">
                          <div className="text-sm text-gray-500">{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</div>
                          <div className="text-lg font-semibold">
                            {key.includes('Time') ? `${value}ms` :
                             key.includes('Usage') ? `${value}%` :
                             key.includes('Rate') ? `${value}%` :
                             value}
                          </div>
                        </div>
                      )
                    ))}
                  </div>
                  
                  {/* AI Diagnosis */}
                  {componentDetails.status !== 'healthy' && (
                    <div className="mt-4">
                      {aiDiagnosis ? (
                        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
                          <div className="flex justify-between items-center mb-2">
                            <h3 className="font-semibold text-indigo-800">AI Diagnosis</h3>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              aiDiagnosis.severity === 'critical' ? 'bg-red-100 text-red-800' :
                              aiDiagnosis.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                              aiDiagnosis.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-blue-100 text-blue-800'
                            }`}>
                              {aiDiagnosis.severity.charAt(0).toUpperCase() + aiDiagnosis.severity.slice(1)} Severity
                            </span>
                          </div>
                          
                          <div className="mb-3">
                            <div className="font-medium text-gray-700">Issue Detected:</div>
                            <p className="text-gray-800">{aiDiagnosis.issue}</p>
                          </div>
                          
                          <div className="mb-3">
                            <div className="font-medium text-gray-700">Analysis:</div>
                            <p className="text-gray-800">{aiDiagnosis.analysis}</p>
                          </div>
                          
                          <div className="mb-3">
                            <div className="font-medium text-gray-700">Potential Impact:</div>
                            <p className="text-gray-800">{aiDiagnosis.potentialImpact}</p>
                          </div>
                          
                          <div>
                            <div className="font-medium text-green-700">Recommendation:</div>
                            <p className="text-gray-800">{aiDiagnosis.recommendation}</p>
                          </div>
                        </div>
                      ) : (
                        <button
                          onClick={diagnoseProblem}
                          disabled={isDiagnosing}
                          className={`w-full px-4 py-2 rounded-md text-center text-white ${
                            isDiagnosing
                              ? 'bg-gray-400 cursor-not-allowed'
                              : 'bg-indigo-600 hover:bg-indigo-700'
                          }`}
                        >
                          {isDiagnosing ? 'Running Diagnosis...' : 'Diagnose Problem with AI'}
                        </button>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                  <p className="text-xl">Select a component to view details</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
          <p className="text-xl">Unable to fetch system status</p>
          <button
            onClick={() => fetchSystemStatus(true)}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

export default SystemHealthDashboard;