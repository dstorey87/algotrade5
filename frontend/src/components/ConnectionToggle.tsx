'use client'

import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '@/lib/store'
import { Button } from '@tremor/react'
import { BoltIcon, ArrowPathIcon } from '@heroicons/react/24/outline'
import { setRealTimeEnabled } from '@/store/slices/tradingSlice'
import websocketService from '@/services/websocket'
// Use MUI Tooltip instead since we're already using MUI components elsewhere
import { Tooltip } from '@mui/material'

interface ConnectionToggleProps {
  className?: string
}

export default function ConnectionToggle({ className = '' }: ConnectionToggleProps) {
  const dispatch = useDispatch<AppDispatch>()
  const { realTimeEnabled } = useSelector((state: RootState) => state.trading)
  const [isConnecting, setIsConnecting] = useState(false)

  const handleToggle = () => {
    if (realTimeEnabled) {
      // Disconnect WebSocket
      websocketService.disconnect()
      dispatch(setRealTimeEnabled(false))
    } else {
      // Try to connect WebSocket
      setIsConnecting(true)
      
      try {
        websocketService.connect(dispatch)
        
        // Check connection after a short delay
        setTimeout(() => {
          const connected = websocketService.isConnected()
          dispatch(setRealTimeEnabled(connected))
          setIsConnecting(false)
        }, 1500)
      } catch (error) {
        console.error('Failed to connect:', error)
        dispatch(setRealTimeEnabled(false))
        setIsConnecting(false)
      }
    }
  }

  return (
    <Tooltip title={realTimeEnabled ? 'Switch to polling updates' : 'Switch to real-time updates'}>
      <Button
        className={className}
        color={realTimeEnabled ? 'emerald' : 'blue'}
        variant="secondary"
        icon={realTimeEnabled ? BoltIcon : ArrowPathIcon}
        disabled={isConnecting}
        onClick={handleToggle}
        size="xs"
      >
        {isConnecting ? 'Connecting...' : (realTimeEnabled ? 'Real-time' : 'Polling')}
      </Button>
    </Tooltip>
  )
}