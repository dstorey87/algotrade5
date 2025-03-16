import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { StrategyManager } from './StrategyManager';

const queryClient = new QueryClient();

describe('StrategyManager', () => {
    beforeEach(() => {
        render(
            <QueryClientProvider client={queryClient}>
                <StrategyManager />
            </QueryClientProvider>
        );
    });

    it('renders strategy list', () => {
        expect(screen.getByTestId('strategy-list')).toBeInTheDocument();
    });

    it('renders strategy editor', () => {
        expect(screen.getByTestId('strategy-editor')).toBeInTheDocument();
    });

    it('updates strategy configuration', async () => {
        const saveButton = screen.getByText('Save Changes');
        fireEvent.click(saveButton);
        await screen.findByText('Strategy updated successfully');
    });
});
