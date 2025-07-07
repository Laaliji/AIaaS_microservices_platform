import { useState } from 'react'
import { motion } from 'framer-motion'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general')
  const [apiKey, setApiKey] = useState('sk-1234567890abcdefghijklmnopqrstuvwxyz')
  const [apiKeyVisible, setApiKeyVisible] = useState(false)
  const [rateLimitEnabled, setRateLimitEnabled] = useState(true)
  const [rateLimit, setRateLimit] = useState(100)
  const [notificationsEnabled, setNotificationsEnabled] = useState(true)
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [slackNotifications, setSlackNotifications] = useState(false)
  const [slackWebhook, setSlackWebhook] = useState('')
  const [loggingLevel, setLoggingLevel] = useState('info')

  const tabs = [
    { id: 'general', name: 'General' },
    { id: 'api', name: 'API Keys' },
    { id: 'security', name: 'Security' },
    { id: 'notifications', name: 'Notifications' },
    { id: 'logs', name: 'Logs & Monitoring' },
    { id: 'advanced', name: 'Advanced' },
  ]

  const handleSaveSettings = () => {
    // Mock save functionality
    console.log('Settings saved')
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-foreground">General Settings</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Basic configuration options for your AIaaS Platform.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="platform-name" className="block text-sm font-medium text-foreground">
                  Platform Name
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    name="platform-name"
                    id="platform-name"
                    className="block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    defaultValue="AIaaS Platform"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-foreground">
                  Description
                </label>
                <div className="mt-1">
                  <textarea
                    id="description"
                    name="description"
                    rows={3}
                    className="block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    defaultValue="AI-as-a-Service Microservices Platform with RAG capabilities"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="timezone" className="block text-sm font-medium text-foreground">
                  Timezone
                </label>
                <select
                  id="timezone"
                  name="timezone"
                  className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                  defaultValue="UTC"
                >
                  <option>UTC</option>
                  <option>America/New_York</option>
                  <option>Europe/London</option>
                  <option>Asia/Tokyo</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="debug-mode"
                    name="debug-mode"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                  />
                  <label htmlFor="debug-mode" className="ml-2 block text-sm text-foreground">
                    Enable Debug Mode
                  </label>
                </div>
              </div>
            </div>
          </div>
        )
      
      case 'api':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-foreground">API Keys</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Manage API keys for authentication with the platform.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="api-key" className="block text-sm font-medium text-foreground">
                  API Key
                </label>
                <div className="mt-1 flex rounded-md shadow-sm">
                  <input
                    type={apiKeyVisible ? 'text' : 'password'}
                    name="api-key"
                    id="api-key"
                    className="block w-full rounded-l-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    value={apiKey}
                    readOnly
                  />
                  <button
                    type="button"
                    className="inline-flex items-center rounded-r-md border border-l-0 border-input bg-muted px-3 py-2 text-sm font-medium text-foreground hover:bg-muted/80 focus:outline-none"
                    onClick={() => setApiKeyVisible(!apiKeyVisible)}
                  >
                    {apiKeyVisible ? 'Hide' : 'Show'}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="rate-limit"
                    name="rate-limit"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                    checked={rateLimitEnabled}
                    onChange={(e) => setRateLimitEnabled(e.target.checked)}
                  />
                  <label htmlFor="rate-limit" className="ml-2 block text-sm text-foreground">
                    Enable Rate Limiting
                  </label>
                </div>
              </div>

              {rateLimitEnabled && (
                <div>
                  <label htmlFor="rate-limit-value" className="block text-sm font-medium text-foreground">
                    Requests per minute
                  </label>
                  <div className="mt-1">
                    <input
                      type="number"
                      name="rate-limit-value"
                      id="rate-limit-value"
                      className="block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                      value={rateLimit}
                      onChange={(e) => setRateLimit(parseInt(e.target.value))}
                    />
                  </div>
                </div>
              )}

              <div className="pt-4">
                <button
                  type="button"
                  className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                >
                  Generate New API Key
                </button>
              </div>
            </div>
          </div>
        )
      
      case 'notifications':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-foreground">Notification Settings</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Configure how you want to receive notifications from the platform.
              </p>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="enable-notifications"
                    name="enable-notifications"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                    checked={notificationsEnabled}
                    onChange={(e) => setNotificationsEnabled(e.target.checked)}
                  />
                  <label htmlFor="enable-notifications" className="ml-2 block text-sm text-foreground">
                    Enable Notifications
                  </label>
                </div>
              </div>

              {notificationsEnabled && (
                <div className="space-y-4 pl-6">
                  <div className="flex items-center">
                    <input
                      id="email-notifications"
                      name="email-notifications"
                      type="checkbox"
                      className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      checked={emailNotifications}
                      onChange={(e) => setEmailNotifications(e.target.checked)}
                    />
                    <label htmlFor="email-notifications" className="ml-2 block text-sm text-foreground">
                      Email Notifications
                    </label>
                  </div>

                  <div className="flex items-center">
                    <input
                      id="slack-notifications"
                      name="slack-notifications"
                      type="checkbox"
                      className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      checked={slackNotifications}
                      onChange={(e) => setSlackNotifications(e.target.checked)}
                    />
                    <label htmlFor="slack-notifications" className="ml-2 block text-sm text-foreground">
                      Slack Notifications
                    </label>
                  </div>

                  {slackNotifications && (
                    <div>
                      <label htmlFor="slack-webhook" className="block text-sm font-medium text-foreground">
                        Slack Webhook URL
                      </label>
                      <div className="mt-1">
                        <input
                          type="text"
                          name="slack-webhook"
                          id="slack-webhook"
                          className="block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                          value={slackWebhook}
                          onChange={(e) => setSlackWebhook(e.target.value)}
                          placeholder="https://hooks.slack.com/services/..."
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )
      
      case 'logs':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-foreground">Logs & Monitoring</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Configure logging and monitoring settings.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="logging-level" className="block text-sm font-medium text-foreground">
                  Logging Level
                </label>
                <select
                  id="logging-level"
                  name="logging-level"
                  className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-foreground shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                  value={loggingLevel}
                  onChange={(e) => setLoggingLevel(e.target.value)}
                >
                  <option value="debug">Debug</option>
                  <option value="info">Info</option>
                  <option value="warning">Warning</option>
                  <option value="error">Error</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="request-logging"
                    name="request-logging"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                    defaultChecked
                  />
                  <label htmlFor="request-logging" className="ml-2 block text-sm text-foreground">
                    Log API Requests
                  </label>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="response-logging"
                    name="response-logging"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                    defaultChecked
                  />
                  <label htmlFor="response-logging" className="ml-2 block text-sm text-foreground">
                    Log API Responses
                  </label>
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  className="inline-flex items-center rounded-md bg-muted px-4 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted/80 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                >
                  View Logs
                </button>
              </div>
            </div>
          </div>
        )
      
      default:
        return (
          <div className="text-center py-8">
            <p className="text-muted-foreground">Select a tab to view settings</p>
          </div>
        )
    }
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-foreground">Settings</h1>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Tabs */}
        <div className="w-full lg:w-64 flex-shrink-0">
          <nav className="space-y-1" aria-label="Settings">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  activeTab === tab.id
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="flex-1"
        >
          <div className="rounded-lg bg-card p-6 shadow">
            {renderTabContent()}
          </div>

          <div className="mt-6 flex justify-end space-x-4">
            <button
              type="button"
              className="inline-flex items-center rounded-md bg-muted px-4 py-2 text-sm font-medium text-foreground hover:bg-muted/80 focus:outline-none"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSaveSettings}
              className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            >
              Save Settings
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Settings 