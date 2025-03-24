import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ErrorBoundary from '../ErrorBoundary';

// Mock Tremor components
jest.mock('@tremor/react', () => ({
  Card: ({ children, decoration, decorationColor }: any) => (
    <div data-testid="tremor-card" data-decoration={decoration} data-decoration-color={decorationColor}>
      {children}
    </div>
  ),
  Title: ({ children }: { children: React.ReactNode }) => (
    <h2 data-testid="tremor-title">{children}</h2>
  ),
  Text: ({ children, className }: any) => (
    <p data-testid="tremor-text" className={className}>{children}</p>
  ),
  Button: ({ children, onClick, color, size }: any) => (
    <button 
      data-testid="tremor-button" 
      onClick={onClick}
      data-color={color}
      data-size={size}
    >
      {children}
    </button>
  ),
}));

// Mock HeroIcons
jest.mock('@heroicons/react/24/outline', () => ({
  ExclamationTriangleIcon: ({ className }: any) => (
    <svg data-testid="error-icon" className={className} />
  ),
}));

// Component that throws an error for testing
const ThrowError = () => {
  throw new Error('Test error');
};

describe('ErrorBoundary', () => {
  // Prevent console.error from cluttering the test output
  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <div data-testid="test-child">Test Content</div>
      </ErrorBoundary>
    );

    expect(screen.getByTestId('test-child')).toBeInTheDocument();
  });

  it('renders error UI when an error occurs', () => {
    render(
      <ErrorBoundary componentName="TestComponent">
        <ThrowError />
      </ErrorBoundary>
    );

    expect(screen.getByTestId('tremor-card')).toBeInTheDocument();
    expect(screen.getByTestId('tremor-title')).toHaveTextContent('TestComponent Error');
    expect(screen.getByText(/A component has encountered an error/i)).toBeInTheDocument();
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('allows recovery with the Try Again button', () => {
    const TestComponent = ({ shouldThrow }: { shouldThrow: boolean }) => {
      if (shouldThrow) {
        throw new Error('Test error');
      }
      return <div data-testid="recovered-component">Component Recovered</div>;
    };

    const { rerender } = render(
      <ErrorBoundary>
        <TestComponent shouldThrow={true} />
      </ErrorBoundary>
    );

    // Error UI should be shown
    expect(screen.getByTestId('tremor-card')).toBeInTheDocument();
    
    // Click the "Try Again" button
    fireEvent.click(screen.getByTestId('tremor-button'));
    
    // Rerender with a non-throwing component
    rerender(
      <ErrorBoundary>
        <TestComponent shouldThrow={false} />
      </ErrorBoundary>
    );
    
    // Component should be recovered
    expect(screen.getByTestId('recovered-component')).toBeInTheDocument();
  });
});