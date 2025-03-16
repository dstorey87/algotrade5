'use client'

import { useEffect } from 'react'
import {
  Card,
  Table,
  TableHead,
  TableHeaderCell,
  TableBody,
  TableRow,
  TableCell,
  Badge,
  Text
} from "@tremor/react"
import { useSelector, useDispatch } from 'react-redux'
import { RootState, AppDispatch } from "@/lib/store"
import { updateCurrentPrices } from "@/lib/slices/tradingSlice"

export default function ActiveTrades() {
  const dispatch = useDispatch<AppDispatch>()
  const { trades } = useSelector((state: RootState) => state.trading)
  const activeTrades = trades.filter(trade => !trade.exitPrice)

  useEffect(() => {
    // Set up WebSocket connection for real-time price updates
    const ws = new WebSocket('ws://localhost:8080/ws/prices')
    
    ws.onmessage = (event) => {
      const prices = JSON.parse(event.data)
      dispatch(updateCurrentPrices(prices))
    }

    return () => {
      ws.close()
    }
  }, [dispatch])

  return (
    <Card>
      <div className="flex justify-between items-center mb-4">
        <Text>Active Trades ({activeTrades.length})</Text>
      </div>

      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell>Pair</TableHeaderCell>
            <TableHeaderCell>Entry Price</TableHeaderCell>
            <TableHeaderCell>Amount</TableHeaderCell>
            <TableHeaderCell>Current Price</TableHeaderCell>
            <TableHeaderCell>Unrealized P/L</TableHeaderCell>
            <TableHeaderCell>Strategy</TableHeaderCell>
            <TableHeaderCell>Confidence</TableHeaderCell>
            <TableHeaderCell>Status</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {activeTrades.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} className="text-center">
                No active trades
              </TableCell>
            </TableRow>
          ) : (
            activeTrades.map((trade) => (
              <TableRow key={trade.id}>
                <TableCell>{trade.pair}</TableCell>
                <TableCell>£{trade.entryPrice.toFixed(2)}</TableCell>
                <TableCell>{trade.amount}</TableCell>
                <TableCell>£{trade.currentPrice?.toFixed(2) || '-'}</TableCell>
                <TableCell>
                  <Text color={trade.unrealizedProfit >= 0 ? "green" : "red"}>
                    £{trade.unrealizedProfit?.toFixed(2) || '-'} 
                    ({trade.unrealizedProfitPercentage?.toFixed(2) || '-'}%)
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