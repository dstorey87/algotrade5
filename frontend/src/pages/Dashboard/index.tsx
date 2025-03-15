import { Grid, Paper, Typography } from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
}))

const Dashboard = () => {
  const {
    gpuUtilization,
    memoryUsage,
    modelAccuracy,
    modelConfidence,
    quantumCircuitStatus,
    systemHealth
  } = useSelector((state: RootState) => state.system)

  return (
    <Grid container spacing={3}>
      {/* System Status */}
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          System Overview
        </Typography>
      </Grid>

      {/* Resource Usage */}
      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">Resource Usage</Typography>
          <Typography>GPU: {gpuUtilization.toFixed(2)}%</Typography>
          <Typography>Memory: {memoryUsage.toFixed(2)}%</Typography>
        </Item>
      </Grid>

      {/* Model Performance */}
      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">Model Performance</Typography>
          <Typography>Accuracy: {(modelAccuracy * 100).toFixed(2)}%</Typography>
          <Typography>Confidence: {(modelConfidence * 100).toFixed(2)}%</Typography>
        </Item>
      </Grid>

      {/* Quantum Circuit Status */}
      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">Quantum Circuit</Typography>
          <Typography>Status: {quantumCircuitStatus}</Typography>
        </Item>
      </Grid>

      {/* System Health */}
      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">System Health</Typography>
          <Typography>FreqTrade: {systemHealth.freqtrade ? 'Online' : 'Offline'}</Typography>
          <Typography>Database: {systemHealth.database ? 'Connected' : 'Disconnected'}</Typography>
          <Typography>Models: {systemHealth.models ? 'Loaded' : 'Not Loaded'}</Typography>
          <Typography>Quantum: {systemHealth.quantum ? 'Ready' : 'Not Ready'}</Typography>
        </Item>
      </Grid>

      {/* Trading Stats - Placeholder for future integration */}
      <Grid item xs={12}>
        <Item>
          <Typography variant="h6">Trading Statistics</Typography>
          <Typography>Current Balance: £0.00</Typography>
          <Typography>Total Profit: £0.00</Typography>
          <Typography>Win Rate: 0%</Typography>
          <Typography>Active Trades: 0</Typography>
        </Item>
      </Grid>
    </Grid>
  )
}

export default Dashboard