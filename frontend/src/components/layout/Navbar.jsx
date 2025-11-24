import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { 
  Menu, 
  X, 
  Home, 
  BarChart3, 
  Calendar, 
  MessageCircle, 
  Users, 
  User,
  LogOut,
  Mail
} from 'lucide-react'
import Logo from '../ui/Logo'
import NotificationDropdown from '../ui/NotificationDropdown'
import DirectMessagesModal from '../modals/DirectMessagesModal'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [showMessages, setShowMessages] = useState(false)
  const { user, logout, isAuthenticated } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const navItems = [
    { name: 'Home', path: '/', icon: Home, public: true, hideWhenAuthenticated: true },
    { name: 'Dashboard', path: '/dashboard', icon: BarChart3 },
    { name: 'Tree Calendar', path: '/calendar', icon: Calendar },
    { name: 'AI Expert', path: '/chatbot', icon: MessageCircle },
    { name: 'Community', path: '/community', icon: Users },
    { name: 'Analytics', path: '/analytics', icon: BarChart3, public: true },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-white shadow-lg border-b-2 border-primary-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/">
              <Logo size="medium" showText={true} />
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              if (!item.public && !isAuthenticated) return null
              if (item.hideWhenAuthenticated && isAuthenticated) return null
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive(item.path)
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                {/* Messages Button */}
                <button
                  onClick={() => setShowMessages(true)}
                  className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                  title="Messages"
                >
                  <Mail className="w-6 h-6" />
                </button>

                {/* Notifications */}
                <NotificationDropdown
                  isOpen={showNotifications}
                  onClose={() => setShowNotifications(false)}
                  onToggle={() => setShowNotifications(!showNotifications)}
                />

                <Link
                  to="/profile"
                  className="flex items-center space-x-2 text-gray-600 hover:text-primary-600"
                >
                  <User className="w-5 h-5" />
                  <span className="text-sm font-medium">{user?.username}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-gray-600 hover:text-red-600 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link
                  to="/login"
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-600 hover:text-primary-600 focus:outline-none"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-white border-t border-primary-100">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map((item) => {
              if (!item.public && !isAuthenticated) return null
              if (item.hideWhenAuthenticated && isAuthenticated) return null
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium ${
                    isActive(item.path)
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              )
            })}

            {isAuthenticated ? (
              <div className="border-t border-primary-100 pt-4 mt-4">
                <Link
                  to="/profile"
                  onClick={() => setIsOpen(false)}
                  className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-primary-600"
                >
                  <User className="w-5 h-5" />
                  <span>Profile ({user?.username})</span>
                </Link>
                <button
                  onClick={() => {
                    handleLogout()
                    setIsOpen(false)
                  }}
                  className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-red-600 w-full text-left"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="border-t border-primary-100 pt-4 mt-4 space-y-2">
                <Link
                  to="/login"
                  onClick={() => setIsOpen(false)}
                  className="block px-3 py-2 text-primary-600 font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  onClick={() => setIsOpen(false)}
                  className="block px-3 py-2 bg-primary-600 text-white rounded-md font-medium"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Direct Messages Modal */}
      <DirectMessagesModal
        isOpen={showMessages}
        onClose={() => setShowMessages(false)}
      />
    </nav>
  )
}

export default Navbar