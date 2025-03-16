'use client'

import { useEffect, useState } from 'react'
import {
  Card,
  Metric,
  Text,
  Flex,
  Grid,
  Title,
  BarChart,
  Color,
  AreaChart,
} from '@tremor/react'
import { formatDistance } from 'date-fns'

interface PerformanceMetrics {
  tradingMetrics: {
    winRate: number
    profitLoss: number
    totalTrades: number
    successfulTrades: number
    averageProfit: number
    drawdown: number
  }
  systemMetrics: {
    gpuUtilization: number
    memoryUsage: number
    modelAccuracy: number
    predictionConfidence: number
  }
  recentTrades: Array<{
    id: number
    pair: string
    type: string
    entryPrice: number
    exitPrice: number
    profit: number
    timestamp: string
  }>
}

const valueFormatter = (number: number) => 
  `£${Intl.NumberFormat('en-GB').format(number).toString()}`

export default function PerformancePage() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/v1/performance')
      .then(res => res.json())
      .then(data => {
        setMetrics(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to fetch performance metrics:', err)
        setError('Failed to load performance metrics')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="p-4">
        <Text>Loading performance metrics...</Text>
      </div>
    )
  }

  if (error || !metrics) {
    return (
      <div className="p-4">
        <Text color="red">{error || 'Failed to load metrics'}</Text>
      </div>
    )
  }

  const { tradingMetrics, systemMetrics, recentTrades } = metrics

  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Title>Performance Dashboard</Title>
      <Text>Real-time trading performance and system metrics</Text>

      <Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-4 mt-6">
        <Card>
          <Text>Win Rate</Text>
          <Metric>{tradingMetrics.winRate}%</Metric>
        </Card>
        <Card>
          <Text>Total Profit/Loss</Text>
          <Metric>{valueFormatter(tradingMetrics.profitLoss)}</Metric>
        </Card>
        <Card>
          <Text>Successful Trades</Text>
          <Metric>{tradingMetrics.successfulTrades}/{tradingMetrics.totalTrades}</Metric>
        </Card>
        <Card>
          <Text>Average Profit</Text>
          <Metric>{valueFormatter(tradingMetrics.averageProfit)}</Metric>
        </Card>
      </Grid>

      <div className="mt-6">
        <Card>
          <Title>System Health</Title>
          <Grid numItems={1} numItemsSm={2} numItemsLg={2} className="gap-4">
            <div>
              <Text>GPU Utilization</Text>
              <Metric>{systemMetrics.gpuUtilization}%</Metric>
            </div>
            <div>
              <Text>Memory Usage</Text>
              <Metric>{systemMetrics.memoryUsage}GB</Metric>
            </div>
            <div>
              <Text>Model Accuracy</Text>
              <Metric>{systemMetrics.modelAccuracy}%</Metric>
            </div>
            <div>
              <Text>Prediction Confidence</Text>
              <Metric>{systemMetrics.predictionConfidence}%</Metric>
            </div>
          </Grid>
        </Card>
      </div>

      <div className="mt-6">
        <Card>
          <Title>Recent Trades</Title>
          <div className="mt-4">
            {recentTrades.map((trade) => (
              <div
                key={trade.id}
                className="border-b border-tremor-border dark:border-dark-tremor-border p-4"
              >
                <Flex>
                  <div>
                    <Text>{trade.pair}</Text>
                    <Text color={trade.type === 'LONG' ? 'green' : 'red'}>
                      {trade.type}
                    </Text>
                  </div>
                  <div className="text-right">
                    <Text>
                      Entry: {valueFormatter(trade.entryPrice)}
                    </Text>
                    <Text>
                      Exit: {valueFormatter(trade.exitPrice)}
                    </Text>
                  </div>
                  <div className="text-right">
                    <Text color={trade.profit > 0 ? 'green' : 'red'}>
                      {trade.profit > 0 ? '+' : ''}{valueFormatter(trade.profit)}
                    </Text>
                    <Text>
                      {formatDistance(new Date(trade.timestamp), new Date(), { addSuffix: true })}
                    </Text>
                  </div>
                </Flex>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </main>
  )
}