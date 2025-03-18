'use client'

import { Card, Title, Grid, Tab, TabGroup, TabList, Text, TabPanel, TabPanels, Flex, Badge, Select, SelectItem } from "@tremor/react"
import { AreaChart, BarChart, DonutChart, LineChart } from "@tremor/react"
import { useSelector } from 'react-redux'
import { RootState } from "@/lib/store"
import { useState } from 'react'
import { formatDistanceToNow } from 'date-fns'

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
  cumulativeProfit: number
}

interface PairProfit {
  name: string
  value: number
}

interface TimeframeOption {
  label: string
  value: string
  days: number
}

export default function PerformanceCharts() {
  const { tradeHistory, activeTradesList, realTimeEnabled, lastUpdated } = useSelector((state: RootState) => state.trading)
  const [timeframe, setTimeframe] = useState<string>("30d")
  
  const timeframeOptions: TimeframeOption[] = [
    { label: "Last 7 days", value: "7d", days: 7 },
    { label: "Last 30 days", value: "30d", days: 30 },
    { label: "Last 90 days", value: "90d", days: 90 },
    { label: "All time", value: "all", days: 9999 }
  ]
  
  const selectedTimeframe = timeframeOptions.find(option => option.value === timeframe)
  const cutoffDate = new Date()
  cutoffDate.setDate(cutoffDate.getDate() - (selectedTimeframe?.days || 30))
  
  // Filter trades based on selected timeframe
  const filteredTrades = tradeHistory.filter(trade => {
    if (timeframe === 'all') return true
    const tradeDate = new Date(trade.close_date || '')
    return tradeDate >= cutoffDate
  })
  
  // Process trades to extract timestamps and convert to Date objects
  const tradesWithDates = filteredTrades.map(trade => ({
    ...trade,
    closeDate: trade.close_date ? new Date(trade.close_date) : null,
    openDate: trade.open_date ? new Date(trade.open_date) : null
  }))
  
  // Sort trades by close date
  const sortedTrades = tradesWithDates
    .filter(trade => trade.closeDate) // Only include trades with valid close dates
    .sort((a, b) => a.closeDate!.getTime() - b.closeDate!.getTime())
  
  // Calculate daily profit data with cumulative profits
  let cumulativeProfit = 0
  const dailyProfits: Record<string, DailyProfit> = {}
  
  sortedTrades.forEach(trade => {
    if (!trade.closeDate) return
    
    const dateStr = trade.closeDate.toISOString().split('T')[0]
    if (!dailyProfits[dateStr]) {
      dailyProfits[dateStr] = { 
        date: dateStr, 
        profit: 0,
        cumulativeProfit: 0 
      }
    }
    
    dailyProfits[dateStr].profit += trade.profit || 0
  })
  
  // Calculate cumulative profits
  const profitChartData = Object.keys(dailyProfits)
    .sort()
    .map(date => {
      cumulativeProfit += dailyProfits[date].profit
      return {
        date,
        profit: dailyProfits[date].profit,
        cumulativeProfit
      }
    })
  
  // Fill in missing dates to create a continuous chart
  const filledProfitChartData: DailyProfit[] = []
  if (profitChartData.length > 0) {
    const startDate = new Date(profitChartData[0].date)
    const endDate = new Date()
    let currentDate = new Date(startDate)
    let lastCumulative = 0
    
    while (currentDate <= endDate) {
      const dateStr = currentDate.toISOString().split('T')[0]
      const existingData = profitChartData.find(d => d.date === dateStr)
      
      if (existingData) {
        filledProfitChartData.push(existingData)
        lastCumulative = existingData.cumulativeProfit
      } else {
        filledProfitChartData.push({
          date: dateStr,
          profit: 0,
          cumulativeProfit: lastCumulative
        })
      }
      
      currentDate.setDate(currentDate.getDate() + 1)
    }
  }

  // Calculate strategy performance
  const strategyPerformance = filteredTrades.reduce<Record<string, StrategyStats>>((acc, trade) => {
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
    acc[trade.strategy].profit += trade.profit || 0
    if (trade.profit && trade.profit > 0) acc[trade.strategy].wins++
    acc[trade.strategy].winRate = acc[trade.strategy].trades > 0 
      ? (acc[trade.strategy].wins / acc[trade.strategy].trades) * 100 
      : 0
    return acc
  }, {})

  const strategyChartData = Object.values(strategyPerformance)
    .sort((a, b) => b.profit - a.profit) // Sort by profit

  // Calculate profit distribution by pair
  const pairDistribution = filteredTrades.reduce<Record<string, PairProfit>>((acc, trade) => {
    if (!acc[trade.pair]) {
      acc[trade.pair] = { name: trade.pair, value: 0 }
    }
    acc[trade.pair].value += trade.profit || 0
    return acc
  }, {})

  // Sort and limit pairs to top performers and group others
  const sortedPairs = Object.values(pairDistribution)
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
  
  const topPairs = sortedPairs.slice(0, 5)
  
  // Sum the profits of remaining pairs
  const otherPairsValue = sortedPairs.slice(5).reduce((sum, pair) => sum + pair.value, 0)
  
  // Add "Other" category if there are more than 5 pairs
  const pairChartData = sortedPairs.length > 5 
    ? [...topPairs, { name: 'Other Pairs', value: otherPairsValue }]
    : topPairs

  // Calculate win/loss ratio by day of week
  const dayOfWeekStats = filteredTrades.reduce<Record<string, { wins: number, losses: number, total: number }>>((acc, trade) => {
    if (!trade.close_date) return acc
    
    const date = new Date(trade.close_date)
    const dayOfWeek = date.toLocaleString('en-US', { weekday: 'long' })
    
    if (!acc[dayOfWeek]) {
      acc[dayOfWeek] = { wins: 0, losses: 0, total: 0 }
    }
    
    if (trade.profit && trade.profit > 0) {
      acc[dayOfWeek].wins++
    } else if (trade.profit && trade.profit < 0) {
      acc[dayOfWeek].losses++
    }
    
    acc[dayOfWeek].total++
    
    return acc
  }, {})
  
  // Calculate win rate percentages by day of week
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const dayOfWeekData = dayNames.map(day => {
    const stats = dayOfWeekStats[day] || { wins: 0, losses: 0, total: 0 }
    const winRate = stats.total > 0 ? (stats.wins / stats.total) * 100 : 0
    
    return {
      day,
      winRate: Math.round(winRate * 10) / 10,
      trades: stats.total
    }
  })

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
        <Flex alignItems="center">
          <Text>Performance Analysis</Text>
          {realTimeEnabled && (
            <Badge color="emerald" size="xs" className="ml-2">
              Live
            </Badge>
          )}
        </Flex>
        <Flex alignItems="center" className="gap-2">
          <Select
            value={timeframe}
            onValueChange={setTimeframe}
            className="w-40"
          >
            {timeframeOptions.map(option => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </Select>
          <Badge color="gray" size="xs">
            {lastUpdated ? `Updated ${formatDistanceToNow(new Date(lastUpdated), { addSuffix: true })}` : 'Not updated'}
          </Badge>
        </Flex>
      </div>

      <TabGroup>
        <TabList>
          <Tab>Profit & Loss</Tab>
          <Tab>Strategy Analysis</Tab>
          <Tab>Trading Patterns</Tab>
        </TabList>
        
        <TabPanels>
          <TabPanel>
            <div className="space-y-6 mt-4">
              <Card>
                <Title>Profit Over Time</Title>
                <LineChart
                  className="h-72 mt-4"
                  data={filledProfitChartData}
                  index="date"
                  categories={["cumulativeProfit"]}
                  colors={["emerald"]}
                  valueFormatter={(number: number) => `£${number.toFixed(2)}`}
                  showLegend={false}
                  showGridLines={false}
                  startEndOnly={true}
                  showXAxis={true}
                  showYAxis={true}
                  yAxisWidth={60}
                />
              </Card>
              
              <Card>
                <Title>Daily Profit/Loss</Title>
                <BarChart
                  className="h-72 mt-4"
                  data={filledProfitChartData}
                  index="date"
                  categories={["profit"]}
                  colors={["blue"]}
                  valueFormatter={(number: number) => `£${number.toFixed(2)}`}
                  showLegend={false}
                  showGridLines={false}
                  startEndOnly={true}
                  showXAxis={true}
                  showYAxis={true}
                  yAxisWidth={60}
                />
              </Card>
            </div>
          </TabPanel>
          
          <TabPanel>
            <div className="space-y-6 mt-4">
              <Grid numItems={1} numItemsLg={2} className="gap-6">
                <Card>
                  <Title>Strategy Profit</Title>
                  <BarChart
                    className="h-72 mt-4"
                    data={strategyChartData}
                    index="name"
                    categories={["profit"]}
                    colors={["indigo"]}
                    valueFormatter={(number: number) => `£${number.toFixed(2)}`}
                    showLegend={false}
                  />
                </Card>

                <Card>
                  <Title>Strategy Win Rate</Title>
                  <BarChart
                    className="h-72 mt-4"
                    data={strategyChartData}
                    index="name"
                    categories={["winRate"]}
                    colors={["amber"]}
                    valueFormatter={(number: number) => `${number.toFixed(1)}%`}
                    showLegend={false}
                  />
                </Card>
              </Grid>
              
              <Card>
                <Title>Profit Distribution by Trading Pair</Title>
                <DonutChart
                  className="h-72 mt-4"
                  data={pairChartData}
                  category="value"
                  index="name"
                  valueFormatter={(number: number) => `£${number.toFixed(2)}`}
                  colors={["slate", "violet", "indigo", "rose", "cyan", "amber"]}
                />
              </Card>
            </div>
          </TabPanel>
          
          <TabPanel>
            <div className="space-y-6 mt-4">
              <Card>
                <Title>Win Rate by Day of Week</Title>
                <BarChart
                  className="h-72 mt-4"
                  data={dayOfWeekData}
                  index="day"
                  categories={["winRate"]}
                  colors={["emerald"]}
                  valueFormatter={(number: number) => `${number.toFixed(1)}%`}
                  showLegend={false}
                />
              </Card>
              
              <Card>
                <Title>Number of Trades by Day of Week</Title>
                <BarChart
                  className="h-72 mt-4"
                  data={dayOfWeekData}
                  index="day"
                  categories={["trades"]}
                  colors={["blue"]}
                  showLegend={false}
                />
              </Card>
            </div>
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </div>
  )
}
