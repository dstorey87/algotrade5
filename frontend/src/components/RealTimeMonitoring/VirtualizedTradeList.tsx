import React, { memo } from 'react';
import { FixedSizeList } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';
import { Paper, Typography, Box } from '@mui/material';
import type { Trade } from '../../services/websocket';

interface Props {
  trades: Trade[];
}

const TradeRow = memo(({ index, style, data }: any) => {
  const trade = data[index];
  const profit = trade.profit;
  const color = profit >= 0 ? '#00ff88' : '#ff0088';

  return (
    <Box
      style={style}
      sx={{
        display: 'flex',
        alignItems: 'center',
        padding: 2,
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        backgroundColor: index % 2 === 0 ? 'rgba(0,0,0,0.02)' : 'transparent',
        '&:hover': {
          backgroundColor: 'rgba(0,0,0,0.1)',
        }
      }}
    >
      <Typography sx={{ flex: 1 }}>{trade.pair}</Typography>
      <Typography sx={{ flex: 1 }}>{trade.type.toUpperCase()}</Typography>
      <Typography sx={{ flex: 1, color }}>
        {profit.toFixed(8)} BTC
      </Typography>
      <Typography sx={{ flex: 1 }}>
        {new Date(trade.timestamp).toLocaleTimeString()}
      </Typography>
    </Box>
  );
});

TradeRow.displayName = 'TradeRow';

export const VirtualizedTradeList: React.FC<Props> = ({ trades }) => {
  return (
    <Paper sx={{ height: '60vh', bgcolor: 'background.paper' }}>
      <Box sx={{ display: 'flex', p: 2, borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <Typography sx={{ flex: 1, fontWeight: 'bold' }}>Pair</Typography>
        <Typography sx={{ flex: 1, fontWeight: 'bold' }}>Type</Typography>
        <Typography sx={{ flex: 1, fontWeight: 'bold' }}>Profit</Typography>
        <Typography sx={{ flex: 1, fontWeight: 'bold' }}>Time</Typography>
      </Box>
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            height={height - 56} // Subtract header height
            width={width}
            itemCount={trades.length}
            itemSize={64}
            itemData={trades}
            overscanCount={5}
          >
            {TradeRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </Paper>
  );
};