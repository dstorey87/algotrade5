'use client'

import { ThemeProvider } from '@mui/material'
import CssBaseline from '@mui/material/CssBaseline'
import { ReactNode } from 'react'
import ErrorBoundary from '@/components/ErrorBoundary'
import theme from '@/theme'

export function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ErrorBoundary>
  )
}
