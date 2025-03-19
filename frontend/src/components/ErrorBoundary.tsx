'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'
import { Card, Title, Text, Button } from '@tremor/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  componentName?: string
}

interface State {
  hasError: boolean
  error?: Error
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <Card decoration="top" decorationColor="rose">
          <div className="flex items-center mb-4">
            <ExclamationTriangleIcon className="h-8 w-8 text-rose-500 mr-2" />
            <Title>{this.props.componentName || 'Component'} Error</Title>
          </div>
          <Text className="mb-2">
            A component has encountered an error.
          </Text>
          <Text className="text-tremor-content-subtle text-sm mb-4">
            {this.state.error?.message || 'Unknown error occurred'}
          </Text>
          <Button 
            size="xs"
            color="rose"
            onClick={() => this.setState({ hasError: false, error: undefined })}
          >
            Try Again
          </Button>
        </Card>
      )
    }

    return this.props.children
  }
}