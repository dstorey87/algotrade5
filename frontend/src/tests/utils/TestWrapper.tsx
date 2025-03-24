import React, { PropsWithChildren } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import tradingReducer from '../../store/slices/tradingSlice';

// Create a test store for Redux
const createTestStore = () => configureStore({
  reducer: {
    trading: tradingReducer,
  },
});

// Create TestWrapper component that provides both Redux and React Query contexts
export const TestWrapper: React.FC<PropsWithChildren> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        staleTime: 0,
      },
    },
  });
  
  const store = createTestStore();
  
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </Provider>
  );
};