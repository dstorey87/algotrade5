"""
Test WebSocket component for AlgoTradePro5 frontend integration.

This component provides real-time market data updates to the trading dashboard.
"""

import React, { useEffect, useState } from 'react'
import { useDispatch } from 'react-redux'
import io from 'socket.io-client'

class WebSocketService {
    constructor(url) {
        this.url = url
        this.socket = null
        this.reconnectAttempts = 0
        this.maxReconnectAttempts = 5
        this.reconnectInterval = 1000 // Start with 1 second
    }

    connect() {
        this.socket = io(this.url, {
            reconnection: false, // We'll handle reconnection manually
            transports: ['websocket'],
            timeout: 10000
        })

        this.socket.on('connect', () => {
            console.log('WebSocket connected')
            this.reconnectAttempts = 0
            this.reconnectInterval = 1000
        })

        this.socket.on('disconnect', () => {
            console.log('WebSocket disconnected')
            this.attemptReconnect()
        })

        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error)
            this.attemptReconnect()
        })

        return this.socket
    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect()
            this.socket = null
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Maximum reconnection attempts reached')
            return
        }

        setTimeout(() => {
            console.log(`Attempting to reconnect (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`)
            this.reconnectAttempts++
            this.connect()
            // Exponential backoff
            this.reconnectInterval = Math.min(this.reconnectInterval * 2, 30000)
        }, this.reconnectInterval)
    }

    subscribe(channel, callback) {
        if (!this.socket) {
            throw new Error('WebSocket not connected')
        }
        this.socket.on(channel, callback)
    }

    unsubscribe(channel, callback) {
        if (!this.socket) {
            return
        }
        this.socket.off(channel, callback)
    }

    emit(event, data) {
        if (!this.socket) {
            throw new Error('WebSocket not connected')
        }
        this.socket.emit(event, data)
    }
}

export const useWebSocket = (url) => {
    const [socket, setSocket] = useState(null)
    const [isConnected, setIsConnected] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        const webSocketService = new WebSocketService(url)
        const socketInstance = webSocketService.connect()

        socketInstance.on('connect', () => {
            setIsConnected(true)
            setError(null)
        })

        socketInstance.on('disconnect', () => {
            setIsConnected(false)
        })

        socketInstance.on('error', (err) => {
            setError(err)
            setIsConnected(false)
        })

        setSocket(socketInstance)

        return () => {
            webSocketService.disconnect()
        }
    }, [url])

    const subscribe = (channel, callback) => {
        if (!socket) return
        socket.on(channel, callback)
    }

    const unsubscribe = (channel, callback) => {
        if (!socket) return
        socket.off(channel, callback)
    }

    const emit = (event, data) => {
        if (!socket) return
        socket.emit(event, data)
    }

    return {
        socket,
        isConnected,
        error,
        subscribe,
        unsubscribe,
        emit
    }
}

export const WebSocketProvider = ({ url, children }) => {
    const dispatch = useDispatch()
    const { isConnected, error, subscribe, unsubscribe } = useWebSocket(url)

    useEffect(() => {
        // Subscribe to market data updates
        const handleMarketUpdate = (data) => {
            dispatch({
                type: 'MARKET_DATA_UPDATE',
                payload: data
            })
        }

        // Subscribe to trade updates
        const handleTradeUpdate = (data) => {
            dispatch({
                type: 'TRADE_UPDATE',
                payload: data
            })
        }

        // Subscribe to system status updates
        const handleSystemUpdate = (data) => {
            dispatch({
                type: 'SYSTEM_STATUS_UPDATE',
                payload: data
            })
        }

        if (isConnected) {
            subscribe('market_update', handleMarketUpdate)
            subscribe('trade_update', handleTradeUpdate)
            subscribe('system_status', handleSystemUpdate)
        }

        return () => {
            if (isConnected) {
                unsubscribe('market_update', handleMarketUpdate)
                unsubscribe('trade_update', handleTradeUpdate)
                unsubscribe('system_status', handleSystemUpdate)
            }
        }
    }, [isConnected, subscribe, unsubscribe, dispatch])

    return (
        <div className="websocket-provider">
            {error && <div className="websocket-error">WebSocket Error: {error.message}</div>}
            {children}
        </div>
    )
}

export default WebSocketProvider