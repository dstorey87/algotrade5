import { Inter } from 'next/font/google'
import { Metadata } from 'next'
import { ClientProviders } from './providers-client'
import '@/styles/globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AlgoTradePro5',
  description: 'AI-Driven Trading System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`h-full antialiased ${inter.className}`}>
      <body className="h-full">
        <ClientProviders>
          {children}
        </ClientProviders>
      </body>
    </html>
  )
}
