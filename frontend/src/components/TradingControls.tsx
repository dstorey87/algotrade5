'use client'

import { useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { AppDispatch, RootState } from "@/lib/store"
import { Button, Title, Text, Badge } from "@tremor/react"
import { startTrading, stopTrading } from "@/store/slices/tradingSlice"

export default function TradingControls() {
  const dispatch = useDispatch<AppDispatch>()
  const { tradingEnabled, systemStatus } = useSelector((state: RootState) => state.trading)

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <Title>Trading Controls</Title>
        <Badge color={tradingEnabled ? "green" : "red"}>
          {tradingEnabled ? "Active" : "Inactive"}
        </Badge>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Button
          size="lg"
          color="green"
          onClick={() => dispatch(startTrading())}
          disabled={tradingEnabled}
        >
          Start Trading
        </Button>
        <Button
          size="lg"
          color="red"
          onClick={() => dispatch(stopTrading())}
          disabled={!tradingEnabled}
        >
          Stop Trading
        </Button>
      </div>

      <Button
        size="lg"
        color="amber"
        className="w-full"
        onClick={() => dispatch(stopTrading())}
      >
        Emergency Stop
      </Button>

      <div className="space-y-2 mt-4">
        <Text>System Status</Text>
        <div className="flex flex-wrap gap-2">
          <Badge color={systemStatus?.freqtrade ? "green" : "red"}>
            FreqTrade: {systemStatus?.freqtrade ? "Online" : "Offline"}
          </Badge>
          <Badge color={systemStatus?.database ? "green" : "red"}>
            Database: {systemStatus?.database ? "Connected" : "Disconnected"}
          </Badge>
          <Badge color={systemStatus?.models ? "green" : "red"}>
            Models: {systemStatus?.models ? "Loaded" : "Not Loaded"}
          </Badge>
          <Badge color={systemStatus?.quantum ? "green" : "red"}>
            Quantum: {systemStatus?.quantum ? "Ready" : "Not Ready"}
          </Badge>
        </div>
      </div>
    </div>
  )
}
