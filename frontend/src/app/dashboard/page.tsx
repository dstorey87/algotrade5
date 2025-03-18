'use client'

import { Card, Grid, Title, Text, Tab, TabList, TabGroup, TabPanel, TabPanels, Callout, Badge, Flex } from "@tremor/react"
import { useSelector } from "react-redux"
import { RootState } from "@/lib/store"
import { useRealTimeUpdates } from "@/hooks/useRealTimeUpdates"
import TradingControls from "@/components/TradingControls"
import TradingOverview from "@/components/TradingOverview"
import ActiveTrades from "@/components/ActiveTrades"
import TradeHistory from "@/components/TradeHistory"
import PerformanceCharts from "@/components/PerformanceCharts"
import LoadingOverlay from "@/components/LoadingOverlay"
import ConnectionToggle from "@/components/ConnectionToggle"
import SystemHealth from "@/components/SystemHealth"
import WebSocketTester from "@/components/WebSocketTester"
import ErrorBoundary from "@/components/ErrorBoundary"
import { ExclamationCircleIcon } from '@heroicons/react/24/solid'
import { formatDistance } from 'date-fns'

export default function DashboardPage() {
  const { 
    balance, 
    totalProfit, 
    winRate, 
    isLoading, 
    error, 
    lastUpdated,
    realTimeEnabled
  } = useSelector((state: RootState) => state.trading)

  // Use our real-time updates hook
  useRealTimeUpdates({
    enableWebSocket: true,
    pollingInterval: 5000
  })

  // Format the last updated time
  const lastUpdatedText = lastUpdated 
    ? formatDistance(new Date(lastUpdated), new Date(), { addSuffix: true })
    : 'Never';

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <Title>Trading Dashboard</Title>
        <Flex alignItems="center" className="gap-2">
          <SystemHealth compact />
          <Text className="text-xs text-tremor-content-subtle ml-2">
            Last updated: {lastUpdatedText}
          </Text>
          <ConnectionToggle />
        </Flex>
      </div>

      {error && (
        <Callout
          className="mb-6"
          title="Error"
          color="rose"
          icon={ExclamationCircleIcon}
        >
          {error}
        </Callout>
      )}

      <LoadingOverlay loading={isLoading}>
        <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-6 mb-6">
          <ErrorBoundary componentName="Balance Card">
            <Card>
              <Title>Balance</Title>
              <Text>£{balance.total.toFixed(2)}</Text>
              <Text className="text-sm text-tremor-content-subtle">
                Free: £{balance.free.toFixed(2)} / Used: £{balance.used.toFixed(2)}
              </Text>
            </Card>
          </ErrorBoundary>
          
          <ErrorBoundary componentName="Profit Card">
            <Card>
              <Title>Total Profit</Title>
              <Text className={totalProfit >= 0 ? "text-emerald-500" : "text-red-500"}>
                £{totalProfit.toFixed(2)}
              </Text>
              <Text className="text-sm text-tremor-content-subtle">
                Target: £1,000.00
              </Text>
            </Card>
          </ErrorBoundary>
          
          <ErrorBoundary componentName="Win Rate Card">
            <Card>
              <Title>Win Rate</Title>
              <Text>{(winRate * 100).toFixed(1)}%</Text>
              <Text className="text-sm text-tremor-content-subtle">
                Target: 85%
              </Text>
            </Card>
          </ErrorBoundary>
        </Grid>

        <Grid numItems={1} numItemsLg={2} className="gap-6">
          <ErrorBoundary componentName="Trading Controls">
            <Card>
              <TradingControls />
            </Card>
          </ErrorBoundary>
          
          <ErrorBoundary componentName="Trading Overview">
            <Card>
              <TradingOverview />
            </Card>
          </ErrorBoundary>
        </Grid>

        <ErrorBoundary componentName="Trade Data Tabs">
          <Card className="mt-6">
            <TabGroup>
              <TabList>
                <Tab>Active Trades</Tab>
                <Tab>Trade History</Tab>
                <Tab>Performance</Tab>
                <Tab>System Health</Tab>
              </TabList>
              <TabPanels>
                <TabPanel>
                  <ErrorBoundary componentName="Active Trades">
                    <ActiveTrades />
                  </ErrorBoundary>
                </TabPanel>
                <TabPanel>
                  <ErrorBoundary componentName="Trade History">
                    <TradeHistory />
                  </ErrorBoundary>
                </TabPanel>
                <TabPanel>
                  <ErrorBoundary componentName="Performance Charts">
                    <PerformanceCharts />
                  </ErrorBoundary>
                </TabPanel>
                <TabPanel>
                  <div className="space-y-6">
                    <ErrorBoundary componentName="System Health">
                      <SystemHealth />
                    </ErrorBoundary>
                    <ErrorBoundary componentName="WebSocket Tester">
                      <WebSocketTester />
                    </ErrorBoundary>
                  </div>
                </TabPanel>
              </TabPanels>
            </TabGroup>
          </Card>
        </ErrorBoundary>
      </LoadingOverlay>
    </div>
  )
}
