import React, { useState, useEffect } from 'react';
import { tradingService } from '@/services/tradingService';

// Types
interface Trade {
  id: string;
  pair: string;
  open_rate: number;
  current_rate: number;
  profit_ratio: number;
  profit_abs: number;
  open_date: string;
  close_date: string | null;
  stake_amount: number;
  stop_loss_abs: number;
  take_profit_abs: number | null;
  strategy: string;
  enter_tag: string;
}

interface TradingStatusData {
  status: string;
  running: boolean;
  max_open_trades: number;
  stake_amount: number;
  stake_currency: string;
  strategies: string[];
  timeframe: string;
}

const TradingOperationsDashboard: React.FC = () => {
  // State management
  const [activeTrades, setActiveTrades] = useState<Trade[]>([]);
  const [tradingStatus, setTradingStatus] = useState<TradingStatusData | null>(null);
  const [selectedStrategy, setSelectedStrategy] = useState<string>('');
  const [feedback, setFeedback] = useState({ message: '', isError: false });
  const [isLoading, setIsLoading] = useState(true);

  // Load initial data
  useEffect(() => {
    Promise.all([
      fetchActiveTrades(),
      fetchTradingStatus()
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
      const trades = await tradingService.getTrades();
      // Filter for active trades (trades without a close_date)
      const activeTrades = trades.filter((trade: Trade) => trade.close_date === null);
      setActiveTrades(activeTrades);
    } catch (error) {
      console.error('Error fetching active trades:', error);
      throw error;
    }
  };

  // Fetch trading status
  const fetchTradingStatus = async () => {
    try {
      const status = await tradingService.getTradingStatus();
      setTradingStatus(status);
      
      // Set default strategy if available
      if (status.strategies?.length > 0 && !selectedStrategy) {
        setSelectedStrategy(status.strategies[0]);
      }
    } catch (error) {
      console.error('Error fetching trading status:', error);
      throw error;
    }
  };

  // Toggle trading
  const toggleTradingSystem = async () => {
    if (!tradingStatus) return;
    
    try {
      const isRunning = tradingStatus.running;
      setFeedback({
        message: `${isRunning ? 'Stopping' : 'Starting'} trading system...`,
        isError: false
      });

      if (isRunning) {
        await tradingService.stopTrading();
      } else {
        await tradingService.startTrading(selectedStrategy);
      }

      await fetchTradingStatus();
      
      setFeedback({
        message: `Trading system ${isRunning ? 'stopped' : 'started'} successfully`,
        isError: false
      });
    } catch (error) {
      console.error('Error toggling trading system:', error);
      setFeedback({
        message: `Failed to ${tradingStatus.running ? 'stop' : 'start'} trading system`,
        isError: true
      });
    }
  };

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: tradingStatus?.stake_currency || 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 6
    }).format(value);
  };

  // Format percentage
  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${(value * 100).toFixed(2)}%`;
  };

  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="p-6 bg-gray-100 dark:bg-gray-900 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Trading Operations</h1>

        <div className="flex items-center space-x-3">
          {tradingStatus && (
            <>
              <span className={`px-3 py-1 rounded-full text-white ${
                tradingStatus.running ? 'bg-green-500' : 'bg-red-500'
              }`}>
                Trading {tradingStatus.running ? 'Active' : 'Inactive'}
              </span>

              <button
                onClick={toggleTradingSystem}
                className={`px-4 py-2 rounded-md text-white ${
                  tradingStatus.running
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {tradingStatus.running ? 'Stop Trading' : 'Start Trading'}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Feedback message */}
      {feedback.message && (
        <div className={`mb-4 p-3 rounded ${
          feedback.isError ? 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200' 
          : 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200'
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
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Active Trades</h2>
            </div>

            {activeTrades.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pair</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Entry Price</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Current</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">P/L</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Stop Loss</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Strategy</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Time</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {activeTrades.map(trade => (
                      <tr key={trade.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="font-medium text-gray-900 dark:text-white">{trade.pair}</div>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-gray-700 dark:text-gray-300">
                          {formatCurrency(trade.open_rate)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-gray-700 dark:text-gray-300">
                          {formatCurrency(trade.current_rate)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            trade.profit_ratio >= 0
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          }`}>
                            {formatPercentage(trade.profit_ratio)}
                          </span>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-gray-700 dark:text-gray-300">
                          {formatCurrency(trade.stop_loss_abs)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="ml-1">
                              <div className="text-sm font-medium text-gray-900 dark:text-white">
                                {trade.strategy}
                              </div>
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                Tag: {trade.enter_tag}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {formatDate(trade.open_date)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="p-6 text-center text-gray-500 dark:text-gray-400">
                No active trades at the moment
              </div>
            )}
          </div>

          {/* Trading Status Section */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Trading Status</h2>
            </div>

            {tradingStatus ? (
              <div className="p-4">
                <div className="mb-4">
                  <h3 className="text-md font-medium text-gray-700 dark:text-gray-300 mb-2">Current Strategy</h3>
                  {tradingStatus.strategies && tradingStatus.strategies.length > 0 ? (
                    <div className="mb-4">
                      <select
                        value={selectedStrategy}
                        onChange={(e) => setSelectedStrategy(e.target.value)}
                        className="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 rounded-md shadow-sm text-gray-900 dark:text-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        disabled={tradingStatus.running}
                      >
                        {tradingStatus.strategies.map((strategy: string) => (
                          <option key={strategy} value={strategy}>
                            {strategy}
                          </option>
                        ))}
                      </select>
                      {tradingStatus.running && (
                        <p className="mt-1 text-sm text-yellow-600 dark:text-yellow-400">
                          Stop trading to change strategy
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400">No strategies available</p>
                  )}
                </div>

                <div className="mb-4">
                  <h3 className="text-md font-medium text-gray-700 dark:text-gray-300 mb-2">Trading Configuration</h3>
                  
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 mb-2">
                    <p className="text-sm text-gray-500 dark:text-gray-400">Max Open Trades</p>
                    <p className="text-lg font-medium text-gray-900 dark:text-white">{tradingStatus.max_open_trades}</p>
                  </div>
                  
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 mb-2">
                    <p className="text-sm text-gray-500 dark:text-gray-400">Stake Amount</p>
                    <p className="text-lg font-medium text-gray-900 dark:text-white">
                      {formatCurrency(tradingStatus.stake_amount)}
                    </p>
                  </div>
                  
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 mb-2">
                    <p className="text-sm text-gray-500 dark:text-gray-400">Timeframe</p>
                    <p className="text-lg font-medium text-gray-900 dark:text-white">{tradingStatus.timeframe}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-6 text-center text-gray-500 dark:text-gray-400">
                No trading status available
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TradingOperationsDashboard;
