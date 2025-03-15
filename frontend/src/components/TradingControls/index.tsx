import { Button, Grid, Paper, Typography } from '@mui/material'
import { styled } from '@mui/material/styles'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../store'
import { updateBalance, updateTotalProfit, updateWinRate, updateActiveTrades } from '../../store/slices/tradingSlice'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
}))

const TradingControls = () => {
  const dispatch = useDispatch()
  const { balance, totalProfit, winRate, activeTrades } = useSelector((state: RootState) => state.trading)

  const handleStartTrading = () => {
    // In a real implementation, this would connect to the trading system
    console.log('Starting trading...')
  }

  const handleStopTrading = () => {
    // In a real implementation, this would stop the trading system
    console.log('Stopping trading...')
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Trading Controls
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">Account Status</Typography>
          <Typography>Balance: £{balance.toFixed(2)}</Typography>
          <Typography>Total Profit: £{totalProfit.toFixed(2)}</Typography>
          <Typography>Win Rate: {(winRate * 100).toFixed(2)}%</Typography>
          <Typography>Active Trades: {activeTrades}</Typography>
        </Item>
      </Grid>

      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6">Controls</Typography>
          <Button 
            variant="contained" 
            color="success" 
            onClick={handleStartTrading}
            sx={{ marginRight: 2 }}
          >
            Start Trading
          </Button>
          <Button 
            variant="contained" 
            color="error" 
            onClick={handleStopTrading}
          >
            Stop Trading
          </Button>
        </Item>
      </Grid>
    </Grid>
  )
}

export default TradingControls