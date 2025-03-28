'use client';

import React, { useEffect } from 'react';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';

// Simple logger for development
const logger = {
  info: (message: string, data?: any) => console.info(`[INFO] ${message}`, data || ''),
  debug: (message: string, data?: any) => console.debug(`[DEBUG] ${message}`, data || ''),
  error: (message: string, data?: any) => console.error(`[ERROR] ${message}`, data || '')
};

/**
 * Application Dark Theme
 */
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3f8cff',
    },
    secondary: {
      main: '#ff9f46',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

/**
 * Simplified Client Layout Component
 */
export default function ClientLayout({ children }: { children: React.ReactNode }) {
  // Log layout initialization for debugging
  useEffect(() => {
    logger.info('Simplified client layout initialized');
    
    // Log routing information to help debug issues
    if (typeof window !== 'undefined') {
      logger.debug('App initialization', {
        url: window.location.href,
        pathname: window.location.pathname
      });
    }
  }, []);

  // Simple try-catch to handle any rendering errors safely
  try {
    return (
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    );
  } catch (error) {
    logger.error('Error in ClientLayout', error);
    return (
      <div style={{ padding: '20px', color: 'white', backgroundColor: '#121212', height: '100vh' }}>
        <h1>Something went wrong</h1>
        <p>There was an error loading the application layout.</p>
        <button onClick={() => window.location.reload()}>Reload page</button>
      </div>
    );
  }
}