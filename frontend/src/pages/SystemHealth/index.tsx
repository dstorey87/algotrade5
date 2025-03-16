import React, { useEffect, useState } from 'react';
import { Box, Typography, Grid, Card, Divider, List, ListItem, ListItemText, LinearProgress } from '@mui/material';
import { styled } from '@mui/material/styles';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { tradingApi } from '../../services/api';

const Item = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  height: '100%'
}));

const StatusIndicator = styled('span')(({ theme, status }: { theme: any, status: 'online' | 'warning' | 'offline' }) => ({
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
}));

const SystemHealth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  
  // Resource usage history
  const [resourceHistory, setResourceHistory] = useState<any[]>([]);
  
  useEffect(() => {
    fetchMetrics();
    fetchLogs();
    
    // Set up periodic refresh
    const interval = setInterval(() => {
      fetchMetrics();
      fetchLogs();
    }, 30000); // Refresh every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await tradingApi.getSystemMetrics();
      setMetrics(response.data);
      
      // Update resource history
      setResourceHistory(prev => {
        const now = new Date();
        const time = `${now.getHours()}:${now.getMinutes()}`;
        
        const newPoint = {
          time,
          cpu: response.data.resources.cpu_usage,
          memory: response.data.resources.memory_usage,
          gpu: response.data.resources.gpu_utilization
        };
        
        // Keep last 24 points (8 hours with 20min intervals)
        const updated = [...prev, newPoint].slice(-24);
        return updated;
      });
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError('Failed to fetch system metrics');
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await tradingApi.getSystemLogs();
      setLogs(response.data.logs);
    } catch (err) {
      console.error('Error fetching logs:', err);
      setError('Failed to fetch system logs');
    }
  };

  if (!metrics) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box sx={{ width: '100%', py: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ color: 'primary.main', mb: 2 }}>
        System Health
      </Typography>

      <Grid container spacing={3}>
        {/* System Status */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h6" gutterBottom>
              System Status
            </Typography>
            <Box sx={{ p: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Status
                  </Typography>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={metrics.system_status.status === 'running' ? 'online' : 'warning'} />
                    {metrics.system_status.status === 'running' ? 'Online' : 'Degraded'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Version
                  </Typography>
                  <Typography variant="body1">
                    {metrics.system_status.version}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Uptime
                  </Typography>
                  <Typography variant="body1">
                    {metrics.system_status.uptime}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Mode
                  </Typography>
                  <Typography variant="body1">
                    {metrics.system_status.mode}
                  </Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Component Status:
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={metrics.health.database ? 'online' : 'offline'} />
                    Database
                  </Typography>
                  <Typography variant="body2">
                    {metrics.health.database ? 'Connected' : 'Disconnected'}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={metrics.health.api_connected ? 'online' : 'offline'} />
                    API
                  </Typography>
                  <Typography variant="body2">
                    {metrics.health.api_connected ? 'Connected' : 'Disconnected'}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                    <StatusIndicator status={metrics.health.quantum_ready ? 'online' : 'offline'} />
                    Quantum Circuit
                  </Typography>
                  <Typography variant="body2">
                    {metrics.health.quantum_ready ? 'Ready' : 'Not Ready'}
                  </Typography>
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
                    value={metrics.resources.cpu_usage} 
                    color={metrics.resources.cpu_usage > 80 ? 'error' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  {metrics.resources.cpu_usage}%
                </Typography>
              </Box>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Memory Usage
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={metrics.resources.memory_usage} 
                    color={metrics.resources.memory_usage > 80 ? 'error' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  {metrics.resources.memory_usage}%
                </Typography>
              </Box>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                GPU Usage
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={metrics.resources.gpu_utilization} 
                    color={metrics.resources.gpu_utilization > 80 ? 'error' : 'success'}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 35 }}>
                  {metrics.resources.gpu_utilization}%
                </Typography>
              </Box>
              
              <Typography variant="subtitle2" sx={{ mt: 3 }}>
                Storage Summary:
              </Typography>
              <Typography variant="body2">
                Disk Usage: {metrics.resources.disk_usage}%
              </Typography>
            </Box>
          </Item>
        </Grid>

        {/* Resource History */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h6" gutterBottom>
              Resource Usage History
            </Typography>
            <Box sx={{ height: 300, mt: 2 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={resourceHistory}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="cpu" 
                    name="CPU Usage (%)" 
                    stroke="#8884d8" 
                    activeDot={{ r: 8 }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="memory" 
                    name="Memory Usage (%)" 
                    stroke="#82ca9d" 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="gpu" 
                    name="GPU Usage (%)" 
                    stroke="#ffc658" 
                  />
                </LineChart>
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
            {logs.length === 0 ? (
              <Typography variant="body2" color="text.secondary">
                No logs available
              </Typography>
            ) : (
              <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
                <List>
                  {logs.map((log, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={
                            <Typography
                              variant="body2"
                              color={
                                log.level === 'ERROR' 
                                  ? 'error' 
                                  : log.level === 'WARNING'
                                    ? 'warning.main'
                                    : 'text.primary'
                              }
                            >
                              {log.message}
                            </Typography>
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
  );
};

export default SystemHealth;