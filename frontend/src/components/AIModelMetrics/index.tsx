import React from 'react';
import { Box, Card, CardContent, Typography, Grid, Chip, useTheme } from '@mui/material';
import { ResponsiveRadar } from '@nivo/radar';
import { ResponsivePie } from '@nivo/pie';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';

const AIModelMetrics = () => {
  const theme = useTheme();
  const aiMetrics = useSelector((state: RootState) => state.trading.aiMetrics);

  const radarData = [
    {
      metric: 'Accuracy',
      Model1: 0.92,
      Model2: 0.85,
      Model3: 0.88
    },
    {
      metric: 'Precision',
      Model1: 0.89,
      Model2: 0.82,
      Model3: 0.86
    },
    {
      metric: 'Recall',
      Model1: 0.87,
      Model2: 0.84,
      Model3: 0.85
    },
    {
      metric: 'F1 Score',
      Model1: 0.88,
      Model2: 0.83,
      Model3: 0.85
    },
    {
      metric: 'ROC AUC',
      Model1: 0.91,
      Model2: 0.86,
      Model3: 0.89
    }
  ];

  const pieData = [
    {
      id: 'Successful Predictions',
      label: 'Successful',
      value: 75,
      color: theme.palette.success.main
    },
    {
      id: 'False Positives',
      label: 'False Positives',
      value: 15,
      color: theme.palette.warning.main
    },
    {
      id: 'False Negatives',
      label: 'False Negatives',
      value: 10,
      color: theme.palette.error.main
    }
  ];

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          AI Model Performance
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Box sx={{ height: 300 }}>
              <ResponsiveRadar
                data={radarData}
                keys={['Model1', 'Model2', 'Model3']}
                indexBy="metric"
                maxValue={1}
                margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
                borderColor={{ from: 'color' }}
                gridLabelOffset={20}
                dotSize={6}
                dotColor={{ theme: 'background' }}
                dotBorderWidth={2}
                colors={[theme.palette.primary.main, theme.palette.secondary.main, theme.palette.info.main]}
                blendMode="multiply"
                motionConfig="wobbly"
                theme={{
                  textColor: theme.palette.text.secondary,
                  grid: {
                    line: {
                      stroke: theme.palette.grey[800],
                    },
                  },
                }}
              />
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ height: 300 }}>
              <ResponsivePie
                data={pieData}
                margin={{ top: 40, right: 80, bottom: 40, left: 80 }}
                innerRadius={0.5}
                padAngle={0.7}
                cornerRadius={3}
                activeOuterRadiusOffset={8}
                borderWidth={1}
                borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
                arcLinkLabelsSkipAngle={10}
                arcLinkLabelsTextColor={theme.palette.text.secondary}
                arcLinkLabelsThickness={2}
                arcLinkLabelsColor={{ from: 'color' }}
                arcLabelsSkipAngle={10}
                arcLabelsTextColor={{ from: 'color', modifiers: [['darker', 2]] }}
                theme={{
                  textColor: theme.palette.text.secondary,
                }}
              />
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Chip
                label={`Ensemble Accuracy: ${(aiMetrics?.ensembleAccuracy * 100 || 0).toFixed(1)}%`}
                color="primary"
                variant="outlined"
              />
              <Chip
                label={`Active Models: ${aiMetrics?.activeModels || 0}`}
                color="secondary"
                variant="outlined"
              />
              <Chip
                label={`Training Status: ${aiMetrics?.trainingInProgress ? 'In Progress' : 'Idle'}`}
                color={aiMetrics?.trainingInProgress ? 'warning' : 'success'}
                variant="outlined"
              />
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default AIModelMetrics;
