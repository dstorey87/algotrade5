import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Mock data - in production this would fetch from FreqTrade's API
    return NextResponse.json({
      tradingMetrics: {
        winRate: 85.5,
        profitLoss: 12.35,
        totalTrades: 45,
        successfulTrades: 38,
        averageProfit: 0.32,
        drawdown: -2.1
      },
      systemMetrics: {
        gpuUtilization: 65,
        memoryUsage: 4.2,
        modelAccuracy: 92.3,
        predictionConfidence: 87.6
      },
      recentTrades: [
        {
          id: 1,
          pair: 'BTC/USDT',
          type: 'LONG',
          entryPrice: 52100.50,
          exitPrice: 52300.75,
          profit: 0.38,
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          pair: 'ETH/USDT',
          type: 'SHORT',
          entryPrice: 2850.25,
          exitPrice: 2830.50,
          profit: 0.69,
          timestamp: new Date(Date.now() - 5 * 60000).toISOString()
        }
      ]
    })
  } catch (error: any) {
    console.error('Error fetching performance metrics:', error)
    return NextResponse.json(
      { error: 'Failed to fetch performance metrics' },
      { status: 500 }
    )
  }
}
