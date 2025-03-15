import { Routes, Route } from 'react-router-dom'
import Dashboard from '../pages/Dashboard'
import Strategies from '../pages/Strategies'
import ModelMetrics from '../pages/ModelMetrics'
import SystemHealth from '../pages/SystemHealth'
import TradeHistory from '../pages/TradeHistory'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/strategies" element={<Strategies />} />
      <Route path="/model-metrics" element={<ModelMetrics />} />
      <Route path="/system-health" element={<SystemHealth />} />
      <Route path="/trade-history" element={<TradeHistory />} />
    </Routes>
  )
}

export default AppRoutes