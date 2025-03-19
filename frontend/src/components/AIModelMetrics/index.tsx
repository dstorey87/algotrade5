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
      value: aiMetrics.accuracy * 100
    },
    {
      metric: 'Precision',
      value: aiMetrics.precision * 100
    },
    {
      metric: 'Recall',
      value: aiMetrics.recall * 100
    },
    {
      metric: 'F1 Score',
      value: aiMetrics.f1Score * 100
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
                keys={['value']}
                indexBy="metric"
                maxValue={100}
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
                  axis: {
                    ticks: {
                      text: {
                        fill: theme.palette.text.secondary,
                      },
                    },
                  },
                  grid: {
                    line: {
                      stroke: theme.palette.grey[800],
                    },
                  },
                  labels: {
                    text: {
                      fill: theme.palette.text.secondary,
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
                arcLinkLabelsTextColor={theme.palette.text.primary}
                arcLinkLabelsThickness={2}
                arcLinkLabelsColor={{ from: 'color' }}
                arcLabelsSkipAngle={10}
                arcLabelsTextColor={{ from: 'color', modifiers: [['darker', 2]] }}
                theme={{
                  labels: {
                    text: {
                      fill: theme.palette.text.primary,
                    }
                  },
                  legends: {
                    text: {
                      fill: theme.palette.text.secondary,
                    }
                  },
                  tooltip: {
                    container: {
                      background: theme.palette.background.paper,
                      color: theme.palette.text.primary,
                      fontSize: '12px',
                    },
                  }
                }}
                legends={[
                  {
                    anchor: 'bottom',
                    direction: 'row',
                    justify: false,
                    translateX: 0,
                    translateY: 56,
                    itemsSpacing: 0,
                    itemWidth: 100,
                    itemHeight: 18,
                    itemTextColor: theme.palette.text.secondary,
                    itemDirection: 'left-to-right',
                    itemOpacity: 1,
                    symbolSize: 18,
                    symbolShape: 'circle'
                  }
                ]}
              />
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 2 }}>
              <Chip label={`Last Updated: ${new Date().toLocaleTimeString()}`} size="small" />
              <Chip label={`Model: ${aiMetrics.modelName}`} color="primary" size="small" />
              <Chip label={`Confidence: ${(aiMetrics.confidence * 100).toFixed(1)}%`} color="secondary" size="small" />
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default AIModelMetrics;
