'use client'

import { useEffect, useState } from 'react'
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
  Flex,
  Icon,
  Button
} from "@tremor/react"
import { useSelector } from 'react-redux'
import { RootState } from "@/lib/store"
import { formatDistanceToNow } from 'date-fns'
import { ArrowPathIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/outline'

export default function ActiveTrades() {
  const { activeTradesList, realTimeEnabled, lastUpdated } = useSelector((state: RootState) => state.trading)
  const [sortField, setSortField] = useState<string | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  // Handle sorting
  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  // Sort trades based on selected field and direction
  const sortedTrades = [...activeTradesList].sort((a, b) => {
    if (!sortField) return 0
    
    const aValue = a[sortField as keyof typeof a]
    const bValue = b[sortField as keyof typeof b]
    
    if (aValue === undefined || bValue === undefined) return 0
    
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

  // Format time from timestamp
  const formatTimeAgo = (timestamp: string) => {
    if (!timestamp) return 'Unknown'
    return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
  }

  // Get appropriate color based on profit value
  const getProfitColor = (value: number | undefined) => {
    if (value === undefined) return 'gray'
    if (value > 0) return 'emerald'
    if (value < 0) return 'red'
    return 'gray'
  }

  return (
    <Card>
      <div className="flex justify-between items-center mb-4">
        <Flex alignItems="center">
          <Text>Active Trades ({activeTradesList.length})</Text>
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

      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('pair')}
            >
              Pair {sortField === 'pair' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('entryPrice')}
            >
              Entry Price {sortField === 'entryPrice' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell>Amount</TableHeaderCell>
            <TableHeaderCell>Current Price</TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('unrealizedProfit')}
            >
              Unrealized P/L {sortField === 'unrealizedProfit' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell>Strategy</TableHeaderCell>
            <TableHeaderCell 
              className="cursor-pointer" 
              onClick={() => handleSort('confidence')}
            >
              Confidence {sortField === 'confidence' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeaderCell>
            <TableHeaderCell>Time Open</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {activeTradesList.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} className="text-center">
                <Text>No active trades</Text>
              </TableCell>
            </TableRow>
          ) : (
            sortedTrades.map((trade) => (
              <TableRow key={trade.id}>
                <TableCell>{trade.pair}</TableCell>
                <TableCell>£{trade.entryPrice.toFixed(6)}</TableCell>
                <TableCell>{trade.amount.toFixed(6)}</TableCell>
                <TableCell className="relative">
                  £{(trade.currentPrice || 0).toFixed(6)}
                  {trade.currentPrice !== undefined && trade.currentPrice > trade.entryPrice && (
                    <Icon icon={ArrowTrendingUpIcon} color="emerald" className="ml-1 h-4 w-4 inline" />
                  )}
                  {trade.currentPrice !== undefined && trade.currentPrice < trade.entryPrice && (
                    <Icon icon={ArrowTrendingDownIcon} color="red" className="ml-1 h-4 w-4 inline" />
                  )}
                </TableCell>
                <TableCell>
                  <Text color={getProfitColor(trade.unrealizedProfit)}>
                    £{(trade.unrealizedProfit || 0).toFixed(2)}
                    <span className="text-xs ml-1">
                      ({(trade.unrealizedProfitPercentage || 0).toFixed(2)}%)
                    </span>
                  </Text>
                </TableCell>
                <TableCell>{trade.strategy}</TableCell>
                <TableCell>
                  <Badge
                    color={
                      trade.confidence > 0.85 ? "emerald" :
                      trade.confidence > 0.7 ? "amber" : "rose"
                    }
                  >
                    {(trade.confidence * 100).toFixed(0)}%
                  </Badge>
                </TableCell>
                <TableCell>
                  {trade.open_date ? formatTimeAgo(trade.open_date) : 'Unknown'}
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </Card>
  )
}
