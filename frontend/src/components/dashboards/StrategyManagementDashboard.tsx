import React, { useState, useEffect } from 'react';
import { tradingService, aiService } from '../../services/api';

// Types
interface StrategyDetails {
  id: string;
  name: string;
  description: string;
  version: string;
  creation_date: string;
  last_modified: string;
  author: string;
  status: 'active' | 'inactive' | 'testing' | 'optimizing';
  tags: string[];
  timeframes: string[];
  pairs: string[];
  parameters: Record<string, any>;
}

interface StrategyPerformance {
  win_rate: number;
  profit_factor: number;
  avg_profit: number;
  avg_loss: number;
  max_drawdown: number;
  total_trades: number;
  profitable_trades: number;
  timeframe: string;
  pair: string;
  period: string;
  backtest_date: string;
}

interface StrategyAnalysis {
  recommendation: string;
  summary: string;
  strengths: string[];
  weaknesses: string[];
  market_conditions: {
    suitable: string[];
    unsuitable: string[];
  };
  improvement_suggestions: string[];
}

const StrategyManagementDashboard: React.FC = () => {
  // State management
  const [strategies, setStrategies] = useState<StrategyDetails[]>([]);
  const [selectedStrategy, setSelectedStrategy] = useState<string | null>(null);
  const [currentDetails, setCurrentDetails] = useState<StrategyDetails | null>(null);
  const [performanceData, setPerformanceData] = useState<StrategyPerformance | null>(null);
  const [timeframeOptions, setTimeframeOptions] = useState<string[]>(['5m', '15m', '1h', '4h', '1d']);
  const [pairOptions, setPairOptions] = useState<string[]>(['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'SOL/USDT']);
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('1h');
  const [selectedPair, setSelectedPair] = useState<string>('BTC/USDT');
  const [strategyAnalysis, setStrategyAnalysis] = useState<StrategyAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [actionInProgress, setActionInProgress] = useState(false);
  const [feedback, setFeedback] = useState({ message: '', isError: false });
  const [activeTab, setActiveTab] = useState<'details' | 'performance' | 'analysis'>('details');
  
  // Load initial data
  useEffect(() => {
    fetchStrategies();
  }, []);
  
  // Fetch strategy when selection changes
  useEffect(() => {
    if (selectedStrategy) {
      fetchStrategyDetails(selectedStrategy);
      fetchStrategyPerformance(selectedStrategy, selectedTimeframe, selectedPair);
    } else {
      setCurrentDetails(null);
      setPerformanceData(null);
      setStrategyAnalysis(null);
    }
  }, [selectedStrategy, selectedTimeframe, selectedPair]);
  
  // Fetch all available strategies
  const fetchStrategies = async () => {
    try {
      setIsLoading(true);
      
      const response = await tradingService.getAvailableStrategies();
      setStrategies(response.data.strategies || []);
      
      // Auto-select the first strategy if available
      if (response.data.strategies && response.data.strategies.length > 0) {
        setSelectedStrategy(response.data.strategies[0].id);
      }
    } catch (error) {
      console.error('Error fetching strategies:', error);
      setFeedback({
        message: 'Failed to fetch strategy data. Check API connection.',
        isError: true
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  // Fetch details for a specific strategy
  const fetchStrategyDetails = async (strategyId: string) => {
    try {
      setIsLoading(true);
      
      const response = await tradingService.getStrategyDetails(strategyId);
      setCurrentDetails(response.data.details || null);
      
      // Extract available timeframes and pairs from the strategy
      if (response.data.details) {
        setTimeframeOptions(response.data.details.timeframes || ['5m', '15m', '1h', '4h', '1d']);
        setPairOptions(response.data.details.pairs || ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'SOL/USDT']);
      }
    } catch (error) {
      console.error(`Error fetching strategy details for ${strategyId}:`, error);
      setFeedback({
        message: `Failed to fetch details for strategy ${strategyId}. Check API connection.`,
        isError: true
      });
      setCurrentDetails(null);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Fetch performance data for a strategy
  const fetchStrategyPerformance = async (strategyId: string, timeframe: string, pair: string) => {
    try {
      setIsLoading(true);
      
      // In a real implementation, this would call the API
      // For demonstration, we'll create sample data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Sample performance data
      const samplePerformance: StrategyPerformance = {
        win_rate: 0.78,
        profit_factor: 2.3,
        avg_profit: 0.014,
        avg_loss: -0.0075,
        max_drawdown: 0.075,
        total_trades: 124,
        profitable_trades: 97,
        timeframe: timeframe,
        pair: pair,
        period: '30 days',
        backtest_date: new Date().toISOString()
      };
      
      setPerformanceData(samplePerformance);
    } catch (error) {
      console.error(`Error fetching performance data for ${strategyId}:`, error);
      setFeedback({
        message: `Failed to fetch performance data for strategy ${strategyId}. Check API connection.`,
        isError: true
      });
      setPerformanceData(null);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Run AI analysis on the strategy
  const analyzeStrategy = async () => {
    if (!selectedStrategy) return;
    
    try {
      setIsAnalyzing(true);
      setFeedback({ message: 'Analyzing strategy...', isError: false });
      
      const response = await aiService.analyzeStrategy(
        selectedStrategy,
        selectedTimeframe,
        selectedPair
      );
      
      setStrategyAnalysis(response.data.analysis || null);
      setFeedback({ message: 'Strategy analysis complete', isError: false });
      setActiveTab('analysis');
    } catch (error) {
      console.error(`Error analyzing strategy ${selectedStrategy}:`, error);
      setFeedback({
        message: 'Failed to analyze strategy. AI service may be unavailable.',
        isError: true
      });
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  // Activate a strategy
  const activateStrategy = async () => {
    if (!selectedStrategy) return;
    
    try {
      setActionInProgress(true);
      setFeedback({ message: 'Activating strategy...', isError: false });
      
      const response = await tradingService.activateStrategy(selectedStrategy);
      
      if (response.data.success) {
        setFeedback({ 
          message: `Strategy ${selectedStrategy} activated successfully`,
          isError: false
        });
        
        // Update the strategy list to reflect the change
        setStrategies(prevStrategies => 
          prevStrategies.map(strategy => 
            strategy.id === selectedStrategy 
              ? { ...strategy, status: 'active' }
              : strategy.status === 'active' 
                ? { ...strategy, status: 'inactive' }
                : strategy
          )
        );
        
        // Update current details if it's the selected strategy
        if (currentDetails && currentDetails.id === selectedStrategy) {
          setCurrentDetails({ ...currentDetails, status: 'active' });
        }
      } else {
        setFeedback({
          message: `Failed to activate strategy: ${response.data.message}`,
          isError: true
        });
      }
    } catch (error) {
      console.error(`Error activating strategy ${selectedStrategy}:`, error);
      setFeedback({
        message: 'Failed to activate strategy. Check API connection.',
        isError: true
      });
    } finally {
      setActionInProgress(false);
    }
  };
  
  // Handle strategy selection change
  const handleStrategyChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const strategyId = e.target.value;
    setSelectedStrategy(strategyId === 'none' ? null : strategyId);
  };
  
  // Handle timeframe selection change
  const handleTimeframeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedTimeframe(e.target.value);
  };
  
  // Handle pair selection change
  const handlePairChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPair(e.target.value);
  };
  
  // Switch between tabs
  const switchTab = (tab: 'details' | 'performance' | 'analysis') => {
    setActiveTab(tab);
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Strategy Management</h1>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={fetchStrategies}
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
      
      {/* Strategy Selection */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
          <div className="sm:w-1/3">
            <label htmlFor="strategy" className="block text-sm font-medium text-gray-700 mb-1">
              Select Strategy
            </label>
            <select
              id="strategy"
              className="block w-full p-2 border border-gray-300 rounded-md"
              value={selectedStrategy || 'none'}
              onChange={handleStrategyChange}
              disabled={isLoading || actionInProgress}
            >
              <option value="none">-- Select a strategy --</option>
              {strategies.map(strategy => (
                <option key={strategy.id} value={strategy.id}>
                  {strategy.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="sm:w-1/3">
            <label htmlFor="timeframe" className="block text-sm font-medium text-gray-700 mb-1">
              Timeframe
            </label>
            <select
              id="timeframe"
              className="block w-full p-2 border border-gray-300 rounded-md"
              value={selectedTimeframe}
              onChange={handleTimeframeChange}
              disabled={!selectedStrategy || isLoading || actionInProgress}
            >
              {timeframeOptions.map(tf => (
                <option key={tf} value={tf}>
                  {tf}
                </option>
              ))}
            </select>
          </div>
          
          <div className="sm:w-1/3">
            <label htmlFor="pair" className="block text-sm font-medium text-gray-700 mb-1">
              Trading Pair
            </label>
            <select
              id="pair"
              className="block w-full p-2 border border-gray-300 rounded-md"
              value={selectedPair}
              onChange={handlePairChange}
              disabled={!selectedStrategy || isLoading || actionInProgress}
            >
              {pairOptions.map(pair => (
                <option key={pair} value={pair}>
                  {pair}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
      
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-700"></div>
        </div>
      ) : selectedStrategy && currentDetails ? (
        <div className="bg-white rounded-lg shadow">
          {/* Strategy Header */}
          <div className="p-4 border-b">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-semibold">{currentDetails.name}</h2>
                <p className="text-gray-600">{currentDetails.description}</p>
              </div>
              
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  currentDetails.status === 'active' ? 'bg-green-100 text-green-800' :
                  currentDetails.status === 'testing' ? 'bg-blue-100 text-blue-800' :
                  currentDetails.status === 'optimizing' ? 'bg-purple-100 text-purple-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {currentDetails.status}
                </span>
                
                <button
                  onClick={activateStrategy}
                  disabled={actionInProgress || currentDetails.status === 'active'}
                  className={`px-4 py-2 rounded-md text-sm text-white ${
                    actionInProgress || currentDetails.status === 'active'
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {currentDetails.status === 'active' ? 'Active' : 'Activate'}
                </button>
                
                <button
                  onClick={analyzeStrategy}
                  disabled={isAnalyzing}
                  className={`px-4 py-2 rounded-md text-sm text-white ${
                    isAnalyzing
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-indigo-600 hover:bg-indigo-700'
                  }`}
                >
                  {isAnalyzing ? 'Analyzing...' : 'Analyze with AI'}
                </button>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mt-2">
              {currentDetails.tags.map(tag => (
                <span key={tag} className="px-2.5 py-0.5 rounded-full text-xs bg-blue-100 text-blue-800">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          
          {/* Tabs */}
          <div className="border-b">
            <nav className="flex -mb-px">
              <button
                onClick={() => switchTab('details')}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  activeTab === 'details' 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Strategy Details
              </button>
              
              <button
                onClick={() => switchTab('performance')}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  activeTab === 'performance' 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Performance Metrics
              </button>
              
              <button
                onClick={() => switchTab('analysis')}
                disabled={!strategyAnalysis}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  activeTab === 'analysis' 
                    ? 'border-blue-500 text-blue-600' 
                    : !strategyAnalysis
                    ? 'border-transparent text-gray-400 cursor-not-allowed'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                AI Analysis
              </button>
            </nav>
          </div>
          
          {/* Tab Content */}
          <div className="p-4">
            {/* Strategy Details Tab */}
            {activeTab === 'details' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">General Information</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Version:</span>
                      <span>{currentDetails.version}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Author:</span>
                      <span>{currentDetails.author}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Created:</span>
                      <span>{new Date(currentDetails.creation_date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Last Modified:</span>
                      <span>{new Date(currentDetails.last_modified).toLocaleDateString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Supported Timeframes:</span>
                      <span>{currentDetails.timeframes.join(', ')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Supported Pairs:</span>
                      <span>{currentDetails.pairs.length} pairs</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-3">Strategy Parameters</h3>
                  <div className="space-y-2">
                    {Object.entries(currentDetails.parameters).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-gray-600">{key}:</span>
                        <span>{typeof value === 'object' ? JSON.stringify(value) : value.toString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
            
            {/* Performance Metrics Tab */}
            {activeTab === 'performance' && performanceData && (
              <div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-500">Win Rate</div>
                    <div className="text-2xl font-bold text-green-600">
                      {(performanceData.win_rate * 100).toFixed(1)}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {performanceData.profitable_trades} / {performanceData.total_trades} trades
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-500">Profit Factor</div>
                    <div className="text-2xl font-bold text-blue-600">
                      {performanceData.profit_factor.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-500">
                      Gross Profit / Gross Loss
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-500">Avg. Profit</div>
                    <div className="text-2xl font-bold text-green-600">
                      {(performanceData.avg_profit * 100).toFixed(2)}%
                    </div>
                    <div className="text-xs text-gray-500">
                      Per winning trade
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-500">Max Drawdown</div>
                    <div className="text-2xl font-bold text-red-600">
                      {(performanceData.max_drawdown * 100).toFixed(2)}%
                    </div>
                    <div className="text-xs text-gray-500">
                      Largest drop from peak
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Performance Details</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total Trades:</span>
                        <span>{performanceData.total_trades}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Profitable Trades:</span>
                        <span className="text-green-600">{performanceData.profitable_trades}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Loss Trades:</span>
                        <span className="text-red-600">{performanceData.total_trades - performanceData.profitable_trades}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Average Loss:</span>
                        <span className="text-red-600">{(performanceData.avg_loss * 100).toFixed(2)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Test Parameters</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Timeframe:</span>
                        <span>{performanceData.timeframe}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Trading Pair:</span>
                        <span>{performanceData.pair}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Test Period:</span>
                        <span>{performanceData.period}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Backtest Date:</span>
                        <span>{new Date(performanceData.backtest_date).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* AI Analysis Tab */}
            {activeTab === 'analysis' && strategyAnalysis && (
              <div>
                <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 mb-6">
                  <h3 className="text-lg font-semibold text-indigo-800 mb-2">AI Recommendation</h3>
                  <p className="text-indigo-700">{strategyAnalysis.recommendation}</p>
                </div>
                
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3">Strategy Summary</h3>
                  <p className="text-gray-700">{strategyAnalysis.summary}</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h3 className="text-lg font-semibold mb-3 text-green-700">Strengths</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      {strategyAnalysis.strengths.map((strength, index) => (
                        <li key={index} className="text-gray-700">{strength}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-3 text-red-700">Weaknesses</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      {strategyAnalysis.weaknesses.map((weakness, index) => (
                        <li key={index} className="text-gray-700">{weakness}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3">Market Conditions</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-green-50 p-3 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">Suitable For</h4>
                      <ul className="list-disc pl-5 space-y-1">
                        {strategyAnalysis.market_conditions.suitable.map((condition, index) => (
                          <li key={index} className="text-gray-700">{condition}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="bg-red-50 p-3 rounded-lg">
                      <h4 className="font-medium text-red-800 mb-2">Unsuitable For</h4>
                      <ul className="list-disc pl-5 space-y-1">
                        {strategyAnalysis.market_conditions.unsuitable.map((condition, index) => (
                          <li key={index} className="text-gray-700">{condition}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-3">Improvement Suggestions</h3>
                  <ul className="list-disc pl-5 space-y-2">
                    {strategyAnalysis.improvement_suggestions.map((suggestion, index) => (
                      <li key={index} className="text-gray-700">{suggestion}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
          <p className="text-xl">Please select a strategy to view details</p>
        </div>
      )}
    </div>
  );
};

export default StrategyManagementDashboard;