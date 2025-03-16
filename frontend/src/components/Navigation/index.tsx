import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  ChartBarIcon, 
  CubeIcon, 
  BeakerIcon,
  ClockIcon, 
  CogIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  PresentationChartLineIcon,
  CurrencyDollarIcon,
  ServerIcon
} from '@heroicons/react/24/outline'

const navItems = [
  { name: 'Dashboard', path: '/', icon: ChartBarIcon },
  { name: 'Trading Controls', path: '/trading', icon: CubeIcon },
  { name: 'Quantum Control', path: '/quantum', icon: BeakerIcon },
  { name: 'Trade History', path: '/history', icon: ClockIcon },
  { name: 'Strategies', path: '/strategies', icon: PresentationChartLineIcon },
  { name: 'System Health', path: '/system', icon: ServerIcon },
  { name: 'Model Metrics', path: '/models', icon: ChartBarIcon },
  { name: 'Wallet', path: '/wallet', icon: CurrencyDollarIcon },
  { name: 'Settings', path: '/settings', icon: CogIcon },
]

export default function Navigation() {
  const [isExpanded, setIsExpanded] = useState(true)
  const pathname = usePathname()

  return (
    <nav className={`bg-white border-r border-gray-200 ${isExpanded ? 'w-64' : 'w-20'} transition-all duration-300`}>
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h1 className={`font-bold text-primary-600 ${isExpanded ? 'block' : 'hidden'}`}>
            AlgoTradePro5
          </h1>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            {isExpanded ? (
              <ChevronLeftIcon className="w-5 h-5" />
            ) : (
              <ChevronRightIcon className="w-5 h-5" />
            )}
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          <ul className="p-2 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <li key={item.path}>
                  <Link
                    href={item.path}
                    className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                      pathname === item.path
                        ? 'bg-primary-50 text-primary-600'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-6 h-6 shrink-0" />
                    {isExpanded && (
                      <span className="ml-3">{item.name}</span>
                    )}
                  </Link>
                </li>
              )
            })}
          </ul>
        </div>
      </div>
    </nav>
  )
}