'use client'

import { Card } from '@tremor/react'

export default function LoadingSpinner() {
  return (
    <Card className="h-full w-full flex items-center justify-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </Card>
  )
}