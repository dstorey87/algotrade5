import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders the dashboard header', () => {
    render(<Home />);
    expect(screen.getByText('AlgoTradePro5 Dashboard')).toBeInTheDocument();
  });

  it('displays initial investment card', () => {
    render(<Home />);
    expect(screen.getByText('£10.00')).toBeInTheDocument();
    expect(screen.getByText('Initial Investment')).toBeInTheDocument();
  });

  it('displays current balance card', () => {
    render(<Home />);
    expect(screen.getByText('£0.00')).toBeInTheDocument();
    expect(screen.getByText('Current Balance')).toBeInTheDocument();
  });

  it('displays profit/loss card', () => {
    render(<Home />);
    expect(screen.getByText('0.00%')).toBeInTheDocument();
    expect(screen.getByText('Profit/Loss')).toBeInTheDocument();
  });

  it('displays win/loss ratio card', () => {
    render(<Home />);
    expect(screen.getByText('0/0')).toBeInTheDocument();
    expect(screen.getByText('Win/Loss Ratio')).toBeInTheDocument();
  });

  it('renders AI strategy status panel', () => {
    render(<Home />);
    expect(screen.getByText('AI Strategy Status')).toBeInTheDocument();
    expect(screen.getByText('Quantum Loop Progress')).toBeInTheDocument();
  });

  it('renders recent activity panel', () => {
    render(<Home />);
    expect(screen.getByText('Recent Activity')).toBeInTheDocument();
    expect(
      screen.getByText(
        'No recent trading activity to display. Start trading to view performance metrics and transaction history.'
      )
    ).toBeInTheDocument();
  });

  it('renders system status panel', () => {
    render(<Home />);
    expect(screen.getByText('System Status')).toBeInTheDocument();
    expect(screen.getByText('FreqTrade:')).toBeInTheDocument();
    expect(screen.getByText('AI Models:')).toBeInTheDocument();
    expect(screen.getByText('Database:')).toBeInTheDocument();
  });
});