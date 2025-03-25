import '@testing-library/jest-dom';
import { TextDecoder, TextEncoder } from 'util';
import { configure } from '@testing-library/react';
import { QueryClient } from '@tanstack/react-query';
import { enableFetchMocks } from 'jest-fetch-mock';

// Mock TextEncoder/TextDecoder for msgpack-lite
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Configure testing library
configure({ testIdAttribute: 'data-testid' });

// Enable fetch mocks
enableFetchMocks();

// Create a shared QueryClient for testing
export const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      cacheTime: Infinity,
    },
  },
});

// Mock Performance API
if (typeof window.performance === 'undefined') {
  window.performance = {
    now: () => Date.now(),
  } as Performance;
}

// Mock for matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock for IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Mock for ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Mock WebSocket
class MockWebSocket {
  onopen: () => void = () => {};
  onclose: () => void = () => {};
  onmessage: (data: any) => void = () => {};
  onerror: () => void = () => {};
  send = jest.fn();
  close = jest.fn();
}

global.WebSocket = MockWebSocket as any;