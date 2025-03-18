'use client'

import { useState } from 'react'
import { Card, Badge, Button, Flex, Title, Text, Grid, Icon, Metric } from '@tremor/react'
import { useHealthCheck } from '@/services/healthCheck'
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  ExclamationTriangleIcon, 
  QuestionMarkCircleIcon, 
  ArrowPathIcon 
} from '@heroicons/react/24/outline'
import { formatDistanceToNow } from 'date-fns'

interface SystemHealthProps {
  className?: string
  compact?: boolean
}

export default function SystemHealth({ className = '', compact = false }: SystemHealthProps) {
  const { health, componentsHealth, checkHealth, isHealthy, isPartiallyHealthy } = useHealthCheck(true, 60000)
  const [isChecking, setIsChecking] = useState(false)

  const handleRefresh = async () => {
    setIsChecking(true)
    await checkHealth()
    setIsChecking(false)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <Icon icon={CheckCircleIcon} color="emerald" variant="solid" />
      case 'offline':
        return <Icon icon={XCircleIcon} color="rose" variant="solid" />
      case 'degraded':
        return <Icon icon={ExclamationTriangleIcon} color="amber" variant="solid" />
      default:
        return <Icon icon={QuestionMarkCircleIcon} color="gray" variant="solid" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'emerald'
      case 'offline':
        return 'rose'
      case 'degraded':
        return 'amber'
      default:
        return 'gray'
    }
  }

  const formatTime = (date: Date | null) => {
    if (!date) return 'Never'
    return formatDistanceToNow(date, { addSuffix: true })
  }

  const overallStatus = isHealthy 
    ? 'Healthy' 
    : isPartiallyHealthy 
    ? 'Degraded' 
    : 'Unhealthy'

  const statusColor = isHealthy 
    ? 'emerald' 
    : isPartiallyHealthy 
    ? 'amber' 
    : 'rose'

  // If in compact mode, show minimal UI
  if (compact) {
    return (
      <div className={className}>
        <Flex alignItems="center" justifyContent="start" className="gap-2">
          <Badge icon={isHealthy ? CheckCircleIcon : ExclamationTriangleIcon} color={statusColor}>
            {overallStatus}
          </Badge>
          <Button 
            size="xs" 
            variant="light" 
            icon={ArrowPathIcon} 
            loading={isChecking}
            onClick={handleRefresh}
            tooltip="Refresh system status"
            color="gray"
          >
            Refresh
          </Button>
        </Flex>
      </div>
    )
  }

  return (
    <Card className={className}>
      <Flex alignItems="center" justifyContent="between">
        <Title>System Health</Title>
        <Button 
          size="xs" 
          variant="secondary" 
          icon={ArrowPathIcon} 
          loading={isChecking}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Flex>

      <Flex className="mt-4 mb-6" justifyContent="start" alignItems="center">
        <Badge icon={isHealthy ? CheckCircleIcon : ExclamationTriangleIcon} color={statusColor} size="xl">
          {overallStatus}
        </Badge>
        <Text className="ml-2">Last checked: {formatTime(health.lastChecked)}</Text>
      </Flex>

      <Grid numItems={1} numItemsSm={2} numItemsMd={4} className="gap-4 mt-4">
        {Object.entries(componentsHealth).map(([key, component]) => (
          <Card key={key} decoration="top" decorationColor={getStatusColor(component.status)}>
            <Flex alignItems="start">
              {getStatusIcon(component.status)}
              <div className="ml-2">
                <Text>{component.name}</Text>
                <Text color={getStatusColor(component.status)} className="font-medium">
                  {component.status.charAt(0).toUpperCase() + component.status.slice(1)}
                </Text>
                {component.latency !== undefined && (
                  <Text className="text-xs text-tremor-content-subtle">
                    Latency: {component.latency}ms
                  </Text>
                )}
                <Text className="text-xs text-tremor-content-subtle">
                  Last checked: {formatTime(component.lastChecked)}
                </Text>
              </div>
            </Flex>
            {component.error && (
              <Text color="rose" className="mt-2 text-xs">
                Error: {component.error}
              </Text>
            )}
          </Card>
        ))}
      </Grid>

      {health.error && (
        <Text color="rose" className="mt-4">
          {health.error}
        </Text>
      )}
    </Card>
  )
}