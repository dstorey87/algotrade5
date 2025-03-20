import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';

const Strategies = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Trading Strategies
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 300,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Active Strategies
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Currently active trading strategies and their performance
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 300,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Strategy Development
            </Typography>
            <Typography variant="body2" color="text.secondary">
              New strategies under development and testing
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              height: 400,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Performance Metrics
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Detailed performance metrics for all strategies
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Strategies;