import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

const NotFound = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-4 text-center">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="mb-8 text-center">
          <div className="mx-auto h-24 w-24 rounded-full bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
            <span className="text-4xl font-bold text-primary">404</span>
          </div>
        </div>

        <h1 className="mb-4 text-3xl font-bold text-foreground md:text-4xl">Page not found</h1>
        
        <p className="mb-8 text-lg text-muted-foreground">
          Sorry, we couldn't find the page you're looking for.
        </p>
        
        <div className="flex justify-center">
          <Link
            to="/"
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          >
            Go back home
          </Link>
        </div>
      </motion.div>
    </div>
  )
}

export default NotFound 