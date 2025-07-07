import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  DocumentTextIcon,
  PlusIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationCircleIcon,
  ArrowsRightLeftIcon,
  DocumentDuplicateIcon,
  TrashIcon
} from '@heroicons/react/24/outline'

// Mock data for RAG workflows
const workflows = [
  {
    id: 1,
    name: 'Customer Support Knowledge Base',
    description: 'RAG workflow for customer support queries using product documentation.',
    status: 'active',
    lastRun: '2 minutes ago',
    documents: 128,
    avgResponseTime: '450ms',
    successRate: '99.1%'
  },
  {
    id: 2,
    name: 'Financial Reports Analysis',
    description: 'RAG workflow for analyzing financial reports and extracting insights.',
    status: 'active',
    lastRun: '1 hour ago',
    documents: 56,
    avgResponseTime: '620ms',
    successRate: '98.7%'
  },
  {
    id: 3,
    name: 'Medical Research Assistant',
    description: 'RAG workflow for medical research papers and clinical studies.',
    status: 'inactive',
    lastRun: '3 days ago',
    documents: 215,
    avgResponseTime: '780ms',
    successRate: '97.5%'
  }
]

const RAGWorkflows = () => {
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [activeTab, setActiveTab] = useState('all')

  const handleRefresh = () => {
    setIsRefreshing(true)
    setTimeout(() => {
      setIsRefreshing(false)
    }, 1500)
  }

  const filteredWorkflows = activeTab === 'all' 
    ? workflows 
    : workflows.filter(workflow => 
        activeTab === 'active' ? workflow.status === 'active' : workflow.status === 'inactive'
      )

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-foreground">RAG Workflows</h1>
        
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
            New Workflow
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {['all', 'active', 'inactive'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium ${
                activeTab === tab
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-border hover:text-foreground'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </div>

      {/* Workflows list */}
      <div className="space-y-4">
        {filteredWorkflows.map((workflow, index) => (
          <motion.div
            key={workflow.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="overflow-hidden rounded-lg bg-card shadow"
          >
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <DocumentTextIcon className="h-8 w-8 text-primary" aria-hidden="true" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-foreground">{workflow.name}</h3>
                    <div className="mt-1 flex items-center">
                      {workflow.status === 'active' ? (
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
                      <span className="mx-2 text-muted-foreground">•</span>
                      <ClockIcon className="h-4 w-4 text-muted-foreground" />
                      <span className="ml-1 text-xs text-muted-foreground">Last run: {workflow.lastRun}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    type="button"
                    className="rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-foreground focus:outline-none"
                  >
                    <ArrowsRightLeftIcon className="h-5 w-5" />
                  </button>
                  <button
                    type="button"
                    className="rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-foreground focus:outline-none"
                  >
                    <DocumentDuplicateIcon className="h-5 w-5" />
                  </button>
                  <button
                    type="button"
                    className="rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-red-500 focus:outline-none"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
              
              <p className="mt-4 text-sm text-muted-foreground">
                {workflow.description}
              </p>
              
              <div className="mt-5 grid grid-cols-3 gap-4 border-t border-border pt-4">
                <div>
                  <p className="text-xs text-muted-foreground">Documents</p>
                  <p className="text-sm font-medium text-foreground">{workflow.documents}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Avg. Response</p>
                  <p className="text-sm font-medium text-foreground">{workflow.avgResponseTime}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Success Rate</p>
                  <p className="text-sm font-medium text-foreground">{workflow.successRate}</p>
                </div>
              </div>
            </div>
            
            <div className="border-t border-border bg-card px-6 py-3">
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  className="rounded-md bg-muted px-3 py-1.5 text-xs font-medium text-foreground hover:bg-muted/80 focus:outline-none"
                >
                  View Documents
                </button>
                <button
                  type="button"
                  className="rounded-md bg-muted px-3 py-1.5 text-xs font-medium text-foreground hover:bg-muted/80 focus:outline-none"
                >
                  Test Query
                </button>
                <button
                  type="button"
                  className="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground hover:bg-primary/90 focus:outline-none"
                >
                  Edit Workflow
                </button>
              </div>
            </div>
          </motion.div>
        ))}
        
        {/* Add new workflow card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: filteredWorkflows.length * 0.1 }}
          className="flex items-center justify-center rounded-lg border-2 border-dashed border-border bg-card/50 p-12 text-center hover:border-primary/50 hover:bg-card"
        >
          <button
            type="button"
            className="inline-flex flex-col items-center text-muted-foreground hover:text-primary"
          >
            <PlusIcon className="h-12 w-12" />
            <span className="mt-2 block text-sm font-medium">Create new workflow</span>
          </button>
        </motion.div>
      </div>
    </div>
  )
}

export default RAGWorkflows 