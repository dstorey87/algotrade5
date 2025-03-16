import React, { useState, useEffect } from 'react';
import { tradingService } from '../../services/api';

// Types
interface ActiveTrade {
  id: string;
  pair: string;
  entryPrice: number;
  currentPrice: number;
  profitLoss: number;
  profitLossPercentage: number;
  entryTime: string;
  stopLoss: number;
  takeProfit: number | null;
  strategy: string;
  confidence: number;
}

interface TradingPair {
  symbol: string;
  baseAsset: string;
  quoteAsset: string;
  price: number;
  volume24h: number;
  change24h: number;
  available: boolean;
}

interface AvailableStrategy {
  id: string;
  name: string;
  description: string;
  winRate: number;
  avgProfitPercentage: number;
  status: 'active' | 'inactive' | 'backtest' | 'optimizing';
  createdAt: string;
  lastUpdated: string;
}

interface SystemSettings {
  tradingEnabled: boolean;
  maxOpenTrades: number;
  maxRiskPerTrade: number;
  allowedPairs: string[];
  defaultStrategy: string;
  autoRiskManagement: boolean;
}

const TradingOperationsDashboard: React.FC = () => {
  // State management
  const [activeTrades, setActiveTrades] = useState<ActiveTrade[]>([]);
  const [availablePairs, setAvailablePairs] = useState<TradingPair[]>([]);
  const [strategies, setStrategies] = useState<AvailableStrategy[]>([]);
  const [systemSettings, setSystemSettings] = useState<SystemSettings | null>(null);
  const [selectedPair, setSelectedPair] = useState<string>('');
  const [selectedStrategy, setSelectedStrategy] = useState<string>('');
  const [orderType, setOrderType] = useState<'market' | 'limit'>('market');
  const [limitPrice, setLimitPrice] = useState<number | ''>('');
  const [stopLossPercentage, setStopLossPercentage] = useState<number>(1.5);
  const [takeProfitPercentage, setTakeProfitPercentage] = useState<number>(3.0);
  const [amount, setAmount] = useState<number | ''>('');
  const [feedback, setFeedback] = useState({ message: '', isError: false });
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [tradingEnabled, setTradingEnabled] = useState(false);
  
  // Load initial data
  useEffect(() => {
    Promise.all([
      fetchActiveTrades(),
      fetchAvailablePairs(),
      fetchStrategies(),
      fetchSystemSettings()
    ]).then(() => {
      setIsLoading(false);
    }).catch(error => {
      console.error('Error loading initial data:', error);
      setFeedback({
        message: 'Failed to load trading data. Please try again.',
        isError: true
      });
      setIsLoading(false);
    });
  }, []);
  
  // Fetch active trades
  const fetchActiveTrades = async () => {
    try {
      const response = await tradingService.getActiveTrades();
      setActiveTrades(response.data);
    } catch (error) {
      console.error('Error fetching active trades:', error);
      throw error;
    }
  };
  
  // Fetch available pairs
  const fetchAvailablePairs = async () => {
    try {
      const response = await tradingService.getAvailablePairs();
      setAvailablePairs(response.data);
      
      // Set default selected pair if none is selected
      if (!selectedPair && response.data.length > 0) {
        setSelectedPair(response.data[0].symbol);
      }
    } catch (error) {
      console.error('Error fetching available pairs:', error);
      throw error;
    }
  };
  
  // Fetch available strategies
  const fetchStrategies = async () => {
    try {
      const response = await tradingService.getAvailableStrategies();
      setStrategies(response.data);
      
      // Set default selected strategy if none is selected
      if (!selectedStrategy && response.data.length > 0) {
        const activeStrategies = response.data.filter(s => s.status === 'active');
        if (activeStrategies.length > 0) {
          setSelectedStrategy(activeStrategies[0].id);
        } else if (response.data.length > 0) {
          setSelectedStrategy(response.data[0].id);
        }
      }
    } catch (error) {
      console.error('Error fetching strategies:', error);
      throw error;
    }
  };
  
  // Fetch system settings
  const fetchSystemSettings = async () => {
    try {
      const response = await tradingService.getSystemSettings();
      setSystemSettings(response.data);
      setTradingEnabled(response.data.tradingEnabled);
    } catch (error) {
      console.error('Error fetching system settings:', error);
      throw error;
    }
  };
  
  // Execute trade
  const executeTrade = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedPair || !selectedStrategy || amount === '') {
      setFeedback({
        message: 'Please fill in all required fields',
        isError: true
      });
      return;
    }
    
    try {
      setIsSubmitting(true);
      setFeedback({ message: 'Executing trade...', isError: false });
      
      const tradeParams = {
        pair: selectedPair,
        strategyId: selectedStrategy,
        orderType,
        limitPrice: orderType === 'limit' ? limitPrice : undefined,
        stopLossPercentage,
        takeProfitPercentage,
        amount: typeof amount === 'number' ? amount : parseFloat(amount)
      };
      
      const response = await tradingService.executeTrade(tradeParams);
      
      setFeedback({
        message: `Trade executed successfully! Order ID: ${response.data.orderId}`,
        isError: false
      });
      
      // Refresh active trades
      fetchActiveTrades();
      
      // Reset form
      if (orderType === 'limit') {
        setLimitPrice('');
      }
      setAmount('');
    } catch (error) {
      console.error('Error executing trade:', error);
      setFeedback({
        message: `Failed to execute trade: ${(error as Error).message || 'Unknown error'}`,
        isError: true
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // Close a trade
  const closeTrade = async (tradeId: string) => {
    if (!confirm('Are you sure you want to close this trade?')) {
      return;
    }
    
    try {
      setFeedback({ message: 'Closing trade...', isError: false });
      
      await tradingService.closeTrade(tradeId);
      
      setFeedback({
        message: 'Trade closed successfully',
        isError: false
      });
      
      // Refresh active trades
      fetchActiveTrades();
    } catch (error) {
      console.error('Error closing trade:', error);
      setFeedback({
        message: `Failed to close trade: ${(error as Error).message || 'Unknown error'}`,
        isError: true
      });
    }
  };
  
  // Cancel all trades
  const cancelAllTrades = async () => {
    if (!confirm('Are you sure you want to cancel all active trades? This will close all positions.')) {
      return;
    }
    
    try {
      setFeedback({ message: 'Cancelling all trades...', isError: false });
      
      await tradingService.cancelAllTrades();
      
      setFeedback({
        message: 'All trades cancelled successfully',
        isError: false
      });
      
      // Refresh active trades
      fetchActiveTrades();
    } catch (error) {
      console.error('Error cancelling all trades:', error);
      setFeedback({
        message: `Failed to cancel trades: ${(error as Error).message || 'Unknown error'}`,
        isError: true
      });
    }
  };
  
  // Toggle trading
  const toggleTradingSystem = async () => {
    try {
      const newStatus = !tradingEnabled;
      setFeedback({ 
        message: `${newStatus ? 'Enabling' : 'Disabling'} trading system...`, 
        isError: false 
      });
      
      await tradingService.setTradingEnabled(newStatus);
      
      setTradingEnabled(newStatus);
      setFeedback({
        message: `Trading system ${newStatus ? 'enabled' : 'disabled'} successfully`,
        isError: false
      });
      
      // Refresh system settings
      fetchSystemSettings();
    } catch (error) {
      console.error('Error toggling trading system:', error);
      setFeedback({
        message: `Failed to ${tradingEnabled ? 'disable' : 'enable'} trading system`,
        isError: true
      });
      // Revert the toggle
      setTradingEnabled(!tradingEnabled);
    }
  };
  
  // Get a trading pair by symbol
  const getPairBySymbol = (symbol: string) => {
    return availablePairs.find(pair => pair.symbol === symbol);
  };
  
  // Get a strategy by ID
  const getStrategyById = (id: string) => {
    return strategies.find(strategy => strategy.id === id);
  };
  
  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 6
    }).format(value);
  };
  
  // Format percentage
  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };
  
  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };
  
  // Handle order type change
  const handleOrderTypeChange = (type: 'market' | 'limit') => {
    setOrderType(type);
    if (type === 'market') {
      setLimitPrice('');
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Trading Operations</h1>
        
        <div className="flex items-center space-x-3">
          <span className={`px-3 py-1 rounded-full text-white ${
            tradingEnabled ? 'bg-green-500' : 'bg-red-500'
          }`}>
            Trading {tradingEnabled ? 'Enabled' : 'Disabled'}
          </span>
          
          <button
            onClick={toggleTradingSystem}
            className={`px-4 py-2 rounded-md text-white ${
              tradingEnabled 
                ? 'bg-red-600 hover:bg-red-700' 
                : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {tradingEnabled ? 'Disable Trading' : 'Enable Trading'}
          </button>
          
          {activeTrades.length > 0 && (
            <button
              onClick={cancelAllTrades}
              className="px-4 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700"
            >
              Cancel All Trades
            </button>
          )}
        </div>
      </div>
      
      {/* Feedback message */}
      {feedback.message && (
        <div className={`mb-4 p-3 rounded ${
          feedback.isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
        }`}>
          {feedback.message}
        </div>
      )}
      
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-700"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Active Trades Section */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h2 className="text-xl font-semibold">Active Trades</h2>
            </div>
            
            {activeTrades.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pair</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Entry Price</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P/L</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stop Loss</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Strategy</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {activeTrades.map(trade => (
                      <tr key={trade.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="font-medium text-gray-900">{trade.pair}</div>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          {formatCurrency(trade.entryPrice)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          {formatCurrency(trade.currentPrice)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            trade.profitLossPercentage >= 0 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {formatPercentage(trade.profitLossPercentage)}
                          </span>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          {formatCurrency(trade.stopLoss)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="ml-1">
                              <div className="text-sm font-medium text-gray-900">
                                {trade.strategy}
                              </div>
                              <div className="text-xs text-gray-500">
                                Confidence: {trade.confidence.toFixed(1)}%
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(trade.entryTime)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => closeTrade(trade.id)}
                            className="text-indigo-600 hover:text-indigo-900"
                          >
                            Close
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="p-6 text-center text-gray-500">
                No active trades at the moment
              </div>
            )}
          </div>
          
          {/* New Trade Form */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h2 className="text-xl font-semibold">New Trade</h2>
            </div>
            
            <form onSubmit={executeTrade} className="p-4">
              {/* Trading Pair Selection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Trading Pair
                </label>
                <select
                  value={selectedPair}
                  onChange={(e) => setSelectedPair(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  disabled={isSubmitting || !tradingEnabled}
                >
                  {availablePairs.map(pair => (
                    <option key={pair.symbol} value={pair.symbol}>
                      {pair.symbol} ({formatCurrency(pair.price)}{pair.change24h >= 0 ? ' +' : ' '}{pair.change24h.toFixed(2)}%)
                    </option>
                  ))}
                </select>
              </div>
              
              {/* Strategy Selection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Trading Strategy
                </label>
                <select
                  value={selectedStrategy}
                  onChange={(e) => setSelectedStrategy(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  disabled={isSubmitting || !tradingEnabled}
                >
                  {strategies.map(strategy => (
                    <option key={strategy.id} value={strategy.id} disabled={strategy.status !== 'active'}>
                      {strategy.name} ({strategy.winRate.toFixed(1)}% win rate)
                      {strategy.status !== 'active' ? ' - ' + strategy.status : ''}
                    </option>
                  ))}
                </select>
                {selectedStrategy && (
                  <div className="mt-1 text-sm text-gray-500">
                    {getStrategyById(selectedStrategy)?.description}
                  </div>
                )}
              </div>
              
              {/* Order Type */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Order Type
                </label>
                <div className="flex">
                  <button
                    type="button"
                    onClick={() => handleOrderTypeChange('market')}
                    className={`px-4 py-2 rounded-l-md ${
                      orderType === 'market'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                    disabled={isSubmitting || !tradingEnabled}
                  >
                    Market
                  </button>
                  <button
                    type="button"
                    onClick={() => handleOrderTypeChange('limit')}
                    className={`px-4 py-2 rounded-r-md ${
                      orderType === 'limit'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                    disabled={isSubmitting || !tradingEnabled}
                  >
                    Limit
                  </button>
                </div>
              </div>
              
              {/* Limit Price (for limit orders) */}
              {orderType === 'limit' && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Limit Price
                  </label>
                  <input
                    type="number"
                    value={limitPrice}
                    onChange={(e) => setLimitPrice(e.target.value ? parseFloat(e.target.value) : '')}
                    step="0.000001"
                    min="0"
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    disabled={isSubmitting || !tradingEnabled}
                    required
                  />
                </div>
              )}
              
              {/* Amount */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Amount (USD)
                </label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value ? parseFloat(e.target.value) : '')}
                  step="0.01"
                  min="0"
                  max={systemSettings?.maxRiskPerTrade || 10}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  disabled={isSubmitting || !tradingEnabled}
                  required
                />
                {systemSettings && (
                  <div className="mt-1 text-sm text-gray-500">
                    Maximum amount: {formatCurrency(systemSettings.maxRiskPerTrade)}
                  </div>
                )}
              </div>
              
              {/* Stop Loss */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Stop Loss ({stopLossPercentage}%)
                </label>
                <input
                  type="range"
                  value={stopLossPercentage}
                  onChange={(e) => setStopLossPercentage(parseFloat(e.target.value))}
                  min="0.5"
                  max="10"
                  step="0.1"
                  className="block w-full"
                  disabled={isSubmitting || !tradingEnabled}
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>0.5%</span>
                  <span>5%</span>
                  <span>10%</span>
                </div>
              </div>
              
              {/* Take Profit */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Take Profit ({takeProfitPercentage}%)
                </label>
                <input
                  type="range"
                  value={takeProfitPercentage}
                  onChange={(e) => setTakeProfitPercentage(parseFloat(e.target.value))}
                  min="1"
                  max="20"
                  step="0.1"
                  className="block w-full"
                  disabled={isSubmitting || !tradingEnabled}
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>1%</span>
                  <span>10%</span>
                  <span>20%</span>
                </div>
              </div>
              
              {/* Submit Button */}
              <button
                type="submit"
                className={`w-full px-4 py-2 text-white rounded-md ${
                  !tradingEnabled
                    ? 'bg-gray-400 cursor-not-allowed'
                    : isSubmitting
                      ? 'bg-indigo-400 cursor-wait'
                      : 'bg-indigo-600 hover:bg-indigo-700'
                }`}
                disabled={isSubmitting || !tradingEnabled}
              >
                {isSubmitting ? 'Executing...' : 'Execute Trade'}
              </button>
              
              {!tradingEnabled && (
                <div className="mt-2 text-center text-sm text-red-600">
                  Trading is currently disabled. Enable trading to execute trades.
                </div>
              )}
            </form>
          </div>
        </div>
      )}
      
      {/* System Settings Section */}
      {systemSettings && (
        <div className="mt-6 bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">System Settings</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-500">Max Open Trades</div>
              <div className="text-xl font-medium">{systemSettings.maxOpenTrades}</div>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-500">Max Risk Per Trade</div>
              <div className="text-xl font-medium">{formatCurrency(systemSettings.maxRiskPerTrade)}</div>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-500">Default Strategy</div>
              <div className="text-xl font-medium">{systemSettings.defaultStrategy}</div>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg md:col-span-2">
              <div className="text-sm text-gray-500">Auto Risk Management</div>
              <div className="text-xl font-medium">
                {systemSettings.autoRiskManagement ? 'Enabled' : 'Disabled'}
              </div>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-500">Allowed Pairs</div>
              <div className="text-sm font-medium mt-1">
                {systemSettings.allowedPairs.length > 5 
                  ? `${systemSettings.allowedPairs.slice(0, 5).join(', ')} +${systemSettings.allowedPairs.length - 5} more`
                  : systemSettings.allowedPairs.join(', ')}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TradingOperationsDashboard;