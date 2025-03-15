import { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Card,
  CardContent,
  CardHeader,
  Button,
  Chip,
  Divider
} from '@mui/material'
import { styled } from '@mui/material/styles'
import { strategyApi, getMockData } from '../../services/api'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`strategy-tabpanel-${index}`}
      aria-labelledby={`strategy-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `strategy-tab-${index}`,
    'aria-controls': `strategy-tabpanel-${index}`,
  }
}

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[10],
  },
}))

interface Strategy {
  name: string
  description: string
  winRate: number
  totalTrades: number
  profitFactor: number
  maxDrawdown: number
  avgProfit: number
  avgTradeDuration: string
  pairPerformance: {
    pair: string
    profit: number
    trades: number
  }[]
  parameterRanges: {
    parameter: string
    min: number
    max: number
    current: number
  }[]
  tags: string[]
}

const mockStrategies: Strategy[] = [
  {
    name: 'QuantumHybridStrategy',
    description: 'AI-powered strategy with quantum circuit validation for high-confidence pattern recognition',
    winRate: 0.82,
    totalTrades: 245,
    profitFactor: 2.3,
    maxDrawdown: 3.5,
    avgProfit: 1.2,
    avgTradeDuration: '3h 45m',
    pairPerformance: [
      { pair: 'BTC/USDT', profit: 3.5, trades: 45 },
      { pair: 'ETH/USDT', profit: 2.8, trades: 32 },
      { pair: 'SOL/USDT', profit: 1.9, trades: 28 },
    ],
    parameterRanges: [
      { parameter: 'buy_threshold', min: 0.6, max: 0.95, current: 0.82 },
      { parameter: 'sell_threshold', min: 0.3, max: 0.7, current: 0.45 },
      { parameter: 'rsi_period', min: 7, max: 21, current: 14 },
    ],
    tags: ['AI', 'Quantum', 'Pattern']
  },
  {
    name: 'TrendFollowingML',
    description: 'Machine learning based trend following strategy with dynamic position sizing',
    winRate: 0.76,
    totalTrades: 193,
    profitFactor: 1.9,
    maxDrawdown: 4.2,
    avgProfit: 0.95,
    avgTradeDuration: '4h 20m',
    pairPerformance: [
      { pair: 'BTC/USDT', profit: 2.1, trades: 37 },
      { pair: 'ETH/USDT', profit: 1.8, trades: 29 },
      { pair: 'MATIC/USDT', profit: 1.5, trades: 22 },
    ],
    parameterRanges: [
      { parameter: 'trend_strength', min: 0.3, max: 0.9, current: 0.65 },
      { parameter: 'entry_timing', min: 0.2, max: 0.8, current: 0.5 },
      { parameter: 'position_size', min: 0.1, max: 1.0, current: 0.3 },
    ],
    tags: ['ML', 'Trend', 'Dynamic']
  },
  {
    name: 'ReversalDetector',
    description: 'Detects market reversals using quantum-enhanced pattern recognition',
    winRate: 0.68,
    totalTrades: 158,
    profitFactor: 1.7,
    maxDrawdown: 5.8,
    avgProfit: 1.35,
    avgTradeDuration: '2h 15m',
    pairPerformance: [
      { pair: 'BTC/USDT', profit: 1.8, trades: 32 },
      { pair: 'ETH/USDT', profit: 1.5, trades: 28 },
      { pair: 'AVAX/USDT', profit: 2.1, trades: 19 },
    ],
    parameterRanges: [
      { parameter: 'reversal_strength', min: 0.5, max: 0.95, current: 0.75 },
      { parameter: 'confirmation_window', min: 2, max: 12, current: 6 },
      { parameter: 'risk_factor', min: 0.1, max: 0.5, current: 0.25 },
    ],
    tags: ['Reversal', 'Quantum', 'Short-term']
  }
];

const Strategies = () => {
  const [value, setValue] = useState(0)
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStrategies = async () => {
      setLoading(true)
      try {
        // Try to fetch from real API
        const response = await strategyApi.getStrategies()
        setStrategies(response.data)
      } catch (error) {
        console.log('Using mock data for strategies')
        // Fall back to mock data
        setStrategies(mockStrategies)
      } finally {
        setLoading(false)
      }
    }

    fetchStrategies()
  }, [])

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue)
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  return (
    <Box sx={{ width: '100%', py: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ color: 'primary.main', mb: 3 }}>
        Strategy Management
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="strategy tabs">
          <Tab label="Available Strategies" {...a11yProps(0)} />
          <Tab label="Performance Analysis" {...a11yProps(1)} />
          <Tab label="Strategy Optimizer" {...a11yProps(2)} />
        </Tabs>
      </Box>

      {/* Available Strategies Tab */}
      <TabPanel value={value} index={0}>
        <Grid container spacing={3}>
          {strategies.map((strategy) => (
            <Grid item xs={12} md={6} lg={4} key={strategy.name}>
              <StyledCard>
                <CardHeader 
                  title={strategy.name} 
                  subheader={
                    <Box sx={{ mt: 1 }}>
                      {strategy.tags.map(tag => (
                        <Chip 
                          key={tag} 
                          label={tag} 
                          size="small" 
                          sx={{ mr: 0.5, mb: 0.5 }} 
                          color="primary" 
                          variant="outlined" 
                        />
                      ))}
                    </Box>
                  }
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {strategy.description}
                  </Typography>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2">Win Rate</Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {(strategy.winRate * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2">Total Trades</Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {strategy.totalTrades}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2">Profit Factor</Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {strategy.profitFactor.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2">Max Drawdown</Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {strategy.maxDrawdown.toFixed(1)}%
                      </Typography>
                    </Grid>
                  </Grid>
                  
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-around' }}>
                    <Button variant="outlined" size="small">
                      Details
                    </Button>
                    <Button variant="contained" size="small">
                      Activate
                    </Button>
                  </Box>
                </CardContent>
              </StyledCard>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Performance Analysis Tab */}
      <TabPanel value={value} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Strategy Performance Comparison
              </Typography>
              <Box sx={{ height: 400, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={strategies.map(s => ({
                      name: s.name,
                      winRate: +(s.winRate * 100).toFixed(1),
                      profitFactor: +s.profitFactor.toFixed(2),
                      avgProfit: +s.avgProfit.toFixed(2)
                    }))}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="winRate" name="Win Rate (%)" fill="#8884d8" />
                    <Bar dataKey="profitFactor" name="Profit Factor" fill="#82ca9d" />
                    <Bar dataKey="avgProfit" name="Avg Profit (%)" fill="#ffc658" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Top Performing Pairs
              </Typography>
              <Box sx={{ mt: 2 }}>
                {strategies.length > 0 && strategies[0].pairPerformance.map((pair) => (
                  <Box key={pair.pair} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">{pair.pair}</Typography>
                      <Typography 
                        variant="body2" 
                        sx={{ color: pair.profit >= 0 ? 'success.main' : 'error.main' }}
                      >
                        {pair.profit > 0 ? '+' : ''}{pair.profit.toFixed(2)}%
                      </Typography>
                    </Box>
                    <Box 
                      sx={{ 
                        width: '100%', 
                        height: 8, 
                        bgcolor: 'background.paper',
                        mt: 0.5,
                        borderRadius: 1,
                        overflow: 'hidden'
                      }}
                    >
                      <Box 
                        sx={{ 
                          width: `${Math.min(100, pair.profit * 10)}%`, 
                          height: '100%', 
                          bgcolor: pair.profit >= 0 ? 'success.main' : 'error.main',
                          borderRadius: 1
                        }} 
                      />
                    </Box>
                  </Box>
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Strategy Optimizer Tab */}
      <TabPanel value={value} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Parameter Optimization
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Optimize strategy parameters to improve performance. Quantum-enhanced parameter optimization can explore multiple combinations simultaneously.
              </Typography>
              
              {strategies.length > 0 && strategies[0].parameterRanges.map((param) => (
                <Box key={param.parameter} sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2">{param.parameter}</Typography>
                    <Typography variant="body2">Current: {param.current}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <Typography variant="caption" sx={{ mr: 1 }}>
                      {param.min}
                    </Typography>
                    <Box
                      sx={{
                        flexGrow: 1,
                        height: 4,
                        bgcolor: 'background.paper',
                        borderRadius: 1,
                        position: 'relative',
                      }}
                    >
                      <Box
                        sx={{
                          position: 'absolute',
                          left: `${((param.current - param.min) / (param.max - param.min)) * 100}%`,
                          transform: 'translateX(-50%)',
                          width: 12,
                          height: 12,
                          bgcolor: 'primary.main',
                          borderRadius: '50%',
                          top: -4,
                        }}
                      />
                    </Box>
                    <Typography variant="caption" sx={{ ml: 1 }}>
                      {param.max}
                    </Typography>
                  </Box>
                </Box>
              ))}
              
              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button variant="contained">
                  Start Optimization
                </Button>
                <Button variant="outlined">
                  Reset Parameters
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  )
}

export default Strategies