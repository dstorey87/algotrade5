import { Metadata } from 'next'
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter'
import { WebSocketErrorBoundary } from '@/components/ErrorBoundary/WebSocketErrorBoundary'
import { Chart as ChartJS } from 'chart.js'

// Configure global chart styles for dark theme
ChartJS.defaults.color = 'rgba(255, 255, 255, 0.87)'
ChartJS.defaults.borderColor = 'rgba(255, 255, 255, 0.1)'

export const metadata: Metadata = {
  title: 'AlgoTradePro5',
  description: 'AI-driven cryptocurrency trading system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider>
          <WebSocketErrorBoundary>
            {children}
          </WebSocketErrorBoundary>
        </AppRouterCacheProvider>
      </body>
    </html>
  )
}