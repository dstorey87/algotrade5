export interface Trade {
  id: string;
  pair: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  timestamp: number;
  strategy: string;
  profitLoss?: number;
}

export interface TradeStats {
  totalTrades: number;
  winRate: number;
  profitLoss: number;
  drawdown: number;
}