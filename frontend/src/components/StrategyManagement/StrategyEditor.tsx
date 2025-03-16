import React, { useState } from 'react';
import { Strategy, StrategyConfig } from '@/types';

interface StrategyEditorProps {
    onSave: (config: StrategyConfig) => void;
    isUpdating: boolean;
}

export const StrategyEditor: React.FC<StrategyEditorProps> = ({ onSave, isUpdating }) => {
    const [config, setConfig] = useState<StrategyConfig>({
        maxOpenTrades: 3,
        stakeAmount: 10,
        minRoi: { "0": 0.05 },
        stopLoss: -0.02,
        trailingStop: true,
        trailingStopPositive: 0.01
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSave(config);
    };

    return (
        <div className="bg-white rounded-lg shadow p-6" data-testid="strategy-editor">
            <h2 className="text-xl font-semibold mb-4">Strategy Configuration</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block mb-1">Max Open Trades</label>
                    <input
                        type="number"
                        value={config.maxOpenTrades}
                        onChange={(e) => setConfig({...config, maxOpenTrades: parseInt(e.target.value)})}
                        className="w-full border rounded p-2"
                        data-testid="max-trades-input"
                    />
                </div>
                <div>
                    <label className="block mb-1">Stake Amount (£)</label>
                    <input
                        type="number"
                        value={config.stakeAmount}
                        onChange={(e) => setConfig({...config, stakeAmount: parseFloat(e.target.value)})}
                        className="w-full border rounded p-2"
                        max={10}
                        step={0.1}
                        data-testid="stake-input"
                    />
                </div>
                <div>
                    <label className="block mb-1">Stop Loss (%)</label>
                    <input
                        type="number"
                        value={config.stopLoss * -100}
                        onChange={(e) => setConfig({...config, stopLoss: parseFloat(e.target.value) / -100})}
                        className="w-full border rounded p-2"
                        min={0.1}
                        max={10}
                        step={0.1}
                        data-testid="stoploss-input"
                    />
                </div>
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        checked={config.trailingStop}
                        onChange={(e) => setConfig({...config, trailingStop: e.target.checked})}
                        className="mr-2"
                        data-testid="trailing-stop-checkbox"
                    />
                    <label>Enable Trailing Stop</label>
                </div>
                {config.trailingStop && (
                    <div>
                        <label className="block mb-1">Trailing Stop Positive (%)</label>
                        <input
                            type="number"
                            value={config.trailingStopPositive * 100}
                            onChange={(e) => setConfig({...config, trailingStopPositive: parseFloat(e.target.value) / 100})}
                            className="w-full border rounded p-2"
                            min={0.1}
                            max={5}
                            step={0.1}
                            data-testid="trailing-stop-positive-input"
                        />
                    </div>
                )}
                <button
                    type="submit"
                    className={`w-full py-2 px-4 rounded text-white ${
                        isUpdating ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'
                    }`}
                    disabled={isUpdating}
                    data-testid="save-button"
                >
                    {isUpdating ? 'Updating...' : 'Save Changes'}
                </button>
            </form>
        </div>
    );
};