import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Mock data - would fetch from FreqTrade API in production
    return NextResponse.json({
      tradingEnabled: true,
      balance: {
        total: 10.50,
        free: 8.20,
        used: 2.30
      },
      currentTrade: {
        pair: 'BTC/USDT',
        side: 'buy',
        amount: 0.0001,
        entryPrice: 52000,
        currentPrice: 52100,
        profitLoss: 0.10
      },
      openPositions: [
        {
          pair: 'BTC/USDT',
          side: 'buy',
          amount: 0.0001,
          entryPrice: 52000,
          currentPrice: 52100,
          profitLoss: 0.10
        }
      ],
      tradeHistory: [
        {
          pair: 'ETH/USDT',
          side: 'sell',
          amount: 0.01,
          entryPrice: 2800,
          exitPrice: 2850,
          profitLoss: 0.50,
          timestamp: new Date().toISOString()
        }
      ]
    })
  } catch (error: any) {
    console.error('Error fetching trading status:', error)
    return NextResponse.json(
      { error: 'Failed to fetch trading status' },
      { status: 500 }
    )
  }
}
