'use client'

import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { ReactNode } from 'react'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import theme from '@/theme'

export function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <div className="dark">
          {children}
        </div>
      </ErrorBoundary>
    </ThemeProvider>
  )
}