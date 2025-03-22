// filepath: c:\AlgoTradPro5\frontend\src\components\TradingOperations\TradeMonitor.tsx
import React from 'react';

export const TradeMonitor: React.FC = () => {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4">Trade Monitor</h2>
      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">Current Status</p>
          <p className="font-medium">Active</p>
        </div>
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">Open Positions</p>
          <p className="font-medium">0</p>
        </div>
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">Last Trade</p>
          <p className="font-medium">N/A</p>
        </div>
      </div>
    </div>
  );
};