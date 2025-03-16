'use client'

import { Card } from "@tremor/react"

interface LoadingOverlayProps {
  loading: boolean
  children: React.ReactNode
}

export default function LoadingOverlay({ loading, children }: LoadingOverlayProps) {
  if (!loading) return <>{children}</>

  return (
    <div className="relative">
      <div className="opacity-50 pointer-events-none">
        {children}
      </div>
      <div className="absolute inset-0 flex items-center justify-center bg-white/50 dark:bg-black/50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    </div>
  )
}