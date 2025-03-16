'use client'

import { Grid, Card, Metric, Text, Title, DonutChart } from '@tremor/react'
import { useEffect, useState } from 'react'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorDisplay from '@/components/ErrorDisplay'
import { formatDistance } from 'date-fns'

interface SystemStatus {
  status: string
  version: string
  uptime: string
  dryRun: boolean
  tradingMode: string
  gpuUtilization: number
  memoryUsage: number
  systemHealth: {
    freqtrade: boolean
    database: boolean
    models: boolean
    quantum: boolean
  }
  logs: Array<{
    timestamp: string
    level: string
    message: string
  }>
}

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

export default function Dashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      setError(null)
      const [statusRes, metricsRes] = await Promise.all([
        fetch('/api/v1/system/status'),
        fetch('/api/v1/performance')
      ])
      
      if (!statusRes.ok || !metricsRes.ok) {
        throw new Error('Failed to fetch data')
      }

      const [statusData, metricsData] = await Promise.all([
        statusRes.json(),
        metricsRes.json()
      ])

      setSystemStatus(statusData)
      setPerformanceMetrics(metricsData)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err)
      setError('Failed to load dashboard data')
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="p-4">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4">
        <ErrorDisplay message={error} onRetry={fetchData} />
      </div>
    )
  }

  if (!systemStatus || !performanceMetrics) {
    return (
      <div className="p-4">
        <ErrorDisplay message="No data available" onRetry={fetchData} />
      </div>
    )
  }

  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Title>AlgoTradePro5 Dashboard</Title>
      <Text>Real-time trading performance and system metrics</Text>

      {/* System Status */}
      <Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-4 mt-6">
        <Card>
          <Text>System Status</Text>
          <Metric color={systemStatus.status === 'running' ? 'green' : 'red'}>
            {systemStatus.status}
          </Metric>
          <Text>Version: {systemStatus.version}</Text>
        </Card>
        <Card>
          <Text>Trading Mode</Text>
          <Metric>{systemStatus.tradingMode}</Metric>
          <Text>{systemStatus.dryRun ? 'Dry Run' : 'Live Trading'}</Text>
        </Card>
        <Card>
          <Text>Uptime</Text>
          <Metric>{systemStatus.uptime}</Metric>
        </Card>
        <Card>
          <Text>System Health</Text>
          <DonutChart
            data={[
              { name: 'FreqTrade', value: systemStatus.systemHealth.freqtrade ? 100 : 0 },
              { name: 'Database', value: systemStatus.systemHealth.database ? 100 : 0 },
              { name: 'Models', value: systemStatus.systemHealth.models ? 100 : 0 },
              { name: 'Quantum', value: systemStatus.systemHealth.quantum ? 100 : 0 }
            ]}
            valueFormatter={(value) => `${value}%`}
            showLabel={false}
            className="mt-2"
          />
        </Card>
      </Grid>

      {/* Trading Performance */}
      <Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-4 mt-6">
        <Card>
          <Text>Win Rate</Text>
          <Metric>{performanceMetrics.tradingMetrics.winRate}%</Metric>
        </Card>
        <Card>
          <Text>Total Profit/Loss</Text>
          <Metric>
            £{performanceMetrics.tradingMetrics.profitLoss.toFixed(2)}
          </Metric>
        </Card>
        <Card>
          <Text>Total Trades</Text>
          <Metric>{performanceMetrics.tradingMetrics.totalTrades}</Metric>
          <Text>{performanceMetrics.tradingMetrics.successfulTrades} successful</Text>
        </Card>
        <Card>
          <Text>Average Profit</Text>
          <Metric>
            £{performanceMetrics.tradingMetrics.averageProfit.toFixed(2)}
          </Metric>
          <Text>Drawdown: {performanceMetrics.tradingMetrics.drawdown}%</Text>
        </Card>
      </Grid>

      {/* System Metrics */}
      <div className="mt-6">
        <Card>
          <Title>System Performance</Title>
          <Grid numItems={1} numItemsSm={2} numItemsLg={2} className="gap-4 mt-4">
            <div>
              <Text>GPU Utilization</Text>
              <Metric>{systemStatus.gpuUtilization}%</Metric>
            </div>
            <div>
              <Text>Memory Usage</Text>
              <Metric>{systemStatus.memoryUsage} GB</Metric>
            </div>
            <div>
              <Text>Model Accuracy</Text>
              <Metric>{performanceMetrics.systemMetrics.modelAccuracy}%</Metric>
            </div>
            <div>
              <Text>Prediction Confidence</Text>
              <Metric>
                {performanceMetrics.systemMetrics.predictionConfidence}%
              </Metric>
            </div>
          </Grid>
        </Card>
      </div>

      {/* Recent Trades */}
      <div className="mt-6">
        <Card>
          <Title>Recent Trades</Title>
          <div className="mt-4">
            {performanceMetrics.recentTrades.map((trade) => (
              <div
                key={trade.id}
                className="border-b border-tremor-border dark:border-dark-tremor-border p-4"
              >
                <Grid numItems={3}>
                  <div>
                    <Text>{trade.pair}</Text>
                    <Text color={trade.type === 'LONG' ? 'green' : 'red'}>
                      {trade.type}
                    </Text>
                  </div>
                  <div>
                    <Text>Entry: £{trade.entryPrice.toFixed(2)}</Text>
                    <Text>Exit: £{trade.exitPrice.toFixed(2)}</Text>
                  </div>
                  <div>
                    <Text color={trade.profit > 0 ? 'green' : 'red'}>
                      {trade.profit > 0 ? '+' : ''}£{trade.profit.toFixed(2)}
                    </Text>
                    <Text>
                      {formatDistance(new Date(trade.timestamp), new Date(), { 
                        addSuffix: true 
                      })}
                    </Text>
                  </div>
                </Grid>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </main>
  )
}