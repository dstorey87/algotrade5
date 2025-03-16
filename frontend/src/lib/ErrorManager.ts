export enum ErrorSeverity {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

export enum ErrorCategory {
  NETWORK = 'NETWORK',
  API = 'API',
  FRONTEND = 'FRONTEND',
  TRADING = 'TRADING',
  SYSTEM = 'SYSTEM'
}

interface ErrorLog {
  message: string
  stack?: string
  url?: string
  timestamp: string
  severity: keyof typeof ErrorSeverity
  category: keyof typeof ErrorCategory
}

export class ErrorManager {
  private static instance: ErrorManager
  private errorHistory: ErrorLog[] = []
  private readonly MAX_HISTORY = 100

  constructor() {
    if (ErrorManager.instance) {
      return ErrorManager.instance
    }
    ErrorManager.instance = this
  }

  public logError(error: ErrorLog) {
    // Add to history with rotation
    this.errorHistory.push(error)
    if (this.errorHistory.length > this.MAX_HISTORY) {
      this.errorHistory.shift()
    }

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[ErrorManager]', error)
    }

    // Send to error tracking service if in production
    if (process.env.NODE_ENV === 'production') {
      // Here we could integrate with services like Bugsnag, Sentry, etc.
      this.sendToErrorService(error)
    }
  }

  private async sendToErrorService(error: ErrorLog) {
    try {
      const response = await fetch('/api/v1/error', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(error)
      })

      if (!response.ok) {
        console.error('Failed to send error to tracking service:', await response.text())
      }
    } catch (e) {
      console.error('Error sending to tracking service:', e)
    }
  }

  public getErrorHistory(): ErrorLog[] {
    return [...this.errorHistory]
  }

  public clearHistory() {
    this.errorHistory = []
  }
}
