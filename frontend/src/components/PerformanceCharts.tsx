'use client'

import { Card, Title, Grid } from "@tremor/react"
import { AreaChart, BarChart, DonutChart } from "@tremor/react"
import { useSelector } from 'react-redux'
import { RootState } from "@/lib/store"

interface StrategyStats {
  name: string
  trades: number
  profit: number
  winRate: number
  wins: number
}

interface DailyProfit {
  date: string
  profit: number
}

interface PairProfit {
  name: string
  value: number
}

export default function PerformanceCharts() {
  const { trades, totalProfit, winRate } = useSelector((state: RootState) => state.trading)

  // Calculate daily profit data
  const dailyProfits = trades.reduce<Record<string, DailyProfit>>((acc, trade) => {
    const date = new Date(trade.timestamp).toLocaleDateString()
    if (!acc[date]) {
      acc[date] = { date, profit: 0 }
    }
    acc[date].profit += trade.profit ?? 0
    return acc
  }, {})

  const profitChartData = Object.values(dailyProfits)

  // Calculate strategy performance
  const strategyPerformance = trades.reduce<Record<string, StrategyStats>>((acc, trade) => {
    if (!acc[trade.strategy]) {
      acc[trade.strategy] = { 
        name: trade.strategy,
        trades: 0,
        profit: 0,
        winRate: 0,
        wins: 0 
      }
    }
    acc[trade.strategy].trades++
    acc[trade.strategy].profit += trade.profit ?? 0
    if (trade.profit && trade.profit > 0) acc[trade.strategy].wins++
    acc[trade.strategy].winRate = (acc[trade.strategy].wins / acc[trade.strategy].trades) * 100
    return acc
  }, {})

  const strategyChartData = Object.values(strategyPerformance)

  // Calculate profit distribution by pair
  const pairDistribution = trades.reduce<Record<string, PairProfit>>((acc, trade) => {
    if (!acc[trade.pair]) {
      acc[trade.pair] = { name: trade.pair, value: 0 }
    }
    acc[trade.pair].value += trade.profit ?? 0
    return acc
  }, {})

  const pairChartData = Object.values(pairDistribution)

  return (
    <div className="space-y-6">
      <Card>
        <Title>Profit History</Title>
        <AreaChart
          className="h-72 mt-4"
          data={profitChartData}
          index="date"
          categories={["profit"]}
          colors={["emerald"]}
          valueFormatter={(number: number) => `£${number.toFixed(2)}`}
        />
      </Card>

      <Grid numItems={1} numItemsLg={2} className="gap-6">
        <Card>
          <Title>Strategy Performance</Title>
          <BarChart
            className="h-72 mt-4"
            data={strategyChartData}
            index="name"
            categories={["profit", "winRate"]}
            colors={["emerald", "blue"]}
            valueFormatter={(number: number) => 
              number >= 1 ? `£${number.toFixed(2)}` : `${number.toFixed(1)}%`
            }
          />
        </Card>

        <Card>
          <Title>Profit Distribution by Pair</Title>
          <DonutChart
            className="h-72 mt-4"
            data={pairChartData}
            category="value"
            index="name"
            valueFormatter={(number: number) => `£${number.toFixed(2)}`}
            colors={["slate", "violet", "indigo", "rose", "cyan", "amber"]}
          />
        </Card>
      </Grid>
    </div>
  )
}