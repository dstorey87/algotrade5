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

const ErrorComponent = () => {
  throw new Error('Test error');
};

const RecoverableComponent = ({ shouldError }: { shouldError: boolean }) => {
  if (shouldError) {
    throw new Error('Test error');
  }
  return <div data-testid="recovered-component">Recovered Content</div>;
};

describe('ErrorBoundary', () => {
  // Prevent console.error from cluttering the test output
  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
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

  it('renders error UI when there is an error', () => {
    render(
      <ErrorBoundary>
        <ErrorComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText(/Component Error/i)).toBeInTheDocument();
    expect(screen.getByText(/Test error/i)).toBeInTheDocument();
  });

  it('allows recovery with the Try Again button', () => {
    const { rerender } = render(
      <ErrorBoundary>
        <RecoverableComponent shouldError={true} />
      </ErrorBoundary>
    );

    // First, we see the error
    expect(screen.getByText(/Component Error/i)).toBeInTheDocument();

    // Click try again and rerender with shouldError=false
    fireEvent.click(screen.getByText('Try Again'));
    rerender(
      <ErrorBoundary>
        <RecoverableComponent shouldError={false} />
      </ErrorBoundary>
    );
    
    // Component should be recovered
    expect(screen.getByTestId('recovered-component')).toBeInTheDocument();
  });
});