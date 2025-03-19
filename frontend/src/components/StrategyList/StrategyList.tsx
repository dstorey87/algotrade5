import React, { useEffect, useState } from 'react';
import { Card, Title, Text } from '@tremor/react';
import { Grid } from '@tremor/react';
import { Tooltip } from '../shared';
import { strategyApi } from '../../services/strategyApi';

interface StrategyPerformance {
  totalProfit: number;
  winRate: number;
  tradeCount: number;
}

interface Strategy {
  name: string;
  description: string;
  performance: StrategyPerformance;
}

interface ApiStrategy {
  name: string;
  description: string;
}

export const StrategyList: React.FC = () => {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStrategies = async () => {
      try {
        const availableStrategies = await strategyApi.listAvailableStrategies() as ApiStrategy[];
        const strategiesWithPerformance = await Promise.all(
          availableStrategies.map(async (strategy) => {
            const performance = await strategyApi.getStrategyPerformance(strategy.name) as StrategyPerformance;
            return { ...strategy, performance };
          })
        );
        setStrategies(strategiesWithPerformance);
      } catch (error) {
        console.error('Failed to fetch strategies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStrategies();
  }, []);

  if (loading) {
    return <div>Loading strategies...</div>;
  }

  return (
    <Grid className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {strategies.map((strategy) => (
        <Tooltip key={strategy.name} content={strategy.description}>
          <Card>
            <Title>{strategy.name}</Title>
            <Text>Win Rate: {strategy.performance.winRate}%</Text>
            <Text>Total Profit: {strategy.performance.totalProfit} USDT</Text>
            <Text>Total Trades: {strategy.performance.tradeCount}</Text>
          </Card>
        </Tooltip>
      ))}
    </Grid>
  );
};