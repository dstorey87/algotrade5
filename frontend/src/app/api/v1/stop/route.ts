import { NextResponse } from 'next/server'

export async function POST() {
  try {
    // TODO: Replace with actual FreqTrade API call
    // const response = await fetch('http://localhost:8080/api/v1/stop', {
    //   method: 'POST'
    // })
    // const data = await response.json()

    return NextResponse.json({
      status: 'success',
      message: 'Trading stopped successfully',
      tradingEnabled: false
    })
  } catch (error: any) {
    console.error('Error stopping trading:', error)
    return NextResponse.json(
      { error: 'Failed to stop trading' },
      { status: 500 }
    )
  }
}
