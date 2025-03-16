import React from 'react';
import { Box, Card, CardContent, Typography, LinearProgress, Grid, useTheme } from '@mui/material';
import { ResponsiveLine } from '@nivo/line';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';

const QuantumLoopVisualization = () => {
  const theme = useTheme();
  const quantum = useSelector((state: RootState) => state.trading.quantum);

  const mockTimeseriesData = [
    {
      id: 'quantum_confidence',
      data: [
        { x: '00:00', y: 0.82 },
        { x: '04:00', y: 0.87 },
        { x: '08:00', y: 0.91 },
        { x: '12:00', y: 0.85 },
        { x: '16:00', y: 0.88 },
        { x: '20:00', y: 0.92 }
      ]
    }
  ];

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Quantum Loop Status
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Current Confidence
              </Typography>
              <LinearProgress
                variant="determinate"
                value={quantum?.confidence * 100 || 0}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: theme.palette.grey[800],
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 4,
                    backgroundImage: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`
                  }
                }}
              />
              <Typography variant="h5" sx={{ mt: 1 }}>
                {(quantum?.confidence * 100 || 0).toFixed(1)}%
              </Typography>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Pattern Recognition
              </Typography>
              <Typography variant="body1">
                {quantum?.currentPattern || 'No active pattern'}
              </Typography>
            </Box>

            <Box>
              <Typography variant="body2" color="text.secondary">
                Active Quantum States
              </Typography>
              <Typography variant="body1">
                {quantum?.activeStates || 0} states
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ height: 200 }}>
              <ResponsiveLine
                data={mockTimeseriesData}
                margin={{ top: 20, right: 20, bottom: 40, left: 40 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 0.5, max: 1 }}
                curve="monotoneX"
                enablePoints={false}
                enableGridX={false}
                enableGridY={true}
                lineWidth={3}
                theme={{
                  textColor: theme.palette.text.secondary,
                  grid: {
                    line: {
                      stroke: theme.palette.grey[800],
                    },
                  },
                }}
                colors={[theme.palette.primary.main]}
              />
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default QuantumLoopVisualization;
