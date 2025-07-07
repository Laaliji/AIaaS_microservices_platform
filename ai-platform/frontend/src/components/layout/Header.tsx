import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { 
  Bars3Icon, 
  BellIcon, 
  SunIcon, 
  MoonIcon, 
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline'

interface HeaderProps {
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  toggleTheme: () => void
  theme: 'light' | 'dark'
}

const Header = ({ 
  sidebarOpen, 
  setSidebarOpen, 
  toggleTheme,
  theme 
}: HeaderProps) => {
  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/95 backdrop-blur">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Left: Hamburger button */}
          <div className="flex lg:hidden">
            <button
              className="text-muted-foreground hover:text-foreground"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <span className="sr-only">Open sidebar</span>
              <Bars3Icon className="h-6 w-6" />
            </button>
          </div>
          
          {/* Right: Header items */}
          <div className="flex items-center space-x-3 md:ml-auto">
            {/* Theme toggle */}
            <button
              className="rounded-full p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground focus:outline-none"
              onClick={toggleTheme}
            >
              {theme === 'dark' ? (
                <SunIcon className="h-5 w-5" />
              ) : (
                <MoonIcon className="h-5 w-5" />
              )}
              <span className="sr-only">Toggle theme</span>
            </button>
            
            {/* Notifications */}
            <button className="rounded-full p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground focus:outline-none">
              <span className="sr-only">View notifications</span>
              <BellIcon className="h-5 w-5" />
            </button>
            
            {/* User menu */}
            <Menu as="div" className="relative">
              <Menu.Button className="flex rounded-full text-sm focus:outline-none">
                <span className="sr-only">Open user menu</span>
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <UserCircleIcon className="h-6 w-6" />
                </div>
              </Menu.Button>
              
              <Transition
                as={Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
              >
                <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-card py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <div className="border-b border-border px-4 py-2">
                    <p className="text-sm font-medium text-foreground">Admin User</p>
                    <p className="text-xs text-muted-foreground">admin@example.com</p>
                  </div>
                  
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={`${
                          active ? 'bg-muted' : ''
                        } flex items-center px-4 py-2 text-sm text-foreground`}
                      >
                        <Cog6ToothIcon className="mr-3 h-5 w-5 text-muted-foreground" />
                        Account settings
                      </a>
                    )}
                  </Menu.Item>
                  
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={`${
                          active ? 'bg-muted' : ''
                        } flex items-center px-4 py-2 text-sm text-foreground`}
                      >
                        <ArrowRightOnRectangleIcon className="mr-3 h-5 w-5 text-muted-foreground" />
                        Sign out
                      </a>
                    )}
                  </Menu.Item>
                </Menu.Items>
              </Transition>
            </Menu>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header 