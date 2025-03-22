import { ReactNode } from 'react';
import Dashboard from '../pages/Dashboard';
import Strategies from '../pages/Strategies';
import ModelMetrics from '../pages/ModelMetrics';
import SystemHealth from '../pages/SystemHealth';
import TradeHistory from '../pages/TradeHistory';
import QuantumControl from '../pages/QuantumControl';

// Define route structure for the app
export interface RouteItem {
  path: string;
  component: ReactNode;
  label: string;
  icon?: string;
}

// Define all application routes
const appRoutes: RouteItem[] = [
  {
    path: '/',
    component: <Dashboard />,
    label: 'Dashboard'
  },
  {
    path: '/strategies',
    component: <Strategies />,
    label: 'Strategies'
  },
  {
    path: '/model-metrics',
    component: <ModelMetrics />,
    label: 'Model Metrics'
  },
  {
    path: '/system-health',
    component: <SystemHealth />,
    label: 'System Health'
  },
  {
    path: '/trade-history',
    component: <TradeHistory />,
    label: 'Trade History'
  },
  {
    path: '/quantum',
    component: <QuantumControl />,
    label: 'Quantum Control'
  }
];

export default appRoutes;
