import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Alert,
  Snackbar,
  useTheme
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import QuantumControlPanel from '../../components/QuantumControlPanel';

const QuantumControl = () => {
  const theme = useTheme();
  const dispatch = useDispatch();
  const [error, setError] = useState<string | null>(null);
  
  // We'll use the trading state when available
  const tradingState = useSelector((state: RootState) => state.trading);

  useEffect(() => {
    // Set up polling for metrics
    const interval = setInterval(() => {
      // We'll implement fetchQuantumMetrics when we have the quantum slice
      // dispatch(fetchQuantumMetrics());
    }, 5000);

    return () => clearInterval(interval);
  }, [dispatch]);

  return (
    <Box sx={{ py: 3 }}>
      <Typography
        variant="h4"
        gutterBottom
        sx={{
          color: theme.palette.primary.main,
          mb: 3,
          fontWeight: 'bold'
        }}
      >
        Quantum Control Center
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <QuantumControlPanel />
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              background: `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${theme.palette.background.default} 90%)`,
              boxShadow: theme.shadows[10]
            }}
          >
            <Typography variant="h6" gutterBottom color="primary">
              Hardware Status
            </Typography>
            {/* Add hardware monitoring components here */}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              background: `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${theme.palette.background.default} 90%)`,
              boxShadow: theme.shadows[10]
            }}
          >
            <Typography variant="h6" gutterBottom color="primary">
              Execution Queue
            </Typography>
            {/* Add quantum circuit queue management here */}
          </Paper>
        </Grid>
      </Grid>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default QuantumControl;
