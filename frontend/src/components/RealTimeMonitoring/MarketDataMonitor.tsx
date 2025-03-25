import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';

interface MarketDataProps {
  pair: string;
  price: number;
  volume: number;
  spread: number;
}

export const MarketDataMonitor: React.FC<MarketDataProps> = ({ 
  pair, 
  price, 
  volume, 
  spread 
}) => {
  return (
    <Card data-testid="market-data-monitor">
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Market Data: {pair}
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Typography color="textSecondary">Price</Typography>
            <Typography variant="h6">${price.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography color="textSecondary">Volume</Typography>
            <Typography variant="h6">{volume.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography color="textSecondary">Spread</Typography>
            <Typography variant="h6">{spread.toFixed(4)}</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};