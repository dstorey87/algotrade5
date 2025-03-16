'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'
import { Card, Text, Title } from '@tremor/react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      error,
      errorInfo
    })
    
    // Log error to error tracking system
    console.error('Error:', error)
    console.error('Error Info:', errorInfo)
  }

  private handleRetry = () => {
    this.setState({ 
      hasError: false,
      error: null,
      errorInfo: null
    })
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="p-4">
          <Card>
            <Title>Something went wrong</Title>
            <Text>{this.state.error?.message}</Text>
            <button
              onClick={this.handleRetry}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Try Again
            </button>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}