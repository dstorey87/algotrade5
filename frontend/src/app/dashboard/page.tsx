'use client'

import { Card, Grid, Title, Text, Tab, TabList, TabGroup, TabPanel, TabPanels, Callout } from "@tremor/react"
import { useSelector } from "react-redux"
import { RootState } from "@/lib/store"
import { useDataPolling } from "@/hooks/useDataPolling"
import TradingControls from "@/components/TradingControls"
import TradingOverview from "@/components/TradingOverview"
import ActiveTrades from "@/components/ActiveTrades"
import TradeHistory from "@/components/TradeHistory"
import PerformanceCharts from "@/components/PerformanceCharts"
import LoadingOverlay from "@/components/LoadingOverlay"
import { ExclamationCircleIcon } from '@heroicons/react/24/solid'

export default function DashboardPage() {
  const { balance, totalProfit, winRate, isLoading, error } = useSelector((state: RootState) => state.trading)
  
  useDataPolling(5000)

  return (
    <div className="p-6">
      <Title className="mb-6">Trading Dashboard</Title>
      
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
          <Card>
            <Title>Balance</Title>
            <Text>£{balance.total.toFixed(2)}</Text>
            <Text className="text-sm text-tremor-content-subtle">
              Free: £{balance.free.toFixed(2)} / Used: £{balance.used.toFixed(2)}
            </Text>
          </Card>
          <Card>
            <Title>Total Profit</Title>
            <Text className={totalProfit >= 0 ? "text-emerald-500" : "text-red-500"}>
              £{totalProfit.toFixed(2)}
            </Text>
            <Text className="text-sm text-tremor-content-subtle">
              Target: £1,000.00
            </Text>
          </Card>
          <Card>
            <Title>Win Rate</Title>
            <Text>{(winRate * 100).toFixed(1)}%</Text>
            <Text className="text-sm text-tremor-content-subtle">
              Target: 85%
            </Text>
          </Card>
        </Grid>

        <Grid numItems={1} numItemsLg={2} className="gap-6">
          <Card>
            <TradingControls />
          </Card>
          <Card>
            <TradingOverview />
          </Card>
        </Grid>

        <Card className="mt-6">
          <TabGroup>
            <TabList>
              <Tab>Active Trades</Tab>
              <Tab>Trade History</Tab>
              <Tab>Performance</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <ActiveTrades />
              </TabPanel>
              <TabPanel>
                <TradeHistory />
              </TabPanel>
              <TabPanel>
                <PerformanceCharts />
              </TabPanel>
            </TabPanels>
          </TabGroup>
        </Card>
      </LoadingOverlay>
    </div>
  )
}