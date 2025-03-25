import React, { useRef, useEffect, useState } from 'react';

interface VirtualizedListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  itemHeight: number;
  maxHeight: number;
}

export function VirtualizedList<T>({ 
  items, 
  renderItem, 
  itemHeight, 
  maxHeight 
}: VirtualizedListProps<T>) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 20 });

  useEffect(() => {
    const updateVisibleRange = () => {
      if (!containerRef.current) return;

      const scrollTop = containerRef.current.scrollTop;
      const viewportHeight = containerRef.current.clientHeight;

      const start = Math.floor(scrollTop / itemHeight);
      const visibleItems = Math.ceil(viewportHeight / itemHeight);
      const end = Math.min(start + visibleItems + 5, items.length);

      setVisibleRange({ start: Math.max(0, start - 5), end });
    };

    const container = containerRef.current;
    if (container) {
      container.addEventListener('scroll', updateVisibleRange);
      updateVisibleRange();
    }

    return () => {
      if (container) {
        container.removeEventListener('scroll', updateVisibleRange);
      }
    };
  }, [items.length, itemHeight]);

  const totalHeight = items.length * itemHeight;
  const offsetY = visibleRange.start * itemHeight;

  const visibleItems = items
    .slice(visibleRange.start, visibleRange.end)
    .map(renderItem);

  return (
    <div
      ref={containerRef}
      style={{ 
        height: Math.min(totalHeight, maxHeight), 
        overflowY: 'auto' 
      }}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems}
        </div>
      </div>
    </div>
  );
}