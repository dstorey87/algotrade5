import React, { useMemo } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import { Trade } from '@/types/trade';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface TradeChartProps {
  trades: Trade[];
}

export const TradeChart: React.FC<TradeChartProps> = ({ trades }) => {
  const chartData = useMemo(() => {
    const sortedTrades = [...trades].sort((a, b) => a.timestamp - b.timestamp);
    let runningPnL = 0;
    
    return {
      labels: sortedTrades.map(trade => new Date(trade.timestamp).toLocaleTimeString()),
      datasets: [
        {
          label: 'Cumulative P&L %',
          data: sortedTrades.map(trade => {
            if (trade.profitLoss) {
              runningPnL += trade.profitLoss;
            }
            return runningPnL;
          }),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
          fill: false,
        },
      ],
    };
  }, [trades]);

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          maxRotation: 45,
          minRotation: 45,
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
  };

  return (
    <div style={{ height: '400px', width: '100%' }}>
      <Line data={chartData} options={options} />
    </div>
  );
};