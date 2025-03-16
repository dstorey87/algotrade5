'use client'

import { Card, Text, Button } from '@tremor/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface ErrorDisplayProps {
  message: string
  onRetry?: () => void
}

export default function ErrorDisplay({ message, onRetry }: ErrorDisplayProps) {
  return (
    <Card className="bg-red-50 dark:bg-red-900/20">
      <div className="flex items-center space-x-3">
        <ExclamationTriangleIcon className="h-6 w-6 text-red-500" />
        <Text color="red">{message}</Text>
      </div>
      {onRetry && (
        <Button
          size="xs"
          variant="secondary"
          className="mt-3"
          onClick={onRetry}
        >
          Retry
        </Button>
      )}
    </Card>
  )
}