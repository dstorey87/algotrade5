import React from 'react';
import { useQuery } from '@tanstack/react-query';

interface Trade {
  pair: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  timestamp: string;
  status: 'open' | 'closed';
}

export const TradeMonitor: React.FC = () => {
  const { data: trades, isLoading, error } = useQuery({
    queryKey: ['trades'],
    queryFn: () => fetch('/api/trades/active').then(res => res.json()) as Promise<Trade[]>
  });

  if (isLoading) return <div>Loading trades...</div>;
  if (error) return <div>Error loading trades: {error.toString()}</div>;

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4">Active Trades</h2>
      <div className="space-y-4">
        {trades?.length === 0 ? (
          <p>No active trades</p>  
        ) : (
          trades?.map((trade, index) => (
            <div key={index} className="border-b pb-2">
              <div className="flex justify-between">
                <span className="font-medium">{trade.pair}</span>
                <span className={trade.type === 'buy' ? 'text-green-500' : 'text-red-500'}>
                  {trade.type.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Amount: {trade.amount}</span>
                <span>Price: {trade.price}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};