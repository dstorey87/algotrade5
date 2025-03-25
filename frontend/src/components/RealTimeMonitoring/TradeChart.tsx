import React, { useMemo } from 'react';
import { Box } from '@mui/material';
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
  TimeScale,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Trade } from '@/types/trade';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

interface TradeChartProps {
  trades: Trade[];
}

export const TradeChart: React.FC<TradeChartProps> = ({ trades }) => {
  const chartData = useMemo(() => {
    const sortedTrades = [...trades].sort((a, b) => a.timestamp - b.timestamp);
    let runningPL = 0;

    const data = sortedTrades.map(trade => {
      if (trade.profitLoss !== undefined) {
        runningPL += trade.profitLoss;
      }
      return {
        x: trade.timestamp,
        y: runningPL
      };
    });

    return {
      datasets: [
        {
          label: 'Cumulative P/L',
          data,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
          pointRadius: 0,
          borderWidth: 2,
        },
      ],
    };
  }, [trades]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    scales: {
      x: {
        type: 'time' as const,
        time: {
          unit: 'minute' as const,
        },
        grid: {
          display: false,
        },
      },
      y: {
        title: {
          display: true,
          text: 'Profit/Loss (£)',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            return `P/L: £${context.parsed.y.toFixed(2)}`;
          },
        },
      },
    },
  };

  return (
    <Box sx={{ height: '100%', width: '100%' }}>
      <Line options={options} data={chartData} />
    </Box>
  );
};