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
  Divider,
  LinearProgress
} from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
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
      id={`metrics-tabpanel-${index}`}
      aria-labelledby={`metrics-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

function a11yProps(index: number) {
  return {
    id: `metrics-tab-${index}`,
    'aria-controls': `metrics-tabpanel-${index}`,
  }
}

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
}))

// Mock data for model metrics
const predictionAccuracyHistory = [
  { date: '2023-11-25', accuracy: 0.78 },
  { date: '2023-11-26', accuracy: 0.79 },
  { date: '2023-11-27', accuracy: 0.81 },
  { date: '2023-11-28', accuracy: 0.83 },
  { date: '2023-11-29', accuracy: 0.85 },
  { date: '2023-11-30', accuracy: 0.84 },
  { date: '2023-12-01', accuracy: 0.87 }
]

const modelConfidenceHistory = [
  { date: '2023-11-25', confidence: 0.84 },
  { date: '2023-11-26', confidence: 0.85 },
  { date: '2023-11-27', confidence: 0.88 },
  { date: '2023-11-28', confidence: 0.90 },
  { date: '2023-11-29', confidence: 0.91 },
  { date: '2023-11-30', confidence: 0.89 },
  { date: '2023-12-01', confidence: 0.92 }
]

const patternRecognitionData = [
  { name: 'Double Top', value: 28 },
  { name: 'Double Bottom', value: 35 },
  { name: 'Head & Shoulders', value: 15 },
  { name: 'Triangle', value: 18 },
  { name: 'Rectangle', value: 12 }
]

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

const modelPerformanceData = [
  {
    subject: 'Accuracy',
    A: 0.87,
    fullMark: 1,
  },
  {
    subject: 'Confidence',
    A: 0.92,
    fullMark: 1,
  },
  {
    subject: 'Speed',
    A: 0.95,
    fullMark: 1,
  },
  {
    subject: 'Stability',
    A: 0.83,
    fullMark: 1,
  },
  {
    subject: 'Memory Usage',
    A: 0.75,
    fullMark: 1,
  },
  {
    subject: 'Quantum Validation',
    A: 0.89,
    fullMark: 1,
  },
]

const MetricCard = ({ title, value, maxValue = 100, suffix = '%', color = 'primary' }: {
  title: string;
  value: number;
  maxValue?: number;
  suffix?: string;
  color?: 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning';
}) => {
  const percentage = (value / maxValue) * 100;

  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Box sx={{ mt: 2, mb: 1, display: 'flex', justifyContent: 'space-between' }}>
          <Typography variant="body2" color="text.secondary">
            0
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {maxValue}
          </Typography>
        </Box>
        <LinearProgress
          variant="determinate"
          value={percentage}
          color={color}
          sx={{ height: 8, borderRadius: 4 }}
        />
        <Typography variant="h4" sx={{ mt: 2, textAlign: 'center' }}>
          {value.toFixed(2)}{suffix}
        </Typography>
      </CardContent>
    </Card>
  )
}

const ModelMetrics = () => {
  const [value, setValue] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    modelAccuracy,
    modelConfidence,
    quantumCircuitStatus
  } = useSelector((state: RootState) => state.system)

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
        AI Model Metrics
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="model metrics tabs">
          <Tab label="Performance Overview" {...a11yProps(0)} />
          <Tab label="Pattern Recognition" {...a11yProps(1)} />
          <Tab label="Quantum Circuit" {...a11yProps(2)} />
        </Tabs>
      </Box>

      {/* Performance Overview Tab */}
      <TabPanel value={value} index={0}>
        <Grid container spacing={3}>
          {/* Key Metrics */}
          <Grid item xs={12} md={4}>
            <MetricCard
              title="Model Accuracy"
              value={modelAccuracy * 100}
              color="primary"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <MetricCard
              title="Prediction Confidence"
              value={modelConfidence * 100}
              color="success"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <MetricCard
              title="Processing Speed"
              value={95.3}
              suffix=" ms"
              maxValue={1000}
              color="info"
            />
          </Grid>

          {/* Performance History */}
          <Grid item xs={12} md={6}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Accuracy Trend (7 Days)
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={predictionAccuracyHistory}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0.7, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                    <Tooltip formatter={(value) => `${(Number(value) * 100).toFixed(2)}%`} />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#8884d8"
                      activeDot={{ r: 8 }}
                      name="Accuracy"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </Item>
          </Grid>

          <Grid item xs={12} md={6}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Confidence Trend (7 Days)
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={modelConfidenceHistory}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0.8, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                    <Tooltip formatter={(value) => `${(Number(value) * 100).toFixed(2)}%`} />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="confidence"
                      stroke="#82ca9d"
                      activeDot={{ r: 8 }}
                      name="Confidence"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </Item>
          </Grid>

          {/* Radar Chart */}
          <Grid item xs={12}>
            <Item>
              <Typography variant="h6" gutterBottom>
                AI Model Performance Metrics
              </Typography>
              <Box sx={{ height: 400, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart outerRadius={150} width={500} height={500} data={modelPerformanceData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis angle={30} domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                    <Radar
                      name="Model Performance"
                      dataKey="A"
                      stroke="#8884d8"
                      fill="#8884d8"
                      fillOpacity={0.6}
                    />
                    <Legend />
                    <Tooltip formatter={(value) => `${(Number(value) * 100).toFixed(2)}%`} />
                  </RadarChart>
                </ResponsiveContainer>
              </Box>
            </Item>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Pattern Recognition Tab */}
      <TabPanel value={value} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Pattern Recognition Distribution
              </Typography>
              <Box sx={{ height: 400, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={patternRecognitionData}
                      cx="50%"
                      cy="50%"
                      labelLine={true}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={150}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {patternRecognitionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value} instances`} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </Item>
          </Grid>

          <Grid item xs={12} md={6}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Pattern Recognition Success Rate
              </Typography>
              <Box sx={{ p: 2 }}>
                {/* Double Top */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Double Top</Typography>
                    <Typography variant="body1" fontWeight="bold">82%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={82}
                    color="success"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                {/* Double Bottom */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Double Bottom</Typography>
                    <Typography variant="body1" fontWeight="bold">89%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={89}
                    color="success"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                {/* Head & Shoulders */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Head & Shoulders</Typography>
                    <Typography variant="body1" fontWeight="bold">75%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={75}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                {/* Triangle */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Triangle</Typography>
                    <Typography variant="body1" fontWeight="bold">79%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={79}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                {/* Rectangle */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Rectangle</Typography>
                    <Typography variant="body1" fontWeight="bold">68%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={68}
                    color="warning"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>
              </Box>
            </Item>
          </Grid>

          <Grid item xs={12}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Pattern Detection Improvements
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body1" paragraph>
                  The AI model has shown significant improvements in pattern detection capabilities over time. The quantum validation circuit has improved accuracy by 12% over the last 30 days.
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle1" gutterBottom>
                  Key Improvements:
                </Typography>
                <ul>
                  <li>Enhanced noise filtering using quantum algorithms</li>
                  <li>Improved pattern validation with multi-asset correlation</li>
                  <li>Reduced false positives by 23%</li>
                  <li>Increased confidence scoring precision</li>
                </ul>
              </Box>
            </Item>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Quantum Circuit Tab */}
      <TabPanel value={value} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card variant="outlined" sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quantum Circuit Status
                </Typography>
                <Typography variant="h4" sx={{ mt: 2, textAlign: 'center', color: 'primary.main' }}>
                  {quantumCircuitStatus}
                </Typography>
                <Box sx={{ mt: 3, mb: 1 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Circuit Validation Rate
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={96}
                    color="success"
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 0.5 }}>
                    <Typography variant="body2" color="text.secondary">
                      96%
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ mt: 2, mb: 1 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Quantum Error Correction
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={89}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 0.5 }}>
                    <Typography variant="body2" color="text.secondary">
                      89%
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={8}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Quantum Algorithm Performance
              </Typography>
              <Box sx={{ p: 2 }}>
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Grover's Search</Typography>
                    <Typography variant="body1" fontWeight="bold">94%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={94}
                    color="success"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Quantum Fourier Transform</Typography>
                    <Typography variant="body1" fontWeight="bold">87%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={87}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Quantum Neural Network</Typography>
                    <Typography variant="body1" fontWeight="bold">91%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={91}
                    color="success"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body1">Variational Quantum Eigensolver</Typography>
                    <Typography variant="body1" fontWeight="bold">82%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={82}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4, mt: 1 }}
                  />
                </Box>
              </Box>
            </Item>
          </Grid>

          <Grid item xs={12}>
            <Item>
              <Typography variant="h6" gutterBottom>
                Quantum Circuit Details
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle1" gutterBottom>
                      Configuration
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Circuit Depth
                      </Typography>
                      <Typography variant="body1">
                        24 gates
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Qubits
                      </Typography>
                      <Typography variant="body1">
                        8 qubits
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Error Correction
                      </Typography>
                      <Typography variant="body1">
                        Surface code
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle1" gutterBottom>
                      Performance
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Execution Time
                      </Typography>
                      <Typography variant="body1">
                        85 ms
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Fidelity
                      </Typography>
                      <Typography variant="body1">
                        92%
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        SWAP Operations
                      </Typography>
                      <Typography variant="body1">
                        12
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle1" gutterBottom>
                      Usage
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Daily Executions
                      </Typography>
                      <Typography variant="body1">
                        1,432
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Success Rate
                      </Typography>
                      <Typography variant="body1">
                        98.5%
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Pattern Validation
                      </Typography>
                      <Typography variant="body1">
                        8 patterns
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            </Item>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  )
}

export default ModelMetrics
