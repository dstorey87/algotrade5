'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'
import { Card, Title, Text, Button } from '@tremor/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
  componentName?: string
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
      errorInfo: null
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.setState({
      errorInfo
    })

    // Call the optional onError callback
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }

    // Log the error to console for debugging
    console.error('Component Error:', error, errorInfo)
  }

  render(): ReactNode {
    const { hasError, error } = this.state
    const { children, fallback, componentName } = this.props

    if (hasError) {
      // If a custom fallback is provided, use it
      if (fallback) {
        return fallback
      }

      // Otherwise show our default error UI
      return (
        <Card decoration="top" decorationColor="rose">
          <div className="flex items-center mb-4">
            <ExclamationTriangleIcon className="h-8 w-8 text-rose-500 mr-2" />
            <Title>Component Error</Title>
          </div>
          <Text className="mb-2">
            {componentName 
              ? `The ${componentName} component has encountered an error.` 
              : 'A component has encountered an error.'
            }
          </Text>
          <Text className="text-tremor-content-subtle text-sm mb-4">
            {error?.message || 'Unknown error occurred'}
          </Text>
          <Button 
            size="xs"
            color="rose"
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
          >
            Try Again
          </Button>
        </Card>
      )
    }

    return children
  }
}

export default ErrorBoundary