import { Box, Paper, Typography, LinearProgress, Tooltip } from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
}))

const Metric = ({ label, value, tooltip }: { label: string; value: string | number; tooltip?: string }) => (
  <Tooltip title={tooltip || ''}>
    <Box sx={{ mb: 2 }}>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {label}
      </Typography>
      <Typography variant="h6">
        {value}
      </Typography>
    </Box>
  </Tooltip>
)

const StrategyStats = () => {
  const { 
    activeStrategy,
    drawdown,
    confidence,
    patternValidation,
    quantumValidation,
    tradesToday,
    winStreak,
    modelPerformance
  } = useSelector((state: RootState) => state.trading)

  return (
    <Item>
      <Typography variant="h6" gutterBottom>
        Strategy Stats
      </Typography>

      <Metric 
        label="Active Strategy" 
        value={activeStrategy || 'None'} 
        tooltip="Currently active trading strategy"
      />

      <Metric 
        label="Drawdown" 
        value={`${(drawdown * 100).toFixed(2)}%`}
        tooltip="Maximum drawdown from peak"
      />

      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          AI Confidence
        </Typography>
        <LinearProgress 
          variant="determinate" 
          value={confidence * 100}
          color={confidence > 0.85 ? "success" : confidence > 0.7 ? "warning" : "error"}
          sx={{ height: 8, borderRadius: 2 }}
        />
        <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
          {(confidence * 100).toFixed(1)}%
        </Typography>
      </Box>

      <Metric 
        label="Pattern Validation" 
        value={patternValidation ? 'Valid' : 'Invalid'}
        tooltip="Current pattern validation status"
      />

      <Metric 
        label="Quantum Validation" 
        value={quantumValidation ? 'Confirmed' : 'Pending'}
        tooltip="Quantum circuit validation status"
      />

      <Metric 
        label="Trades Today" 
        value={tradesToday}
        tooltip="Number of trades executed today"
      />

      <Metric 
        label="Win Streak" 
        value={winStreak}
        tooltip="Current consecutive winning trades"
      />

      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Model Performance
        </Typography>
        <LinearProgress 
          variant="determinate" 
          value={modelPerformance * 100}
          color={modelPerformance > 0.85 ? "success" : modelPerformance > 0.7 ? "warning" : "error"}
          sx={{ height: 8, borderRadius: 2 }}
        />
        <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
          {(modelPerformance * 100).toFixed(1)}%
        </Typography>
      </Box>
    </Item>
  )
}

export default StrategyStats