import { render, screen } from '@testing-library/react';
import ErrorBoundary from '../../components/ErrorBoundary';

describe('ErrorBoundary', () => {
  const ErrorThrowingComponent = () => {
    throw new Error('Test error');
  };

  beforeEach(() => {
    // Prevent console.error from cluttering test output
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders fallback UI when child component throws', () => {
    render(
      <ErrorBoundary>
        <ErrorThrowingComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText(/Something went wrong/i)).toBeInTheDocument();
  });

  it('logs errors to our error monitoring system', () => {
    const mockErrorLogger = jest.fn();
    global.errorLogger = mockErrorLogger;

    render(
      <ErrorBoundary>
        <ErrorThrowingComponent />
      </ErrorBoundary>
    );

    expect(mockErrorLogger).toHaveBeenCalledWith(expect.any(Error));
  });
});