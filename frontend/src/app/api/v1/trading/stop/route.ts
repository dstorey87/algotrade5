import { NextResponse } from 'next/server'

export async function POST() {
  try {
    // In production, this would call FreqTrade's API to stop trading
    return NextResponse.json({
      success: true,
      message: 'Trading stopped successfully'
    })
  } catch (error: any) {
    console.error('Error stopping trading:', error)
    return NextResponse.json(
      { error: 'Failed to stop trading' },
      { status: 500 }
    )
  }
}
