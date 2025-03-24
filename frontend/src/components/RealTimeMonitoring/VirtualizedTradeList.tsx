import React, { useCallback, useMemo, useEffect } from 'react';
import { FixedSizeList as RWList, ListChildComponentProps } from 'react-window';
import RawAutoSizer from 'react-virtualized-auto-sizer';
import { Trade } from '@/types';
import { usePerformanceMonitor } from '@/hooks/usePerformanceMonitor';

// Type assertions to fix the component type issues
const FixedSizeList = RWList as unknown as React.FC<any>;
const AutoSizer = RawAutoSizer as unknown as React.FC<any>;

interface VirtualizedTradeListProps {
  trades: Trade[];
  rowHeight?: number;
}

const TradeRow = React.memo(({ index, style, data }: ListChildComponentProps<Trade[]>) => {
  const trade = data[index];
  return (
    <div style={style} className="trade-row">
      <span>{trade.pair}</span>
      <span>{trade.type}</span>
      <span>{trade.profit}</span>
    </div>
  );
});

TradeRow.displayName = 'TradeRow';

export const VirtualizedTradeList = React.forwardRef<HTMLDivElement, VirtualizedTradeListProps>(({ 
  trades,
  rowHeight = 35
}, ref) => {
  const { logRenderTime } = usePerformanceMonitor('VirtualizedTradeList');

  const sortedTrades = useMemo(() => {
    const startTime = performance.now();
    const sorted = [...trades].sort((a, b) => {
      const aTime = new Date(a.timestamp).getTime();
      const bTime = new Date(b.timestamp).getTime();
      return bTime - aTime;
    });
    logRenderTime(performance.now() - startTime);
    return sorted;
  }, [trades, logRenderTime]);

  // Performance monitoring for render cycles
  useEffect(() => {
    const startTime = performance.now();
    return () => {
      logRenderTime(performance.now() - startTime);
    };
  });

  const getItemKey = useCallback((index: number) => {
    return sortedTrades[index].id;
  }, [sortedTrades]);

  return (
    <div ref={ref} style={{ height: '100%', width: '100%' }}>
      <AutoSizer>
        {({ height, width }: { height: number; width: number }) => (
          <FixedSizeList
            height={height}
            width={width}
            itemCount={sortedTrades.length}
            itemSize={rowHeight}
            itemData={sortedTrades}
            itemKey={getItemKey}
            overscanCount={5} // Optimize rendering by pre-rendering additional items
          >
            {TradeRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </div>
  );
});