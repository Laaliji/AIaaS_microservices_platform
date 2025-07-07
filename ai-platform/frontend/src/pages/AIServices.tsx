import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  ServerIcon,
  ChartBarIcon,
  DocumentTextIcon,
  PlusIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline'

// Mock data for AI services
const services = [
  {
    id: 1,
    name: 'Text Generation',
    description: 'Generate human-like text based on prompts using distilgpt2.',
    status: 'active',
    endpoint: '/api/generate',
    icon: DocumentTextIcon,
    stats: {
      requests: '5,248',
      avgResponseTime: '320ms',
      errorRate: '0.2%'
    }
  },
  {
    id: 2,
    name: 'Sentiment Analysis',
    description: 'Analyze text for sentiment using distilbert model.',
    status: 'active',
    endpoint: '/api/analyze-sentiment',
    icon: ChartBarIcon,
    stats: {
      requests: '2,187',
      avgResponseTime: '145ms',
      errorRate: '0.1%'
    }
  },
  {
    id: 3,
    name: 'Embeddings',
    description: 'Generate text embeddings using all-MiniLM-L6-v2 model.',
    status: 'active',
    endpoint: '/api/embeddings',
    icon: ServerIcon,
    stats: {
      requests: '814',
      avgResponseTime: '95ms',
      errorRate: '0.0%'
    }
  }
]

const AIServices = () => {
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = () => {
    setIsRefreshing(true)
    setTimeout(() => {
      setIsRefreshing(false)
    }, 1500)
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-foreground">AI Services</h1>
        
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleRefresh}
            className="inline-flex items-center rounded-md bg-muted px-3 py-2 text-sm font-medium text-foreground hover:bg-muted/80 focus:outline-none"
          >
            <ArrowPathIcon 
              className={`mr-2 h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} 
            />
            Refresh
          </button>
          
          <button
            type="button"
            className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 focus:outline-none"
          >
            <PlusIcon className="mr-2 h-4 w-4" />
            Add Service
          </button>
        </div>
      </div>

      {/* Services grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {services.map((service, index) => (
          <motion.div
            key={service.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="overflow-hidden rounded-lg bg-card shadow"
          >
            <div className="px-6 py-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <service.icon className="h-8 w-8 text-primary" aria-hidden="true" />
                </div>
                <div className="ml-4 flex-1">
                  <h3 className="text-lg font-medium text-foreground">{service.name}</h3>
                  <div className="flex items-center mt-1">
                    {service.status === 'active' ? (
                      <>
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                        <span className="ml-1 text-xs font-medium text-green-500">Active</span>
                      </>
                    ) : (
                      <>
                        <ExclamationCircleIcon className="h-4 w-4 text-amber-500" />
                        <span className="ml-1 text-xs font-medium text-amber-500">Inactive</span>
                      </>
                    )}
                  </div>
                </div>
              </div>
              
              <p className="mt-4 text-sm text-muted-foreground">
                {service.description}
              </p>
              
              <div className="mt-5 grid grid-cols-3 gap-4 border-t border-border pt-4">
                <div>
                  <p className="text-xs text-muted-foreground">Requests</p>
                  <p className="text-sm font-medium text-foreground">{service.stats.requests}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Avg. Response</p>
                  <p className="text-sm font-medium text-foreground">{service.stats.avgResponseTime}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Error Rate</p>
                  <p className="text-sm font-medium text-foreground">{service.stats.errorRate}</p>
                </div>
              </div>
              
              <div className="mt-5">
                <div className="rounded-md bg-muted px-3 py-1.5 text-xs font-mono text-muted-foreground">
                  {service.endpoint}
                </div>
              </div>
            </div>
            
            <div className="border-t border-border bg-card px-6 py-3">
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  className="rounded px-2 py-1 text-xs font-medium text-foreground hover:bg-muted focus:outline-none"
                >
                  View Docs
                </button>
                <button
                  type="button"
                  className="rounded px-2 py-1 text-xs font-medium text-foreground hover:bg-muted focus:outline-none"
                >
                  Test
                </button>
                <button
                  type="button"
                  className="rounded px-2 py-1 text-xs font-medium text-foreground hover:bg-muted focus:outline-none"
                >
                  Settings
                </button>
              </div>
            </div>
          </motion.div>
        ))}
        
        {/* Add new service card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: services.length * 0.1 }}
          className="flex items-center justify-center rounded-lg border-2 border-dashed border-border bg-card/50 p-12 text-center hover:border-primary/50 hover:bg-card"
        >
          <button
            type="button"
            className="inline-flex flex-col items-center text-muted-foreground hover:text-primary"
          >
            <PlusIcon className="h-12 w-12" />
            <span className="mt-2 block text-sm font-medium">Add new service</span>
          </button>
        </motion.div>
      </div>
    </div>
  )
}

export default AIServices 