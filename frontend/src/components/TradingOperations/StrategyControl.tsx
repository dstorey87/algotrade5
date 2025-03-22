// filepath: c:\AlgoTradPro5\frontend\src\components\TradingOperations\StrategyControl.tsx
import React from 'react';

interface StrategyControlProps {
  strategies?: Array<{ id: string; name: string; active: boolean }>;
}

export const StrategyControl: React.FC<StrategyControlProps> = ({ strategies = [] }) => {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4">Strategy Control</h2>
      {strategies.length === 0 ? (
        <p className="text-gray-500">No active strategies available</p>
      ) : (
        <ul className="space-y-2">
          {strategies.map((strategy) => (
            <li key={strategy.id} className="flex justify-between items-center">
              <span>{strategy.name}</span>
              <span className={strategy.active ? "text-green-500" : "text-red-500"}>
                {strategy.active ? "Active" : "Inactive"}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};