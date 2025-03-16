import { NextResponse } from 'next/server'
import { ErrorManager } from '../../../../lib/ErrorManager'

const errorManager = new ErrorManager()

export async function POST(request: Request) {
  try {
    const errorData = await request.json()

    // Log error with appropriate severity based on error type
    errorManager.logError({
      message: errorData.error,
      stack: errorData.errorInfo,
      url: errorData.url,
      timestamp: errorData.timestamp,
      severity: 'HIGH',
      category: 'FRONTEND'
    })

    return NextResponse.json({
      status: 'success',
      message: 'Error logged successfully'
    })
  } catch (error: any) {
    console.error('Error logging frontend error:', error)
    return NextResponse.json(
      { error: 'Failed to log error' },
      { status: 500 }
    )
  }
}
