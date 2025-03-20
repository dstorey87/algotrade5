'use client'

import {
  Card,
  Table,
  TableHead,
  TableHeaderCell,
  TableBody,
  TableRow,
  TableCell,
  Badge,
  Text,
  DateRangePicker,
  DateRangePickerValue,
  Select,
  SelectItem,
  Flex,
  Divider,
  Title
} from "@tremor/react"
import { useState } from "react"
import { useSelector } from "react-redux"
import { RootState } from "@/lib/store"
import { formatDistanceToNow, format } from 'date-fns'

export default function TradeHistory() {
  const { tradeHistory, realTimeEnabled, lastUpdated } = useSelector((state: RootState) => state.trading)
  const [dateRange, setDateRange] = useState<DateRangePickerValue>({ from: undefined, to: undefined })
  const [selectedStrategy, setSelectedStrategy] = useState<string>("all")
  const [sortField, setSortField] = useState<string>("close_date")
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  // Extract unique strategies from trade history
  const strategies = Array.from(new Set(tradeHistory.map(trade => trade.strategy)))

  // Handle sorting
  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  // Apply filters and sort
  const filteredTrades = tradeHistory
    .filter(trade => {
      // Strategy filter
      if (selectedStrategy !== "all" && trade.strategy !== selectedStrategy) {
        return false
      }

      // Date range filter
      if (trade.close_date) {
        const tradeCloseDate = new Date(trade.close_date)
        if (dateRange.from && tradeCloseDate < dateRange.from) {
          return false
        }
        if (dateRange.to && tradeCloseDate > dateRange.to) {
          return false
        }
      }

      return true
    })
    .sort((a, b) => {
      if (!sortField) return 0
      
      const aValue = a[sortField as keyof typeof a]
      const bValue = b[sortField as keyof typeof b]
      
      if (aValue === undefined || bValue === undefined) return 0
      
      // Handle date values
      if (sortField === 'close_date' || sortField === 'open_date') {
        const aDate = aValue ? new Date(aValue as string).getTime() : 0
        const bDate = bValue ? new Date(bValue as string).getTime() : 0
        return sortDirection === 'asc' ? aDate - bDate : bDate - aDate
      }
      
      // Handle numeric values
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue
      }
      
      // Handle string values
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortDirection === 'asc' 
          ? aValue.localeCompare(bValue) 
          : bValue.localeCompare(aValue)
      }
      
      return 0
    })

  // Calculate trade history summary
  const totalTrades = filteredTrades.length
  const winningTrades = filteredTrades.filter(trade => trade.profit && trade.profit > 0).length
  const losingTrades = filteredTrades.filter(trade => trade.profit && trade.profit < 0).length
  const winRate = totalTrades > 0 ? (winningTrades / totalTrades) * 100 : 0
  const totalProfit = filteredTrades.reduce((sum, trade) => sum + (trade.profit || 0), 0)
  
  // Format time ago from timestamp
  const formatTimeAgo = (timestamp: string) => {
    if (!timestamp) return 'Unknown'
    return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
  }

  // Format date/time
  const formatDateTime = (timestamp: string) => {
    if (!timestamp) return 'Unknown'
    return format(new Date(timestamp), 'MMM d, yyyy HH:mm:ss')
  }

  return (
    <Card>
      <div className="flex justify-between items-center mb-4">
        <Flex alignItems="center">
          <Text>Trade History ({tradeHistory.length})</Text>
          {realTimeEnabled && (
            <Badge color="emerald" size="xs" className="ml-2">
              Live
            </Badge>
          )}
        </Flex>
        <Badge color="gray" size="xs">
          {lastUpdated ? `Updated ${formatDistanceToNow(new Date(lastUpdated), { addSuffix: true })}` : 'Not updated'}
        </Badge>
      </div>

      <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
        <div className="flex gap-4">
          <Select
            value={selectedStrategy}
            onValueChange={setSelectedStrategy}
            placeholder="Select Strategy"
            className="w-48"
          >
            <SelectItem value="all">All Strategies</SelectItem>
            {strategies.map(strategy => (
              <SelectItem key={strategy} value={strategy}>
                {strategy}
              </SelectItem>
            ))}
          </Select>
          
          <DateRangePicker
            value={dateRange}
            onValueChange={setDateRange}
            placeholder="Select Date Range"
            className="w-72"
          />
        </div>
      </div>

      {filteredTrades.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card decoration="top" decorationColor="blue">
            <Text>Total Trades</Text>
            <Title>{totalTrades}</Title>
          </Card>
          <Card decoration="top" decorationColor="emerald">
            <Text>Win Rate</Text>
            <Title>{winRate.toFixed(1)}%</Title>
            <Text className="text-xs text-tremor-content-subtle">
              {winningTrades} won / {losingTrades} lost
            </Text>
          </Card>
          <Card decoration="top" decorationColor={totalProfit >= 0 ? "emerald" : "rose"}>
            <Text>Total Profit</Text>
            <Title className={totalProfit >= 0 ? "text-emerald-500" : "text-rose-500"}>
              £{totalProfit.toFixed(2)}
            </Title>
          </Card>
          <Card decoration="top" decorationColor="amber">
            <Text>Avg. Profit per Trade</Text>
            <Title>
              £{(totalTrades > 0 ? totalProfit / totalTrades : 0).toFixed(2)}
            </Title>
          </Card>
        </div>
      )}

      <Divider />

      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('close_date')}
            >
              Close Date {sortField === 'close_date' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('open_date')}
            >
              Open Date {sortField === 'open_date' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('pair')}
            >
              Pair {sortField === 'pair' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell>Entry/Exit</TableHeaderCell>
            <TableHeaderCell>Amount</TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('profit')}
            >
              P/L {sortField === 'profit' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('strategy')}
            >
              Strategy {sortField === 'strategy' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filteredTrades.length === 0 ? (
            <TableRow>
              <TableCell colSpan={10} className="text-center">
                No trades found
              </TableCell>
            </TableRow>
          ) : (
            filteredTrades.map((trade) => (
              <TableRow key={trade.id}>
                <TableCell>
                  <Text>{formatDateTime(trade.close_date || '')}</Text>
                  <Text className="text-xs text-tremor-content-subtle">
                    {formatTimeAgo(trade.close_date || '')}
                  </Text>
                </TableCell>
                <TableCell>
                  <Text>{formatDateTime(trade.open_date || '')}</Text>
                  <Text className="text-xs text-tremor-content-subtle">
                    {formatTimeAgo(trade.open_date || '')}
                  </Text>
                </TableCell>
                <TableCell>{trade.pair}</TableCell>
                <TableCell>
                  <div className="flex flex-col">
                    <Text>Entry: £{trade.entryPrice.toFixed(4)}</Text>
                    <Text>Exit: £{(trade.exitPrice || 0).toFixed(4)}</Text>
                  </div>
                </TableCell>
                <TableCell>{trade.amount.toFixed(6)}</TableCell>
                <TableCell>
                  <Text color={trade.profit !== undefined && trade.profit >= 0 ? "emerald" : "rose"}>
                    £{(trade.profit || 0).toFixed(2)}
                    <span className="text-xs ml-1">
                      ({(trade.profitPercentage || 0).toFixed(2)}%)
                    </span>
                  </Text>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Text>{trade.strategy}</Text>
                    <Badge
                      color={
                        trade.confidence > 0.85 ? "emerald" :
                        trade.confidence > 0.7 ? "amber" : "rose"
                      }
                      size="xs"
                    >
                      {(trade.confidence * 100).toFixed(0)}%
                    </Badge>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </Card>
  )
}
