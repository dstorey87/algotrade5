import { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  LinearProgress
} from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '../../store'
import { fetchSystemStatus } from '../../store/slices/systemSlice'
import { systemApi } from '../../services/api'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
}))

const StatusIndicator = styled('div')<{ status: 'online' | 'warning' | 'offline' }>(({ theme, status }) => ({
  display: 'inline-block',
  width: 10,
  height: 10,
  borderRadius: '50%',
  marginRight: theme.spacing(1),
  backgroundColor: 
    status === 'online' 
      ? theme.palette.success.main 
      : status === 'warning'
        ? theme.palette.warning.main
        : theme.palette.error.main,
}))

// Mock data for system metrics
const cpuUsageHistory = [
  { time: '00:00', usage: 35 },
  { time: '04:00', usage: 28 },
  { time: '08:00', usage: 42 },
  { time: '12:00', usage: 65 },
  { time: '16:00', usage: 78 },
  { time: '20:00', usage: 52 },
  { time: '24:00', usage: 40 },
]

const memoryUsageHistory = [
  { time: '00:00', usage: 42 },
  { time: '04:00', usage: 38 },
  { time: '08:00', usage: 45 },
  { time: '12:00', usage: 58 },
  { time: '16:00', usage: 72 },
  { time: '20:00', usage: 65 },
  { time: '24:00', usage: 48 },
]

const gpuUsageHistory = [
  { time: '00:00', usage: 55 },
  { time: '04:00', usage: 48 },
  { time: '08:00', usage: 62 },
  { time: '12:00', usage: 75 },
  { time: '16:00', usage: 85 },
  { time: '20:00', usage: 68 },
  { time: '24:00', usage: 58 },
]

const networkThroughputHistory = [
  { time: '00:00', download: 5.2, upload: 1.3 },
  { time: '04:00', download: 3.8, upload: 0.9 },
  { time: '08:00', download: 8.5, upload: 2.2 },
  { time: '12:00', download: 12.4, upload: 3.5 },
  { time: '16:00', download: 9.7, upload: 2.8 },
  { time: '20:00', download: 7.3, upload: 1.9 },
  { time: '24:00', download: 4.5, upload: 1.2 },
]

// Mock system logs
const systemLogs = [
  { 
    timestamp: '2023-12-01T15:45:32', 
    level: 'INFO', 
    message: 'System startup complete' 
  },
  { 
    timestamp: '2023-12-01T15:45:35', 
    level: 'INFO', 
    message: 'Connected to exchange API' 
  },
  { 
    timestamp: '2023-12-01T15:46:12', 
    level: 'INFO', 
    message: 'Loaded AI models successfully' 
  },
  { 
    timestamp: '2023-12-01T15:48:07', 
    level: 'WARNING', 
    message: 'High GPU temperature detected (82°C)' 
  },
  { 
    timestamp: '2023-12-01T15:51:23', 
    level: 'INFO', 
    message: 'Quantum circuit initialization successful' 
  },
  { 
    timestamp: '2023-12-01T16:02:45', 
    level: 'ERROR', 
    message: 'Failed to connect to backup database' 
  },
  { 
    timestamp: '2023-12-01T16:05:18', 
    level: 'INFO', 
    message: 'Strategy QuantumHybridStrategy activated' 
  },
  { 
    timestamp: '2023-12-01T16:12:40', 
    level: 'WARNING', 
    message: 'Network latency increasing (120ms)' 
  },
  { 
    timestamp: '2023-12-01T16:15:55', 
    level: 'INFO', 
    message: 'Trading started in dry run mode' 
  },
  { 
    timestamp: '2023-12-01T16:22:08', 
    level: 'INFO', 
    message: 'First pattern detected: Double Bottom on BTC/USDT' 
  }
]

const SystemHealth = () => {
  const dispatch = useDispatch()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [logs, setLogs] = useState<any[]>(systemLogs) // Using mock data
  
  const {
    status,
    version,
    uptime,
    dryRun,
    tradingMode,
    gpuUtilization,
    memoryUsage,
    systemHealth
  } = useSelector((state: RootState) => state.system)

  useEffect(() => {
    dispatch(fetchSystemStatus() as any)
    
    // Set up periodic refreshes
    const interval = setInterval(() => {
      dispatch(fetchSystemStatus() as any)
    }, 30000) // Refresh every 30 seconds
    
    return () => clearInterval(interval)
  }, [dispatch])
  
  const fetchSystemLogs = async () => {
    setLoading(true)
    try {
      // In a real implementation, this would fetch from the API
      // const response = await systemApi.getLogs()
      // setLogs(response.data)
      
      // Using mock data for now
      setLogs(systemLogs)
    } catch (error) {
      console.error('Error fetching logs:', error)
      setError('Failed to fetch system logs')
    } finally {
      setLoading(false)
    }
  }
  
  const handleRefresh = () => {
    dispatch(fetchSystemStatus() as any)
    fetchSystemLogs()
  }

  return (
    <Box sx={{ width: '100%', py: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ color: 'primary.main', mb: 2 }}>
        System Health
      </Typography>
      
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
        <Button 
          variant="outlined"
          onClick={handleRefresh}
          startIcon={<span>↻</span>}
        >
          Refresh
        </Button>
      </Box>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Grid container spacing={3}>
        {/* System Overview */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h6" gutterBottom>
              System Overview
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Status
                  </Typography>
                  <Typography variant="body1" sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={status === 'running' ? 'online' : 'offline'} />
                    {status === 'running' ? 'Online' : 'Offline'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Version
                  </Typography>
                  <Typography variant="body1">
                    {version || 'Unknown'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Uptime
                  </Typography>
                  <Typography variant="body1">
                    {uptime || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Mode
                  </Typography>
                  <Typography variant="body1">
                    {dryRun ? 'Dry Run' : 'Live'} - {tradingMode || 'Spot'}
                  </Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                Component Status
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={systemHealth.freqtrade ? 'online' : 'offline'} />
                    FreqTrade
                  </Typography>
                  <Chip 
                    label={systemHealth.freqtrade ? 'Online' : 'Offline'} 
                    color={systemHealth.freqtrade ? 'success' : 'error'} 
                    size="small" 
                    variant="outlined"
                  />
                </Box>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={systemHealth.database ? 'online' : 'offline'} />
                    Database
                  </Typography>
                  <Chip 
                    label={systemHealth.database ? 'Connected' : 'Disconnected'} 
                    color={systemHealth.database ? 'success' : 'error'} 
                    size="small" 
                    variant="outlined"
                  />
                </Box>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={systemHealth.models ? 'online' : 'offline'} />
                    AI Models
                  </Typography>
                  <Chip 
                    label={systemHealth.models ? 'Loaded' : 'Not Loaded'} 
                    color={systemHealth.models ? 'success' : 'error'} 
                    size="small" 
                    variant="outlined"
                  />
                </Box>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={systemHealth.quantum ? 'online' : 'offline'} />
                    Quantum Circuit
                  </Typography>
                  <Chip 
                    label={systemHealth.quantum ? 'Ready' : 'Not Ready'} 
                    color={systemHealth.quantum ? 'success' : 'error'} 
                    size="small" 
                    variant="outlined"
                  />
                </Box>
              </Box>
            </Box>
          </Item>
        </Grid>
        
        {/* Resource Usage */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h6" gutterBottom>
              Resource Usage
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" gutterBottom>
                CPU Usage
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={45} 
                    color={45 > 90 ? 'error' : 45 > 70 ? 'warning' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  45%
                </Typography>
              </Box>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Memory Usage
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={memoryUsage} 
                    color={memoryUsage > 90 ? 'error' : memoryUsage > 70 ? 'warning' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  {memoryUsage.toFixed(0)}%
                </Typography>
              </Box>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                GPU Usage
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={gpuUtilization} 
                    color={gpuUtilization > 90 ? 'error' : gpuUtilization > 70 ? 'warning' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  {gpuUtilization.toFixed(0)}%
                </Typography>
              </Box>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Disk Space
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={32} 
                    color="success"
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  32%
                </Typography>
              </Box>
              
              <Typography variant="subtitle2" sx={{ mt: 3 }}>
                Storage Summary:
              </Typography>
              <Typography variant="body2">
                Used: 32.4 GB / Free: 67.6 GB / Total: 100 GB
              </Typography>
              
              <Typography variant="subtitle2" sx={{ mt: 2 }}>
                Network:
              </Typography>
              <Typography variant="body2">
                Download: 5.2 MB/s / Upload: 1.3 MB/s / Latency: 45ms
              </Typography>
            </Box>
          </Item>
        </Grid>
        
        {/* Usage History Charts */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h6" gutterBottom>
              CPU & Memory Usage History (24h)
            </Typography>
            <Box sx={{ height: 300, mt: 2 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" allowDuplicatedCategory={false} />
                  <YAxis yAxisId="left" domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    yAxisId="left"
                    data={cpuUsageHistory} 
                    type="monotone" 
                    dataKey="usage" 
                    name="CPU Usage (%)" 
                    stroke="#8884d8" 
                    activeDot={{ r: 8 }} 
                  />
                  <Line 
                    yAxisId="left" 
                    data={memoryUsageHistory}
                    type="monotone" 
                    dataKey="usage" 
                    name="Memory Usage (%)" 
                    stroke="#82ca9d" 
                  />
                  <Line 
                    yAxisId="left" 
                    data={gpuUsageHistory}
                    type="monotone" 
                    dataKey="usage" 
                    name="GPU Usage (%)" 
                    stroke="#ffc658" 
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Item>
        </Grid>
        
        {/* Network Throughput */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h6" gutterBottom>
              Network Throughput (24h)
            </Typography>
            <Box sx={{ height: 300, mt: 2 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={networkThroughputHistory}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="download" 
                    name="Download (MB/s)" 
                    stroke="#8884d8" 
                    fill="#8884d8" 
                    fillOpacity={0.3}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="upload" 
                    name="Upload (MB/s)" 
                    stroke="#82ca9d" 
                    fill="#82ca9d" 
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </Item>
        </Grid>
        
        {/* System Logs */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h6" gutterBottom>
              System Logs
            </Typography>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
                <CircularProgress size={24} />
              </Box>
            ) : (
              <Box sx={{ mt: 2, maxHeight: '400px', overflow: 'auto' }}>
                <List>
                  {logs.map((log, index) => (
                    <React.Fragment key={index}>
                      <ListItem alignItems="flex-start">
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Chip 
                                label={log.level} 
                                size="small" 
                                color={
                                  log.level === 'ERROR' 
                                    ? 'error' 
                                    : log.level === 'WARNING' 
                                      ? 'warning' 
                                      : 'info'
                                }
                                sx={{ mr: 1 }}
                              />
                              <Typography 
                                component="span" 
                                variant="body2" 
                                color="text.primary"
                              >
                                {log.message}
                              </Typography>
                            </Box>
                          }
                          secondary={
                            <Typography
                              component="span"
                              variant="body2"
                              color="text.secondary"
                            >
                              {new Date(log.timestamp).toLocaleString()}
                            </Typography>
                          }
                        />
                      </ListItem>
                      {index < logs.length - 1 && <Divider component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              </Box>
            )}
          </Item>
        </Grid>
      </Grid>
    </Box>
  )
}

export default SystemHealth