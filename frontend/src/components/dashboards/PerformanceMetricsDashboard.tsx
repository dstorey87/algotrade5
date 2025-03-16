import React, { useState, useEffect } from 'react';
import { tradingService, aiService } from '../../services/api';

// Types
interface PerformanceMetrics {
  total_trades: number;
  profitable_trades: number;
  loss_trades: number;
  win_rate: number;
  profit_factor: number;
  total_profit: number;
  avg_profit_per_trade: number;
  max_drawdown: number;
  current_drawdown: number;
  avg_trade_duration: string;
  best_trade: {
    pair: string;
    profit: number;
    open_date: string;
    close_date: string;
  };
  worst_trade: {
    pair: string;
    profit: number;
    open_date: string;
    close_date: string;
  };
}

interface PairPerformance {
  pair: string;
  trades: number;
  win_rate: number;
  profit: number;
  avg_profit: number;
  max_drawdown: number;
}

interface TimeframePerformance {
  timeframe: string;
  trades: number;
  win_rate: number;
  profit: number;
  profit_factor: number;
}

interface ProfitHistory {
  date: string;
  value: number;
  accumulated: number;
}

interface AiInsight {
  summary: string;
  key_metrics: string[];
  profitable_patterns: string[];
  risk_factors: string[];
  suggestions: string[];
}

const PerformanceMetricsDashboard: React.FC = () => {
  // State management
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [pairPerformance, setPairPerformance] = useState<PairPerformance[]>([]);
  const [timeframePerformance, setTimeframePerformance] = useState<TimeframePerformance[]>([]);
  const [profitHistory, setProfitHistory] = useState<ProfitHistory[]>([]);
  const [aiInsights, setAiInsights] = useState<AiInsight | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState({ message: '', isError: false });
  const [timePeriod, setTimePeriod] = useState<'day' | 'week' | 'month' | 'all'>('week');
  
  // Load initial data
  useEffect(() => {
    fetchPerformanceData();
  }, [timePeriod]);
  
  // Fetch all performance data
  const fetchPerformanceData = async () => {
    try {
      setIsLoading(true);
      setFeedback({ message: 'Loading performance data...', isError: false });
      
      // Fetch overall metrics
      const metricsResponse = await tradingService.getPerformanceMetrics(timePeriod);
      setMetrics(metricsResponse.data.metrics || null);
      
      // Fetch pair-specific performance
      const pairResponse = await tradingService.getPairPerformance(timePeriod);
      setPairPerformance(pairResponse.data.pairs || []);
      
      // Fetch timeframe-specific performance
      const timeframeResponse = await tradingService.getTimeframePerformance(timePeriod);
      setTimeframePerformance(timeframeResponse.data.timeframes || []);
      
      // Fetch profit history for chart
      const historyResponse = await tradingService.getProfitHistory(timePeriod);
      setProfitHistory(historyResponse.data.history || []);
      
      setFeedback({ message: '', isError: false });
    } catch (error) {
      console.error('Error fetching performance data:', error);
      setFeedback({
        message: 'Failed to fetch performance data. Check API connection.',
        isError: true
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  // Analyze performance with AI
  const analyzePerformance = async () => {
    try {
      setIsAnalyzing(true);
      setFeedback({ message: 'Analyzing performance data...', isError: false });
      
      const response = await aiService.analyzePerformance(timePeriod);
      setAiInsights(response.data.insights || null);
      
      setFeedback({ message: 'Analysis complete', isError: false });
    } catch (error) {
      console.error('Error analyzing performance:', error);
      setFeedback({
        message: 'Failed to analyze performance. AI service may be unavailable.',
        isError: true
      });
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  // Handle time period change
  const handlePeriodChange = (period: 'day' | 'week' | 'month' | 'all') => {
    setTimePeriod(period);
  };
  
  // Format profit/loss for display with color
  const formatProfit = (profit: number, includeSign = true) => {
    const formattedValue = includeSign 
      ? (profit >= 0 ? `+${profit.toFixed(2)}%` : `${profit.toFixed(2)}%`)
      : `${Math.abs(profit).toFixed(2)}%`;
      
    return {
      value: formattedValue,
      color: profit > 0 ? 'text-green-600' : profit < 0 ? 'text-red-600' : 'text-gray-600'
    };
  };
  
  // Format currency
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Performance Metrics</h1>
        
        <div className="flex items-center space-x-4">
          {/* Time Period Selector */}
          <div className="flex bg-white rounded-lg shadow">
            <button
              onClick={() => handlePeriodChange('day')}
              className={`px-4 py-2 text-sm ${
                timePeriod === 'day' 
                  ? 'bg-blue-600 text-white font-medium rounded-l-lg' 
                  : 'text-gray-600 hover:bg-gray-100 rounded-l-lg'
              }`}
            >
              Day
            </button>
            <button
              onClick={() => handlePeriodChange('week')}
              className={`px-4 py-2 text-sm ${
                timePeriod === 'week' 
                  ? 'bg-blue-600 text-white font-medium' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Week
            </button>
            <button
              onClick={() => handlePeriodChange('month')}
              className={`px-4 py-2 text-sm ${
                timePeriod === 'month' 
                  ? 'bg-blue-600 text-white font-medium' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Month
            </button>
            <button
              onClick={() => handlePeriodChange('all')}
              className={`px-4 py-2 text-sm ${
                timePeriod === 'all' 
                  ? 'bg-blue-600 text-white font-medium rounded-r-lg' 
                  : 'text-gray-600 hover:bg-gray-100 rounded-r-lg'
              }`}
            >
              All Time
            </button>
          </div>
          
          <button
            onClick={fetchPerformanceData}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Refresh
          </button>
          
          <button
            onClick={analyzePerformance}
            disabled={isAnalyzing || isLoading || !metrics}
            className={`px-4 py-2 rounded text-white ${
              isAnalyzing || isLoading || !metrics
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700'
            }`}
          >
            {isAnalyzing ? 'Analyzing...' : 'AI Analysis'}
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
      ) : metrics ? (
        <div className="space-y-6">
          {/* Key Metrics Overview */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-sm text-gray-500">Win Rate</div>
              <div className="text-2xl font-bold text-blue-600">
                {(metrics.win_rate * 100).toFixed(1)}%
              </div>
              <div className="text-xs text-gray-500">
                {metrics.profitable_trades} / {metrics.total_trades} trades
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-sm text-gray-500">Profit Factor</div>
              <div className="text-2xl font-bold text-blue-600">
                {metrics.profit_factor.toFixed(2)}
              </div>
              <div className="text-xs text-gray-500">
                Gains / Losses ratio
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-sm text-gray-500">Total Profit</div>
              <div className={`text-2xl font-bold ${metrics.total_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(metrics.total_profit)}
              </div>
              <div className="text-xs text-gray-500">
                {formatProfit(metrics.avg_profit_per_trade * 100).value} per trade
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-sm text-gray-500">Max Drawdown</div>
              <div className="text-2xl font-bold text-red-600">
                {(metrics.max_drawdown * 100).toFixed(2)}%
              </div>
              <div className="text-xs text-gray-500">
                Current: {(metrics.current_drawdown * 100).toFixed(2)}%
              </div>
            </div>
          </div>
          
          {/* Profit Chart (this would be a real chart in a complete implementation) */}
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold mb-4">Profit History</h2>
            <div className="h-64 bg-gray-100 rounded flex items-center justify-center text-gray-500">
              {/* In a real implementation, this would be replaced with a chart component */}
              <p>Profit chart would be displayed here using profitHistory data</p>
            </div>
          </div>
          
          {/* Trading Pairs Performance */}
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold mb-4">Trading Pairs Performance</h2>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pair</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trades</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Win Rate</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Profit</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Profit</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max DD</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {pairPerformance.map((pair) => {
                    const profitFormatted = formatProfit(pair.profit);
                    const avgProfitFormatted = formatProfit(pair.avg_profit);
                    
                    return (
                      <tr key={pair.pair}>
                        <td className="px-4 py-2 whitespace-nowrap font-medium">{pair.pair}</td>
                        <td className="px-4 py-2 whitespace-nowrap">{pair.trades}</td>
                        <td className="px-4 py-2 whitespace-nowrap">{(pair.win_rate * 100).toFixed(1)}%</td>
                        <td className={`px-4 py-2 whitespace-nowrap ${profitFormatted.color}`}>
                          {profitFormatted.value}
                        </td>
                        <td className={`px-4 py-2 whitespace-nowrap ${avgProfitFormatted.color}`}>
                          {avgProfitFormatted.value}
                        </td>
                        <td className="px-4 py-2 whitespace-nowrap text-red-600">
                          {(pair.max_drawdown * 100).toFixed(2)}%
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Timeframe Performance */}
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold mb-4">Timeframe Performance</h2>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timeframe</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trades</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Win Rate</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit Factor</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {timeframePerformance.map((tf) => {
                    const profitFormatted = formatProfit(tf.profit);
                    
                    return (
                      <tr key={tf.timeframe}>
                        <td className="px-4 py-2 whitespace-nowrap font-medium">{tf.timeframe}</td>
                        <td className="px-4 py-2 whitespace-nowrap">{tf.trades}</td>
                        <td className="px-4 py-2 whitespace-nowrap">{(tf.win_rate * 100).toFixed(1)}%</td>
                        <td className={`px-4 py-2 whitespace-nowrap ${profitFormatted.color}`}>
                          {profitFormatted.value}
                        </td>
                        <td className="px-4 py-2 whitespace-nowrap">
                          {tf.profit_factor.toFixed(2)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Best and Worst Trades */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold mb-4 text-green-700">Best Trade</h2>
              
              {metrics.best_trade && (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Pair:</span>
                    <span className="font-medium">{metrics.best_trade.pair}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Profit:</span>
                    <span className="font-medium text-green-600">
                      {formatProfit(metrics.best_trade.profit).value}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Opened:</span>
                    <span>{new Date(metrics.best_trade.open_date).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Closed:</span>
                    <span>{new Date(metrics.best_trade.close_date).toLocaleString()}</span>
                  </div>
                </div>
              )}
            </div>
            
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold mb-4 text-red-700">Worst Trade</h2>
              
              {metrics.worst_trade && (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Pair:</span>
                    <span className="font-medium">{metrics.worst_trade.pair}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Loss:</span>
                    <span className="font-medium text-red-600">
                      {formatProfit(metrics.worst_trade.profit).value}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Opened:</span>
                    <span>{new Date(metrics.worst_trade.open_date).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Closed:</span>
                    <span>{new Date(metrics.worst_trade.close_date).toLocaleString()}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* AI Insights */}
          {aiInsights && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold mb-4 text-indigo-800">AI Performance Analysis</h2>
              
              <div className="mb-4">
                <p className="text-indigo-700">{aiInsights.summary}</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h3 className="font-medium text-indigo-800 mb-2">Key Metrics</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {aiInsights.key_metrics.map((metric, index) => (
                      <li key={index} className="text-gray-700">{metric}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h3 className="font-medium text-green-800 mb-2">Profitable Patterns</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {aiInsights.profitable_patterns.map((pattern, index) => (
                      <li key={index} className="text-gray-700">{pattern}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h3 className="font-medium text-red-800 mb-2">Risk Factors</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {aiInsights.risk_factors.map((factor, index) => (
                      <li key={index} className="text-gray-700">{factor}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className="mt-4">
                <h3 className="font-medium text-indigo-800 mb-2">Improvement Suggestions</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {aiInsights.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-gray-700">{suggestion}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
          <p className="text-xl">No performance data available</p>
        </div>
      )}
    </div>
  );
};

export default PerformanceMetricsDashboard;