import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  ArrowDownIcon,
  ArrowUpIcon,
  CalendarIcon,
  ChartBarIcon,
  DocumentTextIcon,
  ServerIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

// Mock data for metrics
const metrics = [
  {
    id: 1,
    name: 'Total API Calls',
    value: '124,582',
    change: '+12.5%',
    trend: 'up',
    icon: ServerIcon
  },
  {
    id: 2,
    name: 'Avg. Response Time',
    value: '245ms',
    change: '-18.3%',
    trend: 'down',
    icon: ClockIcon
  },
  {
    id: 3,
    name: 'Documents Processed',
    value: '8,492',
    change: '+5.2%',
    trend: 'up',
    icon: DocumentTextIcon
  },
  {
    id: 4,
    name: 'Error Rate',
    value: '0.2%',
    change: '-0.1%',
    trend: 'down',
    icon: ChartBarIcon
  }
]

// Mock data for service usage
const serviceUsage = [
  { name: 'Text Generation', value: 45 },
  { name: 'Sentiment Analysis', value: 28 },
  { name: 'Embeddings', value: 17 },
  { name: 'RAG Workflows', value: 10 }
]

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d')

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-foreground">Analytics</h1>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <CalendarIcon className="h-5 w-5 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Time Range:</span>
          </div>
          
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

      {/* Metrics */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="overflow-hidden rounded-lg bg-card shadow"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0 rounded-md bg-primary/10 p-3">
                  <metric.icon className="h-5 w-5 text-primary" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="truncate text-sm font-medium text-muted-foreground">
                      {metric.name}
                    </dt>
                    <dd>
                      <div className="text-xl font-semibold text-foreground">
                        {metric.value}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className={`bg-muted px-5 py-1.5 ${metric.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
              <div className="flex items-center text-xs">
                {metric.trend === 'up' ? (
                  <ArrowUpIcon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                ) : (
                  <ArrowDownIcon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                )}
                <span className="ml-1">{metric.change} from previous period</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* API Calls Over Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.5 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">API Calls Over Time</h2>
          <div className="mt-2 h-64 rounded-md bg-muted/30 flex items-center justify-center">
            <p className="text-sm text-muted-foreground">Chart visualization will be implemented here</p>
          </div>
        </motion.div>

        {/* Service Usage Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.6 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">Service Usage Distribution</h2>
          <div className="mt-6">
            <div className="space-y-4">
              {serviceUsage.map((service) => (
                <div key={service.name} className="flex items-center">
                  <span className="text-sm font-medium text-foreground w-36">{service.name}</span>
                  <div className="flex-1">
                    <div className="h-2 w-full rounded-full bg-muted">
                      <div
                        className="h-2 rounded-full bg-primary"
                        style={{ width: `${service.value}%` }}
                      />
                    </div>
                  </div>
                  <span className="ml-4 text-sm font-medium text-foreground">{service.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Response Time Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.7 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">Response Time Distribution</h2>
          <div className="mt-2 h-64 rounded-md bg-muted/30 flex items-center justify-center">
            <p className="text-sm text-muted-foreground">Chart visualization will be implemented here</p>
          </div>
        </motion.div>

        {/* Error Rate Over Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.8 }}
          className="rounded-lg bg-card p-6 shadow"
        >
          <h2 className="text-lg font-medium text-foreground">Error Rate Over Time</h2>
          <div className="mt-2 h-64 rounded-md bg-muted/30 flex items-center justify-center">
            <p className="text-sm text-muted-foreground">Chart visualization will be implemented here</p>
          </div>
        </motion.div>
      </div>

      {/* Export buttons */}
      <div className="flex justify-end space-x-4">
        <button
          type="button"
          className="inline-flex items-center rounded-md bg-muted px-4 py-2 text-sm font-medium text-foreground hover:bg-muted/80 focus:outline-none"
        >
          Export CSV
        </button>
        <button
          type="button"
          className="inline-flex items-center rounded-md bg-muted px-4 py-2 text-sm font-medium text-foreground hover:bg-muted/80 focus:outline-none"
        >
          Export PDF
        </button>
      </div>
    </div>
  )
}

export default Analytics 