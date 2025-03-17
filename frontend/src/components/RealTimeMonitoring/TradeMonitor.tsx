import React, { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Trade, WSMessage } from '@/types';

interface TradeMonitorProps {
    wsEndpoint: string;
}

export const RealTimeTradeMonitor: React.FC<TradeMonitorProps> = ({ wsEndpoint }) => {
    const [trades, setTrades] = useState<Trade[]>([]);
    const { lastMessage, readyState } = useWebSocket(wsEndpoint);

    useEffect(() => {
        if (lastMessage) {
            const message: WSMessage = JSON.parse(lastMessage.data);
            if (message.type === 'trade_update') {
                setTrades(prevTrades => [message.data, ...prevTrades].slice(0, 50));
            }
        }
    }, [lastMessage]);

    return (
        <div className="bg-white rounded-lg shadow" data-testid="real-time-trade-monitor">
            <div className="p-4 border-b">
                <div className="flex items-center justify-between">
                    <h2 className="text-lg font-semibold">Live Trading Activity</h2>
                    <div className={`px-2 py-1 rounded text-sm ${
                        readyState === 1 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                        {readyState === 1 ? 'Connected' : 'Disconnected'}
                    </div>
                </div>
            </div>
            <div className="p-4">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Time</th>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Pair</th>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Type</th>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Price</th>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Amount</th>
                                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {trades.map((trade) => (
                                <tr key={trade.id} data-testid={`trade-row-${trade.id}`}>
                                    <td className="px-4 py-2 text-sm">
                                        {new Date(trade.timestamp).toLocaleTimeString()}
                                    </td>
                                    <td className="px-4 py-2 text-sm">{trade.pair}</td>
                                    <td className="px-4 py-2 text-sm">
                                        <span className={`px-2 py-1 rounded text-xs ${
                                            trade.type === 'buy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                        }`}>
                                            {trade.type.toUpperCase()}
                                        </span>
                                    </td>
                                    <td className="px-4 py-2 text-sm">£{trade.price.toFixed(2)}</td>
                                    <td className="px-4 py-2 text-sm">{trade.amount.toFixed(8)}</td>
                                    <td className="px-4 py-2 text-sm">
                                        <span className={`px-2 py-1 rounded text-xs ${
                                            trade.status === 'completed' ? 'bg-green-100 text-green-800' : 
                                            trade.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                                            'bg-red-100 text-red-800'
                                        }`}>
                                            {trade.status.toUpperCase()}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};