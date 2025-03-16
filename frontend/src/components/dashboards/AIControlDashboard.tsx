import React, { useState, useEffect } from 'react';
import { mlService, aiService, healthService } from '../../services/api';

// Types
interface ModelInfo {
  id: string;
  name: string;
  type: string;
  loaded: boolean;
  size_mb?: number;
  description?: string;
}

interface QuantumJob {
  task_id: string;
  status: string;
  submitted_at: string;
  completed_at?: string;
  results?: any;
}

const AIControlDashboard: React.FC = () => {
  // State management
  const [mlModels, setMlModels] = useState<ModelInfo[]>([]);
  const [llmModels, setLlmModels] = useState<ModelInfo[]>([]);
  const [quantumStatus, setQuantumStatus] = useState({
    available: false,
    gpu_acceleration: false,
    circuit_limit: 0
  });
  const [quantumJobs, setQuantumJobs] = useState<QuantumJob[]>([]);
  const [gpuStatus, setGpuStatus] = useState({ available: false, utilization: 0 });
  const [isLoading, setIsLoading] = useState(true);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [feedback, setFeedback] = useState({ message: '', isError: false });

  // Load initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setIsLoading(true);

        // Load available ML models
        const mlResponse = await mlService.getAvailableModels();
        setMlModels(mlResponse.data.models || []);

        // Load available LLM models
        const llmResponse = await aiService.getAvailableLlmModels();
        setLlmModels(llmResponse.data.models || []);

        // Check quantum system status
        const quantumResponse = await aiService.getQuantumStatus();
        setQuantumStatus(quantumResponse.data.quantum_system || { available: false });

        // Get GPU status
        const gpuResponse = await healthService.getGpuStatus();
        setGpuStatus(gpuResponse.data.gpu || { available: false });

        setFeedback({ message: 'Systems loaded successfully', isError: false });
      } catch (error) {
        console.error('Error loading AI dashboard data:', error);
        setFeedback({
          message: 'Failed to load AI systems. Check server connection.',
          isError: true
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchInitialData();

    // Set up polling for real-time updates
    const intervalId = setInterval(() => {
      updateRealTimeData();
    }, 5000); // Update every 5 seconds

    return () => clearInterval(intervalId);
  }, []);

  // Function to update real-time data
  const updateRealTimeData = async () => {
    try {
      // Update GPU status
      const gpuResponse = await healthService.getGpuStatus();
      setGpuStatus(gpuResponse.data.gpu || { available: false });

      // Update quantum job status if there are active jobs
      if (quantumJobs.length > 0) {
        const updatedJobs = [...quantumJobs];
        let jobsChanged = false;

        for (let i = 0; i < updatedJobs.length; i++) {
          if (updatedJobs[i].status !== 'completed' && updatedJobs[i].status !== 'failed') {
            try {
              const jobResponse = await aiService.getQuantumJobStatus(updatedJobs[i].task_id);
              updatedJobs[i] = {
                ...updatedJobs[i],
                ...jobResponse.data.status
              };
              jobsChanged = true;
            } catch (error) {
              console.error(`Error updating job ${updatedJobs[i].task_id}:`, error);
            }
          }
        }

        if (jobsChanged) {
          setQuantumJobs(updatedJobs);
        }
      }

      // Check status of selected model if one is selected
      if (selectedModel) {
        try {
          const modelResponse = await mlService.getModelStatus(selectedModel);

          // Update the model list with new status
          setMlModels(prevModels =>
            prevModels.map(model =>
              model.id === selectedModel
                ? { ...model, ...modelResponse.data.status }
                : model
            )
          );
        } catch (error) {
          console.error(`Error updating model ${selectedModel} status:`, error);
        }
      }
    } catch (error) {
      console.error('Error updating real-time data:', error);
    }
  };

  // Handle model loading
  const handleLoadModel = async (modelId: string) => {
    try {
      setFeedback({ message: `Loading model ${modelId}...`, isError: false });
      await mlService.loadModel(modelId);
      setSelectedModel(modelId);
      setFeedback({ message: `Model ${modelId} loading initiated`, isError: false });

      // Update model list after a short delay to show loading status
      setTimeout(async () => {
        try {
          const modelResponse = await mlService.getModelStatus(modelId);
          setMlModels(prevModels =>
            prevModels.map(model =>
              model.id === modelId ? { ...model, ...modelResponse.data.status } : model
            )
          );
        } catch (error) {
          console.error(`Error updating model ${modelId} status:`, error);
        }
      }, 1000);
    } catch (error) {
      console.error(`Error loading model ${modelId}:`, error);
      setFeedback({ message: `Failed to load model ${modelId}`, isError: true });
    }
  };

  // Handle model unloading
  const handleUnloadModel = async (modelId: string) => {
    try {
      setFeedback({ message: `Unloading model ${modelId}...`, isError: false });
      await mlService.unloadModel(modelId);

      // Update model list
      setMlModels(prevModels =>
        prevModels.map(model =>
          model.id === modelId ? { ...model, loaded: false } : model
        )
      );

      if (selectedModel === modelId) {
        setSelectedModel(null);
      }

      setFeedback({ message: `Model ${modelId} unloaded successfully`, isError: false });
    } catch (error) {
      console.error(`Error unloading model ${modelId}:`, error);
      setFeedback({ message: `Failed to unload model ${modelId}`, isError: true });
    }
  };

  // Handle quantum job submission
  const handleSubmitQuantumJob = async () => {
    if (!quantumStatus.available) {
      setFeedback({ message: 'Quantum system is not available', isError: true });
      return;
    }

    try {
      setFeedback({ message: 'Submitting quantum job...', isError: false });

      // Example quantum circuit data - this would come from user input in a real app
      const circuitData = {
        circuit_type: 'grover',
        qubit_count: 4,
        iterations: 2,
        parameters: {
          target_state: '1011'
        }
      };

      const response = await aiService.executeQuantumCircuit(circuitData);

      // Add new job to the list
      const newJob: QuantumJob = {
        task_id: response.data.task_id,
        status: 'submitted',
        submitted_at: new Date().toISOString()
      };

      setQuantumJobs(prevJobs => [newJob, ...prevJobs]);
      setFeedback({ message: 'Quantum job submitted successfully', isError: false });
    } catch (error) {
      console.error('Error submitting quantum job:', error);
      setFeedback({ message: 'Failed to submit quantum job', isError: true });
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">AI Control Dashboard</h1>

      {/* Feedback message */}
      {feedback.message && (
        <div className={`mb-4 p-3 rounded ${feedback.isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {feedback.message}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* System Status Panel */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>

          <div className="mb-4">
            <div className="flex justify-between mb-2">
              <span>GPU Status:</span>
              <span className={`font-semibold ${gpuStatus.available ? 'text-green-600' : 'text-red-600'}`}>
                {gpuStatus.available ? 'Available' : 'Unavailable'}
              </span>
            </div>

            {gpuStatus.available && (
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full"
                  style={{ width: `${gpuStatus.utilization}%` }}
                ></div>
                <div className="text-right text-xs mt-1">
                  {gpuStatus.utilization}% Utilized
                </div>
              </div>
            )}
          </div>

          <div className="mb-4">
            <div className="flex justify-between">
              <span>Quantum System:</span>
              <span className={`font-semibold ${quantumStatus.available ? 'text-green-600' : 'text-red-600'}`}>
                {quantumStatus.available ? 'Available' : 'Unavailable'}
              </span>
            </div>
            {quantumStatus.available && (
              <div className="mt-2 text-sm">
                <div>GPU Acceleration: {quantumStatus.gpu_acceleration ? 'Enabled' : 'Disabled'}</div>
                <div>Circuit Limit: {quantumStatus.circuit_limit} qubits</div>
              </div>
            )}
          </div>
        </div>

        {/* ML Models Panel */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Machine Learning Models</h2>

          {isLoading ? (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
            </div>
          ) : (
            <div className="max-h-80 overflow-y-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {mlModels.map((model) => (
                    <tr key={model.id}>
                      <td className="px-4 py-2 whitespace-nowrap">{model.name}</td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${model.loaded ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                          {model.loaded ? 'Loaded' : 'Unloaded'}
                        </span>
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap text-sm">
                        {model.loaded ? (
                          <button
                            onClick={() => handleUnloadModel(model.id)}
                            className="text-red-600 hover:text-red-900 mr-2"
                          >
                            Unload
                          </button>
                        ) : (
                          <button
                            onClick={() => handleLoadModel(model.id)}
                            className="text-blue-600 hover:text-blue-900 mr-2"
                          >
                            Load
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* LLM Models Panel */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Language Models</h2>

          {isLoading ? (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
            </div>
          ) : (
            <div className="max-h-80 overflow-y-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {llmModels.map((model) => (
                    <tr key={model.id}>
                      <td className="px-4 py-2 whitespace-nowrap">{model.name}</td>
                      <td className="px-4 py-2 whitespace-nowrap">{model.type}</td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${model.loaded ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                          {model.loaded ? 'Loaded' : 'Not Loaded'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Quantum Jobs Panel */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Quantum Jobs</h2>

          <button
            onClick={handleSubmitQuantumJob}
            disabled={!quantumStatus.available}
            className={`mb-4 px-4 py-2 rounded text-white ${
              quantumStatus.available ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
            }`}
          >
            Submit New Quantum Job
          </button>

          <div className="max-h-60 overflow-y-auto">
            {quantumJobs.length === 0 ? (
              <div className="text-center text-gray-500 py-4">
                No quantum jobs found
              </div>
            ) : (
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submitted At</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {quantumJobs.map((job) => (
                    <tr key={job.task_id}>
                      <td className="px-4 py-2 text-sm font-mono whitespace-nowrap">
                        {job.task_id.substring(0, 8)}...
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          job.status === 'completed' ? 'bg-green-100 text-green-800' :
                          job.status === 'failed' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {job.status}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-sm whitespace-nowrap">
                        {new Date(job.submitted_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIControlDashboard;
