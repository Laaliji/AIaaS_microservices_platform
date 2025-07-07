import { useState } from 'react'
import { 
  ArrowUpIcon, 
  ArrowDownIcon,
  ServerIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

// Mock data
const stats = [
  { 
    id: 1, 
    name: 'Total API Requests', 
    value: '8,249', 
    change: '+12.5%', 
    trend: 'up',
    icon: ServerIcon,
    color: 'bg-blue-500'
  },
  { 
    id: 2, 
    name: 'Documents Processed', 
    value: '1,432', 
    change: '+5.2%', 
    trend: 'up',
    icon: DocumentTextIcon,
    color: 'bg-purple-500'
  },
  { 
    id: 3, 
    name: 'Avg. Response Time', 
    value: '245ms', 
    change: '-18.3%', 
    trend: 'down',
    icon: ClockIcon,
    color: 'bg-green-500'
  },
  { 
    id: 4, 
    name: 'Success Rate', 
    value: '99.8%', 
    change: '+0.3%', 
    trend: 'up',
    icon: CheckCircleIcon,
    color: 'bg-amber-500'
  },
]

const recentActivities = [
  {
    id: 1,
    type: 'text-generation',
    status: 'completed',
    timestamp: '2 minutes ago',
    details: 'Generated response for customer inquiry'
  },
  {
    id: 2,
    type: 'sentiment-analysis',
    status: 'completed',
    timestamp: '5 minutes ago',
    details: 'Analyzed 24 customer reviews'
  },
  {
    id: 3,
    type: 'rag-workflow',
    status: 'completed',
    timestamp: '15 minutes ago',
    details: 'Processed financial report Q2 2025'
  },
  {
    id: 4,
    type: 'embeddings',
    status: 'completed',
    timestamp: '32 minutes ago',
    details: 'Generated embeddings for product catalog'
  },
]

const Dashboard = () => {
  const [timeRange, setTimeRange] = useState('24h')

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
        
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Time Range:</span>
          <div className="inline-flex rounded-md shadow-sm">
            {['24h', '7d', '30d', '90d'].map((range) => (
              <button
                key={range}
                type="button"
                onClick={() => setTimeRange(range)}
                className={`relative inline-flex items-center px-3 py-1.5 text-sm font-medium ${
                  timeRange === range
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                } ${
                  range === '24h' ? 'rounded-l-md' : ''
                } ${
                  range === '90d' ? 'rounded-r-md' : ''
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <motion.div
            key={stat.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: stat.id * 0.1 }}
            className="overflow-hidden rounded-lg bg-card shadow"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 rounded-md p-3 ${stat.color}`}>
                  <stat.icon className="h-5 w-5 text-white" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="truncate text-sm font-medium text-muted-foreground">
                      {stat.name}
                    </dt>
                    <dd>
                      <div className="text-xl font-semibold text-foreground">
                        {stat.value}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className={`bg-muted px-5 py-1.5 ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
              <div className="flex items-center text-xs">
                {stat.trend === 'up' ? (
                  <ArrowUpIcon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                ) : (
                  <ArrowDownIcon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                )}
                <span className="ml-1">{stat.change} from previous period</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* API Usage Chart */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.5 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">API Usage</h2>
          <div className="mt-2 h-64 rounded-md bg-muted/30 flex items-center justify-center">
            <p className="text-sm text-muted-foreground">Chart visualization will be implemented here</p>
          </div>
        </motion.div>

        {/* Service Performance */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.6 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">Service Performance</h2>
          <div className="mt-2 h-64 rounded-md bg-muted/30 flex items-center justify-center">
            <p className="text-sm text-muted-foreground">Chart visualization will be implemented here</p>
          </div>
        </motion.div>
      </div>

      {/* Recent Activity */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.7 }}
        className="rounded-lg bg-card p-6 shadow"
      >
        <h2 className="text-lg font-medium text-foreground">Recent Activity</h2>
        <div className="mt-6 flow-root">
          <ul className="-my-5 divide-y divide-border">
            {recentActivities.map((activity) => (
              <li key={activity.id} className="py-4">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                      <span className="text-xs font-medium text-primary">
                        {activity.type.substring(0, 2).toUpperCase()}
                      </span>
                    </span>
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-foreground">
                      {activity.details}
                    </p>
                    <p className="truncate text-sm text-muted-foreground">
                      {activity.type} · {activity.status}
                    </p>
                  </div>
                  <div className="flex-shrink-0 whitespace-nowrap text-sm text-muted-foreground">
                    {activity.timestamp}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <div className="mt-6">
          <a
            href="#"
            className="flex w-full items-center justify-center rounded-md bg-muted px-3 py-2 text-sm font-semibold text-foreground hover:bg-muted/80"
          >
            View all activity
          </a>
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard 