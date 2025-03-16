'use client'

import { Title, Text, Card, Grid, Metric, ProgressBar } from "@tremor/react"
import { useSelector } from 'react-redux'
import { RootState } from "@/lib/store"

export default function TradingOverview() {
  const {
    activeStrategy,
    drawdown,
    confidence,
    patternValidation,
    quantumValidation,
    tradesToday,
    winStreak,
    modelPerformance
  } = useSelector((state: RootState) => state.trading)

  return (
    <div className="space-y-4">
      <Title>Trading Overview</Title>

      <Grid numItems={2} className="gap-4">
        <Card>
          <Text>Active Strategy</Text>
          <Metric>{activeStrategy || 'None'}</Metric>
        </Card>

        <Card>
          <Text>Trades Today</Text>
          <Metric>{tradesToday}</Metric>
        </Card>
      </Grid>

      <Card>
        <Text>AI Confidence</Text>
        <Metric>{(confidence * 100).toFixed(1)}%</Metric>
        <ProgressBar
          value={confidence * 100}
          color={confidence > 0.85 ? "green" : confidence > 0.7 ? "yellow" : "red"}
          className="mt-2"
        />
      </Card>

      <Grid numItems={2} className="gap-4">
        <Card>
          <Text>Pattern Validation</Text>
          <Metric className={patternValidation ? "text-green-500" : "text-red-500"}>
            {patternValidation ? 'Valid' : 'Invalid'}
          </Metric>
        </Card>

        <Card>
          <Text>Quantum Validation</Text>
          <Metric className={quantumValidation ? "text-green-500" : "text-red-500"}>
            {quantumValidation ? 'Confirmed' : 'Pending'}
          </Metric>
        </Card>
      </Grid>

      <Grid numItems={2} className="gap-4">
        <Card>
          <Text>Win Streak</Text>
          <Metric>{winStreak}</Metric>
        </Card>

        <Card>
          <Text>Max Drawdown</Text>
          <Metric className="text-red-500">
            {(drawdown * 100).toFixed(2)}%
          </Metric>
        </Card>
      </Grid>

      <Card>
        <Text>Model Performance</Text>
        <Metric>{(modelPerformance * 100).toFixed(1)}%</Metric>
        <ProgressBar
          value={modelPerformance * 100}
          color={modelPerformance > 0.85 ? "green" : modelPerformance > 0.7 ? "yellow" : "red"}
          className="mt-2"
        />
      </Card>
    </div>
  )
}
