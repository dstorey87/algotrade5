import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Switch,
  FormControlLabel,
  Button,
  useTheme,
  Chip,
} from '@mui/material';
import PsychologyIcon from '@mui/icons-material/Psychology';
import MemoryIcon from '@mui/icons-material/Memory';
import SpeedIcon from '@mui/icons-material/Speed';
import TuneIcon from '@mui/icons-material/Tune';

interface ModelSettings {
  name: string;
  type: 'llm' | 'ml';
  status: 'active' | 'inactive';
  parameters: {
    temperature?: number;
    maxTokens?: number;
    batchSize?: number;
    learningRate?: number;
  };
}

const ModelConfig = () => {
  const theme = useTheme();
  
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [temperature, setTemperature] = useState<number>(0.7);
  const [maxTokens, setMaxTokens] = useState<number>(512);
  const [autoTune, setAutoTune] = useState<boolean>(true);
  
  const models: ModelSettings[] = [
    {
      name: 'deepseek',
      type: 'llm',
      status: 'active',
      parameters: {
        temperature: 0.7,
        maxTokens: 512
      }
    },
    {
      name: 'mistral',
      type: 'llm',
      status: 'active',
      parameters: {
        temperature: 0.8,
        maxTokens: 1024
      }
    },
    {
      name: 'qwen',
      type: 'llm',
      status: 'inactive',
      parameters: {
        temperature: 0.6,
        maxTokens: 2048
      }
    },
    {
      name: 'cibrx',
      type: 'ml',
      status: 'active',
      parameters: {
        batchSize: 32,
        learningRate: 0.001
      }
    }
  ];

  const handleModelChange = (event: any) => {
    const model = models.find(m => m.name === event.target.value);
    if (model && model.parameters.temperature) {
      setTemperature(model.parameters.temperature);
    }
    if (model && model.parameters.maxTokens) {
      setMaxTokens(model.parameters.maxTokens);
    }
    setSelectedModel(event.target.value);
  };

  return (
    <Card sx={{ 
      height: '100%',
      background: `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${theme.palette.background.default} 90%)`,
      boxShadow: theme.shadows[10]
    }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ color: theme.palette.primary.main }}>
          Model Configuration
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Select Model</InputLabel>
              <Select
                value={selectedModel}
                label="Select Model"
                onChange={handleModelChange}
              >
                {models.map((model) => (
                  <MenuItem key={model.name} value={model.name}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {model.type === 'llm' ? <PsychologyIcon /> : <MemoryIcon />}
                      {model.name}
                      <Chip 
                        size="small" 
                        label={model.status}
                        color={model.status === 'active' ? 'success' : 'error'}
                        sx={{ ml: 1 }}
                      />
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle2" gutterBottom>
                Temperature
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item>
                  <SpeedIcon />
                </Grid>
                <Grid item xs>
                  <Slider
                    value={temperature}
                    onChange={(_, value) => setTemperature(value as number)}
                    min={0}
                    max={1}
                    step={0.1}
                    marks
                    disabled={!selectedModel}
                  />
                </Grid>
                <Grid item>
                  <Typography variant="body2">
                    {temperature.toFixed(1)}
                  </Typography>
                </Grid>
              </Grid>
            </Box>

            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle2" gutterBottom>
                Max Tokens
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item>
                  <TuneIcon />
                </Grid>
                <Grid item xs>
                  <Slider
                    value={maxTokens}
                    onChange={(_, value) => setMaxTokens(value as number)}
                    min={256}
                    max={4096}
                    step={256}
                    marks
                    disabled={!selectedModel}
                  />
                </Grid>
                <Grid item>
                  <Typography variant="body2">
                    {maxTokens}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 3 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={autoTune}
                    onChange={(e) => setAutoTune(e.target.checked)}
                    color="primary"
                  />
                }
                label="Auto-tune Parameters"
              />
            </Box>

            <Box sx={{ mt: 2 }}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                disabled={!selectedModel}
              >
                Apply Configuration
              </Button>
            </Box>

            <Box sx={{ mt: 2 }}>
              <Button
                variant="outlined"
                color="secondary"
                fullWidth
                disabled={!selectedModel}
              >
                Reset to Defaults
              </Button>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default ModelConfig;