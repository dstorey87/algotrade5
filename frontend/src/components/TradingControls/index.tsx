import { Button, Grid, Paper, Typography, Chip, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { startTrading, stopTrading, emergencyStop } from '@/store/slices/tradingSlice';

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
}));

const StatusChip = styled(Chip)(({ theme }) => ({
  margin: theme.spacing(0.5),
}));

const TradingControls = () => {
  const dispatch = useDispatch();
  const {
    balance,
    totalProfit,
    winRate,
    activeTrades,
    tradingEnabled,
    systemStatus
  } = useSelector((state: RootState) => state.trading);

  const handleStartTrading = () => {
    dispatch(startTrading());
  };

  const handleStopTrading = () => {
    dispatch(stopTrading());
  };

  const handleEmergencyStop = () => {
    dispatch(emergencyStop());
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Trading Controls
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6" gutterBottom>Account Status</Typography>
          <Typography>Balance: £{balance.total.toFixed(2)}</Typography>
          <Typography>Available: £{balance.free.toFixed(2)}</Typography>
          <Typography>Total Profit: £{totalProfit.toFixed(2)}</Typography>
          <Typography>Win Rate: {(winRate * 100).toFixed(2)}%</Typography>
          <Typography>Active Trades: {activeTrades}</Typography>
        </Item>
      </Grid>

      <Grid item xs={12} md={6}>
        <Item>
          <Typography variant="h6" gutterBottom>System Status</Typography>
          <Box sx={{ mb: 2 }}>
            <StatusChip
              label={`FreqTrade: ${systemStatus?.freqtrade ? 'Online' : 'Offline'}`}
              color={systemStatus?.freqtrade ? 'success' : 'error'}
              variant="outlined"
            />
            <StatusChip
              label={`Database: ${systemStatus?.database ? 'Connected' : 'Disconnected'}`}
              color={systemStatus?.database ? 'success' : 'error'}
              variant="outlined"
            />
            <StatusChip
              label={`Models: ${systemStatus?.models ? 'Loaded' : 'Not Loaded'}`}
              color={systemStatus?.models ? 'success' : 'error'}
              variant="outlined"
            />
            <StatusChip
              label={`Quantum: ${systemStatus?.quantum ? 'Ready' : 'Not Ready'}`}
              color={systemStatus?.quantum ? 'success' : 'error'}
              variant="outlined"
            />
          </Box>

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="success"
              onClick={handleStartTrading}
              disabled={tradingEnabled}
              fullWidth
            >
              Start Trading
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={handleStopTrading}
              disabled={!tradingEnabled}
              fullWidth
            >
              Stop Trading
            </Button>
          </Box>
          <Button
            variant="contained"
            color="warning"
            onClick={handleEmergencyStop}
            fullWidth
            sx={{ mt: 2 }}
          >
            Emergency Stop
          </Button>
        </Item>
      </Grid>
    </Grid>
  );
};

export default TradingControls;
