import { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  InputAdornment,
  Chip,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Tabs,
  Tab,
  IconButton,
  Tooltip
} from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '../../store'
import { fetchTradeData } from '../../store/slices/tradingSlice'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { tradingApi, getMockData } from '../../services/api'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
}))

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
      id={`history-tabpanel-${index}`}
      aria-labelledby={`history-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `history-tab-${index}`,
    'aria-controls': `history-tabpanel-${index}`,
  }
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

// Mock data for trade history
const mockTradeHistory = [
  {
    id: 1,
    pair: "BTC/USDT",
    amount: 0.001,
    openDate: "2023-11-28T09:15:00Z",
    closeDate: "2023-11-28T14:30:00Z",
    openRate: 36250.0,
    closeRate: 36650.0,
    profit: 0.40,
    profitRatio: 0.011,
    strategy: "QuantumHybridStrategy",
    tags: ["AI", "Quantum"]
  },
  {
    id: 2,
    pair: "ETH/USDT",
    amount: 0.05,
    openDate: "2023-11-29T11:00:00Z",
    closeDate: "2023-11-29T16:45:00Z",
    openRate: 2110.0,
    closeRate: 2180.0,
    profit: 3.50,
    profitRatio: 0.033,
    strategy: "TrendFollowingML",
    tags: ["ML", "Trend"]
  },
  {
    id: 3,
    pair: "SOL/USDT",
    amount: 0.5,
    openDate: "2023-11-30T10:30:00Z",
    closeDate: "2023-11-30T15:20:00Z",
    openRate: 102.0,
    closeRate: 107.0,
    profit: 2.50,
    profitRatio: 0.049,
    strategy: "QuantumHybridStrategy",
    tags: ["AI", "Quantum"]
  },
  {
    id: 4,
    pair: "BTC/USDT",
    amount: 0.0015,
    openDate: "2023-11-30T14:15:00Z",
    closeDate: "2023-11-30T19:10:00Z",
    openRate: 36800.0,
    closeRate: 36600.0,
    profit: -0.30,
    profitRatio: -0.005,
    strategy: "ReversalDetector",
    tags: ["Reversal", "Quantum"]
  },
  {
    id: 5,
    pair: "ETH/USDT",
    amount: 0.08,
    openDate: "2023-12-01T08:45:00Z",
    closeDate: "2023-12-01T13:15:00Z",
    openRate: 2170.0,
    closeRate: 2210.0,
    profit: 3.20,
    profitRatio: 0.018,
    strategy: "TrendFollowingML",
    tags: ["ML", "Trend"]
  },
  {
    id: 6,
    pair: "AVAX/USDT",
    amount: 0.75,
    openDate: "2023-12-01T10:05:00Z",
    closeDate: "2023-12-01T17:30:00Z",
    openRate: 24.5,
    closeRate: 25.8,
    profit: 0.98,
    profitRatio: 0.053,
    strategy: "QuantumHybridStrategy",
    tags: ["AI", "Quantum"]
  },
  {
    id: 7,
    pair: "MATIC/USDT",
    amount: 10.0,
    openDate: "2023-12-01T12:20:00Z",
    closeDate: "2023-12-01T18:45:00Z",
    openRate: 0.85,
    closeRate: 0.82,
    profit: -0.30,
    profitRatio: -0.035,
    strategy: "ReversalDetector",
    tags: ["Reversal", "Quantum"]
  }
]

// Mock data for trade stats
const tradeStats = {
  totalTrades: 7,
  winningTrades: 5,
  losingTrades: 2,
  winRate: 0.71,
  totalProfit: 9.98,
  averageProfit: 1.43,
  bestTrade: 3.50,
  worstTrade: -0.30,
  averageDuration: "5h 12m",
  pairDistribution: [
    { name: "BTC/USDT", value: 2 },
    { name: "ETH/USDT", value: 2 },
    { name: "SOL/USDT", value: 1 },
    { name: "AVAX/USDT", value: 1 },
    { name: "MATIC/USDT", value: 1 }
  ],
  strategyDistribution: [
    { name: "QuantumHybridStrategy", value: 3 },
    { name: "TrendFollowingML", value: 2 },
    { name: "ReversalDetector", value: 2 }
  ],
  profitByDay: [
    { date: "2023-11-28", profit: 0.40 },
    { date: "2023-11-29", profit: 3.50 },
    { date: "2023-11-30", profit: 2.20 },
    { date: "2023-12-01", profit: 3.88 }
  ]
}

const TradeHistory = () => {
  const dispatch = useDispatch()
  const [tabValue, setTabValue] = useState(0)
  const [trades, setTrades] = useState<any[]>([])
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState({
    search: '',
    pair: 'all',
    strategy: 'all',
    result: 'all',
    dateFrom: '',
    dateTo: ''
  })

  const { isLoading: storeLoading } = useSelector((state: RootState) => state.trading)

  useEffect(() => {
    const fetchTrades = async () => {
      setLoading(true)
      try {
        // Try to fetch from real API
        // const response = await tradingApi.getTrades(100);
        // setTrades(response.data);

        // Using mock data for now
        setTrades(mockTradeHistory)
        setStats(tradeStats)
      } catch (error) {
        console.log('Using mock data for trade history')
        setTrades(mockTradeHistory)
        setStats(tradeStats)
      } finally {
        setLoading(false)
      }
    }

    fetchTrades()
    dispatch(fetchTradeData() as any)
  }, [dispatch])

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  const handleFilterChange = (field: string, value: string) => {
    setFilter({ ...filter, [field]: value })
  }

  const handleRefresh = () => {
    // In a real app, this would fetch fresh data
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
    }, 1000)
  }

  // Apply filters to trade data
  const filteredTrades = trades.filter(trade => {
    // Search filter
    if (filter.search && !trade.pair.toLowerCase().includes(filter.search.toLowerCase())) {
      return false
    }

    // Pair filter
    if (filter.pair !== 'all' && trade.pair !== filter.pair) {
      return false
    }

    // Strategy filter
    if (filter.strategy !== 'all' && trade.strategy !== filter.strategy) {
      return false
    }

    // Result filter
    if (filter.result === 'profit' && trade.profit <= 0) {
      return false
    }
    if (filter.result === 'loss' && trade.profit >= 0) {
      return false
    }

    // Date filters
    if (filter.dateFrom) {
      const fromDate = new Date(filter.dateFrom)
      const tradeDate = new Date(trade.openDate)
      if (tradeDate < fromDate) {
        return false
      }
    }

    if (filter.dateTo) {
      const toDate = new Date(filter.dateTo)
      const tradeDate = new Date(trade.openDate)
      if (tradeDate > toDate) {
        return false
      }
    }

    return true
  })

  // Extract unique pairs and strategies for filters
  const uniquePairs = [...new Set(trades.map(trade => trade.pair))]
  const uniqueStrategies = [...new Set(trades.map(trade => trade.strategy))]

  if (loading || storeLoading) {
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
    <Box sx={{ width: '100%', pt: 2 }}>
      <Typography variant="h4" gutterBottom sx={{ color: 'primary.main' }}>
        Trade History
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="trade history tabs">
          <Tab label="Trade List" {...a11yProps(0)} />
          <Tab label="Statistics" {...a11yProps(1)} />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Box sx={{ mb: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Search"
                variant="outlined"
                value={filter.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                size="small"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">🔍</InputAdornment>
                  ),
                }}
              />
            </Grid>

            <Grid item xs={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel id="pair-filter-label">Pair</InputLabel>
                <Select
                  labelId="pair-filter-label"
                  value={filter.pair}
                  label="Pair"
                  onChange={(e) => handleFilterChange('pair', e.target.value)}
                >
                  <MenuItem value="all">All Pairs</MenuItem>
                  {uniquePairs.map(pair => (
                    <MenuItem key={pair} value={pair}>{pair}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel id="strategy-filter-label">Strategy</InputLabel>
                <Select
                  labelId="strategy-filter-label"
                  value={filter.strategy}
                  label="Strategy"
                  onChange={(e) => handleFilterChange('strategy', e.target.value)}
                >
                  <MenuItem value="all">All Strategies</MenuItem>
                  {uniqueStrategies.map(strategy => (
                    <MenuItem key={strategy} value={strategy}>{strategy}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel id="result-filter-label">Result</InputLabel>
                <Select
                  labelId="result-filter-label"
                  value={filter.result}
                  label="Result"
                  onChange={(e) => handleFilterChange('result', e.target.value)}
                >
                  <MenuItem value="all">All Results</MenuItem>
                  <MenuItem value="profit">Profit Only</MenuItem>
                  <MenuItem value="loss">Loss Only</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6} md={2}>
              <Button
                variant="outlined"
                fullWidth
                onClick={handleRefresh}
              >
                Refresh
              </Button>
            </Grid>
          </Grid>

          <Grid container spacing={2} alignItems="center" sx={{ mt: 1 }}>
            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="From Date"
                type="date"
                value={filter.dateFrom}
                onChange={(e) => handleFilterChange('dateFrom', e.target.value)}
                size="small"
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="To Date"
                type="date"
                value={filter.dateTo}
                onChange={(e) => handleFilterChange('dateTo', e.target.value)}
                size="small"
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                  {filteredTrades.length} trades found
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="trade history table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Pair</TableCell>
                <TableCell>Open Date</TableCell>
                <TableCell>Close Date</TableCell>
                <TableCell align="right">Amount</TableCell>
                <TableCell align="right">Open Rate</TableCell>
                <TableCell align="right">Close Rate</TableCell>
                <TableCell align="right">Profit</TableCell>
                <TableCell>Strategy</TableCell>
                <TableCell>Tags</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredTrades.map((trade) => (
                <TableRow
                  key={trade.id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {trade.id}
                  </TableCell>
                  <TableCell>{trade.pair}</TableCell>
                  <TableCell>{new Date(trade.openDate).toLocaleString()}</TableCell>
                  <TableCell>{new Date(trade.closeDate).toLocaleString()}</TableCell>
                  <TableCell align="right">{trade.amount}</TableCell>
                  <TableCell align="right">£{trade.openRate.toFixed(2)}</TableCell>
                  <TableCell align="right">£{trade.closeRate.toFixed(2)}</TableCell>
                  <TableCell
                    align="right"
                    sx={{
                      color: trade.profit >= 0 ? 'success.main' : 'error.main',
                      fontWeight: 'bold'
                    }}
                  >
                    £{trade.profit.toFixed(2)} ({(trade.profitRatio * 100).toFixed(2)}%)
                  </TableCell>
                  <TableCell>{trade.strategy}</TableCell>
                  <TableCell>
                    {trade.tags.map((tag: string) => (
                      <Chip
                        key={tag}
                        label={tag}
                        size="small"
                        sx={{ mr: 0.5, mb: 0.5 }}
                        color="primary"
                        variant="outlined"
                      />
                    ))}
                  </TableCell>
                </TableRow>
              ))}
              {filteredTrades.length === 0 && (
                <TableRow>
                  <TableCell colSpan={10} align="center">
                    No trades found matching your filters
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        {stats && (
          <Grid container spacing={3}>
            {/* Trade Overview */}
            <Grid item xs={12} lg={4}>
              <Item>
                <Typography variant="h6" gutterBottom>
                  Trade Statistics
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Total Trades
                      </Typography>
                      <Typography variant="h6">
                        {stats.totalTrades}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Win Rate
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {(stats.winRate * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Winning Trades
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {stats.winningTrades}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Losing Trades
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        {stats.losingTrades}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Total Profit
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        £{stats.totalProfit.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Average Profit
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        £{stats.averageProfit.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Best Trade
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        £{stats.bestTrade.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Worst Trade
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        £{stats.worstTrade.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="body2" color="text.secondary">
                        Average Duration
                      </Typography>
                      <Typography variant="h6">
                        {stats.averageDuration}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </Item>
            </Grid>

            {/* Profit Chart */}
            <Grid item xs={12} lg={8}>
              <Item>
                <Typography variant="h6" gutterBottom>
                  Profit by Day
                </Typography>
                <Box sx={{ height: 300, mt: 2 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                      data={stats.profitByDay}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <RechartsTooltip formatter={(value) => `£${Number(value).toFixed(2)}`} />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="profit"
                        stroke="#8884d8"
                        activeDot={{ r: 8 }}
                        name="Daily Profit"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              </Item>
            </Grid>

            {/* Pair Distribution */}
            <Grid item xs={12} md={6}>
              <Item>
                <Typography variant="h6" gutterBottom>
                  Trade Distribution by Pair
                </Typography>
                <Box sx={{ height: 300, mt: 2 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={stats.pairDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={true}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {stats.pairDistribution.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
              </Item>
            </Grid>

            {/* Strategy Distribution */}
            <Grid item xs={12} md={6}>
              <Item>
                <Typography variant="h6" gutterBottom>
                  Trade Distribution by Strategy
                </Typography>
                <Box sx={{ height: 300, mt: 2 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={stats.strategyDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={true}
                        label={({ name, percent }) => `${name.substring(0, 8)}...: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {stats.strategyDistribution.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
              </Item>
            </Grid>
          </Grid>
        )}
      </TabPanel>
    </Box>
  )
}

export default TradeHistory
