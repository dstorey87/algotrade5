import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  CircularProgress,
  useTheme,
  Slider,
  FormControlLabel,
  Switch,
  Chip,
} from '@mui/material';
import TimelineIcon from '@mui/icons-material/Timeline';
import SyncIcon from '@mui/icons-material/Sync';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LoopIcon from '@mui/icons-material/Loop';

const QuantumControl = () => {
  const theme = useTheme();
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [loopCount, setLoopCount] = useState(100);
  const [autoOptimize, setAutoOptimize] = useState(true);
  const [optimizationProgress, setOptimizationProgress] = useState(0);

  const startOptimization = () => {
    setIsOptimizing(true);
    // Simulate optimization progress
    const interval = setInterval(() => {
      setOptimizationProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsOptimizing(false);
          return 0;
        }
        return prev + 10;
      });
    }, 1000);
  };

  const metrics = [
    { label: 'Quantum Coherence', value: '98.2%', trend: 'up' },
    { label: 'Loop Efficiency', value: '87.5%', trend: 'up' },
    { label: 'Strategy Alignment', value: '92.3%', trend: 'up' },
    { label: 'Optimization Score', value: '95.1%', trend: 'up' },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card sx={{
            height: '100%',
            background: `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${theme.palette.background.default} 90%)`,
            boxShadow: theme.shadows[10]
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: theme.palette.primary.main }}>
                Quantum Loop Control
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Loop Iterations
                    </Typography>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item>
                        <LoopIcon />
                      </Grid>
                      <Grid item xs>
                        <Slider
                          value={loopCount}
                          onChange={(_, value) => setLoopCount(value as number)}
                          min={10}
                          max={1000}
                          step={10}
                          marks
                          disabled={isOptimizing}
                        />
                      </Grid>
                      <Grid item>
                        <Typography variant="body2">
                          {loopCount}
                        </Typography>
                      </Grid>
                    </Grid>
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={autoOptimize}
                          onChange={(e) => setAutoOptimize(e.target.checked)}
                          color="primary"
                          disabled={isOptimizing}
                        />
                      }
                      label="Auto-optimize"
                    />
                  </Box>

                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={isOptimizing ? <CircularProgress size={20} /> : <SyncIcon />}
                      onClick={startOptimization}
                      disabled={isOptimizing}
                      fullWidth
                    >
                      {isOptimizing ? 'Optimizing...' : 'Start Optimization'}
                    </Button>
                    <Button
                      variant="outlined"
                      color="secondary"
                      disabled={!isOptimizing}
                      fullWidth
                    >
                      Stop
                    </Button>
                  </Box>

                  {isOptimizing && (
                    <Box sx={{ mt: 2, width: '100%' }}>
                      <Typography variant="body2" color="textSecondary">
                        Optimization Progress
                      </Typography>
                      <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ width: '100%', mr: 1 }}>
                          <LinearProgress variant="determinate" value={optimizationProgress} />
                        </Box>
                        <Box sx={{ minWidth: 35 }}>
                          <Typography variant="body2" color="textSecondary">{`${Math.round(
                            optimizationProgress,
                          )}%`}</Typography>
                        </Box>
                      </Box>
                    </Box>
                  )}
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{
            height: '100%',
            background: `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${theme.palette.background.default} 90%)`,
            boxShadow: theme.shadows[10]
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: theme.palette.primary.main }}>
                Quantum Metrics
              </Typography>

              <Grid container spacing={2}>
                {metrics.map((metric) => (
                  <Grid item xs={12} key={metric.label}>
                    <Box sx={{
                      p: 2,
                      borderRadius: 1,
                      bgcolor: 'rgba(0, 0, 0, 0.1)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <Typography variant="body2">
                        {metric.label}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Chip
                          label={metric.value}
                          size="small"
                          color="primary"
                        />
                        <TrendingUpIcon color="success" sx={{ fontSize: 16 }} />
                      </Box>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default QuantumControl;
