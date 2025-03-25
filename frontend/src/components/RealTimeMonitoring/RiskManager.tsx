import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';

interface RiskManagerProps {
  maxDrawdown: number;
  currentDrawdown: number;
  riskPerTrade: number;
  activePositions: number;
  marginUsage: number;
}

export const RiskManager: React.FC<RiskManagerProps> = ({
  maxDrawdown,
  currentDrawdown,
  riskPerTrade,
  activePositions,
  marginUsage
}) => {
  const isDrawdownWarning = currentDrawdown > maxDrawdown * 0.8;
  const isMarginWarning = marginUsage > 80;

  return (
    <Card data-testid="risk-manager">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Risk Management
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography color="textSecondary">Current Drawdown</Typography>
            <Typography 
              variant="h6" 
              color={isDrawdownWarning ? 'error' : 'inherit'}
            >
              {currentDrawdown.toFixed(2)}%
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography color="textSecondary">Risk Per Trade</Typography>
            <Typography variant="h6">{riskPerTrade.toFixed(2)}%</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography color="textSecondary">Active Positions</Typography>
            <Typography variant="h6">{activePositions}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography color="textSecondary">Margin Usage</Typography>
            <Typography 
              variant="h6"
              color={isMarginWarning ? 'error' : 'inherit'}
            >
              {marginUsage.toFixed(2)}%
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};