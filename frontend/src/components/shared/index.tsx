import React from 'react';

type TooltipProps = {
  children: React.ReactNode;
  content: string;
};

export const Tooltip: React.FC<TooltipProps> = ({ children, content }) => (
  <div title={content}>
    {children}
  </div>
);

export * from '@tremor/react';