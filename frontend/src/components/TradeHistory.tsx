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
  Select,
  SelectItem,
} from "@tremor/react"
import { useState } from "react"
import { useSelector } from "react-redux"
import { RootState } from "@/lib/store"

export default function TradeHistory() {
  const { trades } = useSelector((state: RootState) => state.trading)
  const [dateRange, setDateRange] = useState<{ from: Date | null, to: Date | null }>({ from: null, to: null })
  const [selectedStrategy, setSelectedStrategy] = useState<string>("all")

  const strategies = Array.from(new Set(trades.map(trade => trade.strategy)))
  
  const filteredTrades = trades.filter(trade => {
    // Strategy filter
    if (selectedStrategy !== "all" && trade.strategy !== selectedStrategy) {
      return false
    }
    
    // Date range filter
    const tradeDate = new Date(trade.timestamp)
    if (dateRange.from && tradeDate < dateRange.from) {
      return false
    }
    if (dateRange.to && tradeDate > dateRange.to) {
      return false
    }
    
    return true
  })

  return (
    <Card>
      <div className="flex justify-between items-center mb-6">
        <Text>Trade History</Text>
        <div className="flex gap-4">
          <Select
            value={selectedStrategy}
            onValueChange={setSelectedStrategy}
            placeholder="Select Strategy"
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
          />
        </div>
      </div>

      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell>Date</TableHeaderCell>
            <TableHeaderCell>Pair</TableHeaderCell>
            <TableHeaderCell>Type</TableHeaderCell>
            <TableHeaderCell>Entry</TableHeaderCell>
            <TableHeaderCell>Exit</TableHeaderCell>
            <TableHeaderCell>Amount</TableHeaderCell>
            <TableHeaderCell>P/L</TableHeaderCell>
            <TableHeaderCell>Strategy</TableHeaderCell>
            <TableHeaderCell>Confidence</TableHeaderCell>
            <TableHeaderCell>Status</TableHeaderCell>
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
                  {new Date(trade.timestamp).toLocaleString()}
                </TableCell>
                <TableCell>{trade.pair}</TableCell>
                <TableCell>
                  <Badge color={trade.type === 'buy' ? 'green' : 'red'}>
                    {trade.type}
                  </Badge>
                </TableCell>
                <TableCell>£{trade.entryPrice.toFixed(2)}</TableCell>
                <TableCell>
                  {trade.exitPrice ? `£${trade.exitPrice.toFixed(2)}` : '-'}
                </TableCell>
                <TableCell>{trade.amount}</TableCell>
                <TableCell>
                  <Text color={trade.profit !== undefined && trade.profit >= 0 ? "green" : "red"}>
                    £{trade.profit?.toFixed(2) || '-'} 
                    ({trade.profitPercentage?.toFixed(2) || '-'}%)
                  </Text>
                </TableCell>
                <TableCell>{trade.strategy}</TableCell>
                <TableCell>
                  <Badge
                    color={
                      trade.confidence > 0.85 ? "green" : 
                      trade.confidence > 0.7 ? "yellow" : "red"
                    }
                  >
                    {(trade.confidence * 100).toFixed(0)}%
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge>
                    {trade.patternValidated && trade.quantumValidated ? 'Validated' : 'Pending'}
                  </Badge>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </Card>
  )
}