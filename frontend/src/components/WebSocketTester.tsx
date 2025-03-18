'use client'

import { useState, useEffect } from 'react'
import { Card, Text, Badge, Button, Callout } from '@tremor/react'
import { ArrowPathIcon, BoltIcon } from '@heroicons/react/24/outline'
import websocketService from '@/services/websocket'
import { useDispatch } from 'react-redux'
import { AppDispatch } from '@/lib/store'
import apiSettings from '@/config/api'

export default function WebSocketTester() {
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected')
  const [testResults, setTestResults] = useState<{success: boolean; message: string} | null>(null)
  const [isTestRunning, setIsTestRunning] = useState(false)
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    // Check initial connection status
    const isConnected = websocketService.isConnected()
    setConnectionStatus(isConnected ? 'connected' : 'disconnected')

    // Set up a periodic check of the connection status
    const statusCheck = setInterval(() => {
      const isConnected = websocketService.isConnected()
      setConnectionStatus(isConnected ? 'connected' : 'disconnected')
    }, 5000)

    return () => {
      clearInterval(statusCheck)
    }
  }, [])

  const handleConnect = () => {
    setConnectionStatus('connecting')
    try {
      websocketService.connect(dispatch)
      
      // Give it a moment to establish connection
      setTimeout(() => {
        const isConnected = websocketService.isConnected()
        setConnectionStatus(isConnected ? 'connected' : 'disconnected')
      }, 2000)
    } catch (error) {
      setConnectionStatus('disconnected')
      setTestResults({
        success: false,
        message: `Connection failed: ${error instanceof Error ? error.message : String(error)}`
      })
    }
  }

  const handleDisconnect = () => {
    websocketService.disconnect()
    setConnectionStatus('disconnected')
  }

  const runConnectivityTest = async () => {
    setIsTestRunning(true)
    setTestResults(null)
    
    try {
      // 1. Check if API is reachable
      const apiResponse = await fetch(apiSettings.apiUrl('ping'), {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        cache: 'no-store'
      })
      
      if (!apiResponse.ok) {
        setTestResults({
          success: false,
          message: `API check failed: ${apiResponse.status} ${apiResponse.statusText}`
        })
        setIsTestRunning(false)
        return
      }
      
      // 2. Check if WebSocket endpoints are available
      const wsCheckResponse = await fetch(apiSettings.apiUrl('ws/status'), {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        cache: 'no-store'
      })
      
      if (!wsCheckResponse.ok) {
        setTestResults({
          success: false,
          message: `WebSocket endpoint check failed: ${wsCheckResponse.status} ${wsCheckResponse.statusText}`
        })
        setIsTestRunning(false)
        return
      }
      
      // 3. Attempt to establish a WebSocket connection
      setConnectionStatus('connecting')
      
      // Disconnect first if already connected
      if (websocketService.isConnected()) {
        websocketService.disconnect()
      }
      
      websocketService.connect(dispatch)
      
      // Check connection after a delay
      setTimeout(() => {
        const isConnected = websocketService.isConnected()
        setConnectionStatus(isConnected ? 'connected' : 'disconnected')
        
        if (isConnected) {
          setTestResults({
            success: true,
            message: 'WebSocket connection test successful. Real-time updates should be working.'
          })
        } else {
          setTestResults({
            success: false,
            message: 'WebSocket connection test failed. Could not establish a connection.'
          })
        }
        
        setIsTestRunning(false)
      }, 3000)
      
    } catch (error) {
      setTestResults({
        success: false,
        message: `Test failed: ${error instanceof Error ? error.message : String(error)}`
      })
      setConnectionStatus('disconnected')
      setIsTestRunning(false)
    }
  }

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <Text>WebSocket Connection Tester</Text>
        <Badge 
          color={
            connectionStatus === 'connected' ? 'emerald' : 
            connectionStatus === 'connecting' ? 'amber' : 'rose'
          }
          icon={connectionStatus === 'connected' ? BoltIcon : undefined}
        >
          {connectionStatus === 'connected' ? 'Connected' : 
           connectionStatus === 'connecting' ? 'Connecting...' : 'Disconnected'}
        </Badge>
      </div>
      
      <div className="flex space-x-2 mb-4">
        <Button 
          size="xs" 
          disabled={connectionStatus === 'connecting' || connectionStatus === 'connected'} 
          onClick={handleConnect}
          loading={connectionStatus === 'connecting'}
        >
          Connect
        </Button>
        <Button 
          size="xs" 
          variant="secondary" 
          disabled={connectionStatus !== 'connected'} 
          onClick={handleDisconnect}
        >
          Disconnect
        </Button>
        <Button 
          size="xs" 
          icon={ArrowPathIcon} 
          variant="light" 
          color="gray" 
          disabled={isTestRunning} 
          onClick={runConnectivityTest}
          loading={isTestRunning}
        >
          Run Connectivity Test
        </Button>
      </div>
      
      {testResults && (
        <Callout
          title={testResults.success ? "Test Successful" : "Test Failed"}
          color={testResults.success ? "emerald" : "rose"}
          className="mt-2"
        >
          {testResults.message}
        </Callout>
      )}
      
      <Text className="text-xs text-tremor-content-subtle mt-4">
        Note: This tool helps diagnose connection issues with the real-time WebSocket updates.
        If you're having trouble with live data updates, run the connectivity test to check your connection.
      </Text>
    </Card>
  )
}