import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Mock data - in production this would fetch from FreqTrade's API
    return NextResponse.json({
      status: 'running',
      version: '0.1.0',
      uptime: '2h 15m',
      dryRun: true,
      tradingMode: 'spot',
      gpuUtilization: 65,
      memoryUsage: 4.2,
      systemHealth: {
        freqtrade: true,
        database: true,
        models: true,
        quantum: true
      },
      logs: [
        {
          timestamp: new Date().toISOString(),
          level: 'INFO',
          message: 'System running normally'
        }
      ]
    })
  } catch (error: any) {
    console.error('Error fetching system status:', error)
    return NextResponse.json(
      { error: 'Failed to fetch system status' },
      { status: 500 }
    )
  }
}