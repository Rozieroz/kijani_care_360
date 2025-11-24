import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Bell, 
  BellRing,
  TreePine, 
  Users, 
  Heart,
  MessageSquare,
  Award,
  Calendar,
  X,
  Check,
  CheckCheck,
  Trash2
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const NotificationDropdown = ({ isOpen, onClose, onToggle }) => {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    fetchNotifications()
    // Set up polling for new notifications
    const interval = setInterval(fetchNotifications, 30000) // Poll every 30 seconds
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen, onClose])

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/notifications')
      setNotifications(response.data.notifications || [])
      setUnreadCount(response.data.unread_count || 0)
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
      // Fallback to mock data
      setNotifications([
        {
          id: 1,
          type: 'streak_milestone',
          title: 'Streak Milestone! 🔥',
          message: 'Congratulations! You\'ve reached a 7-day planting streak!',
          timestamp: '2 minutes ago',
          is_read: false,
          icon: 'flame',
          action_url: '/profile'
        },
        {
          id: 2,
          type: 'group_invite',
          title: 'Group Invitation',
          message: 'Sarah Wanjiku invited you to join "Nairobi Tree Warriors" streak group',
          timestamp: '1 hour ago',
          is_read: false,
          icon: 'users',
          action_url: '/community'
        },
        {
          id: 3,
          type: 'post_like',
          title: 'Post Liked ❤️',
          message: 'John Kimani and 5 others liked your tree planting post',
          timestamp: '3 hours ago',
          is_read: true,
          icon: 'heart',
          action_url: '/community'
        },
        {
          id: 4,
          type: 'comment',
          title: 'New Comment',
          message: 'Grace Akinyi commented on your post: "Amazing work! Keep it up!"',
          timestamp: '5 hours ago',
          is_read: true,
          icon: 'message',
          action_url: '/community'
        },
        {
          id: 5,
          type: 'achievement',
          title: 'Achievement Unlocked! 🏆',
          message: 'You earned the "Green Thumb" badge for maintaining 90% tree survival rate',
          timestamp: '1 day ago',
          is_read: true,
          icon: 'award',
          action_url: '/profile'
        },
        {
          id: 6,
          type: 'event_reminder',
          title: 'Event Reminder 📅',
          message: 'Tree planting event at Karura Forest starts in 2 hours',
          timestamp: '1 day ago',
          is_read: true,
          icon: 'calendar',
          action_url: '/community'
        }
      ])
      setUnreadCount(2)
    }
  }

  const markAsRead = async (notificationId) => {
    try {
      await api.put(`/notifications/${notificationId}/read`)
      setNotifications(prev => prev.map(notif => 
        notif.id === notificationId ? { ...notif, is_read: true } : notif
      ))
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
      // Optimistic update
      setNotifications(prev => prev.map(notif => 
        notif.id === notificationId ? { ...notif, is_read: true } : notif
      ))
      setUnreadCount(prev => Math.max(0, prev - 1))
    }
  }

  const markAllAsRead = async () => {
    try {
      await api.put('/notifications/mark-all-read')
      setNotifications(prev => prev.map(notif => ({ ...notif, is_read: true })))
      setUnreadCount(0)
      toast.success('All notifications marked as read')
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error)
      // Optimistic update
      setNotifications(prev => prev.map(notif => ({ ...notif, is_read: true })))
      setUnreadCount(0)
    }
  }

  const deleteNotification = async (notificationId) => {
    try {
      await api.delete(`/notifications/${notificationId}`)
      setNotifications(prev => prev.filter(notif => notif.id !== notificationId))
      const deletedNotif = notifications.find(n => n.id === notificationId)
      if (deletedNotif && !deletedNotif.is_read) {
        setUnreadCount(prev => Math.max(0, prev - 1))
      }
    } catch (error) {
      console.error('Failed to delete notification:', error)
      // Optimistic update
      setNotifications(prev => prev.filter(notif => notif.id !== notificationId))
    }
  }

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'streak_milestone':
      case 'flame':
        return <TreePine className="w-5 h-5 text-orange-500" />
      case 'group_invite':
      case 'users':
        return <Users className="w-5 h-5 text-blue-500" />
      case 'post_like':
      case 'heart':
        return <Heart className="w-5 h-5 text-red-500" />
      case 'comment':
      case 'message':
        return <MessageSquare className="w-5 h-5 text-green-500" />
      case 'achievement':
      case 'award':
        return <Award className="w-5 h-5 text-yellow-500" />
      case 'event_reminder':
      case 'calendar':
        return <Calendar className="w-5 h-5 text-purple-500" />
      default:
        return <Bell className="w-5 h-5 text-gray-500" />
    }
  }

  const handleNotificationClick = (notification) => {
    if (!notification.is_read) {
      markAsRead(notification.id)
    }
    // Handle navigation to action_url if needed
    onClose()
  }

  return (
    <div className="relative">
      {/* Notification Bell Button */}
      <button
        onClick={onToggle}
        className="relative p-2 text-gray-600 hover:text-primary-600 transition-colors"
      >
        {unreadCount > 0 ? (
          <BellRing className="w-6 h-6" />
        ) : (
          <Bell className="w-6 h-6" />
        )}
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            ref={dropdownRef}
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-xl border border-gray-200 z-50"
          >
            {/* Header */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-800">Notifications</h3>
                <div className="flex items-center space-x-2">
                  {unreadCount > 0 && (
                    <button
                      onClick={markAllAsRead}
                      className="text-sm text-primary-600 hover:text-primary-700 transition-colors"
                    >
                      Mark all read
                    </button>
                  )}
                  <button
                    onClick={onClose}
                    className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>
              {unreadCount > 0 && (
                <p className="text-sm text-gray-600 mt-1">
                  You have {unreadCount} unread notification{unreadCount !== 1 ? 's' : ''}
                </p>
              )}
            </div>

            {/* Notifications List */}
            <div className="max-h-96 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="p-8 text-center">
                  <Bell className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500">No notifications yet</p>
                  <p className="text-sm text-gray-400 mt-1">
                    We'll notify you when something happens
                  </p>
                </div>
              ) : (
                notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer ${
                      !notification.is_read ? 'bg-primary-50' : ''
                    }`}
                    onClick={() => handleNotificationClick(notification)}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 mt-1">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className={`text-sm font-medium ${
                              !notification.is_read ? 'text-gray-900' : 'text-gray-700'
                            }`}>
                              {notification.title}
                            </p>
                            <p className="text-sm text-gray-600 mt-1">
                              {notification.message}
                            </p>
                            <p className="text-xs text-gray-500 mt-2">
                              {notification.timestamp}
                            </p>
                          </div>
                          <div className="flex items-center space-x-1 ml-2">
                            {!notification.is_read && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation()
                                  markAsRead(notification.id)
                                }}
                                className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                                title="Mark as read"
                              >
                                <Check className="w-3 h-3 text-gray-500" />
                              </button>
                            )}
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                deleteNotification(notification.id)
                              }}
                              className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                              title="Delete notification"
                            >
                              <Trash2 className="w-3 h-3 text-gray-500" />
                            </button>
                          </div>
                        </div>
                      </div>
                      {!notification.is_read && (
                        <div className="w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            {notifications.length > 0 && (
              <div className="p-3 border-t border-gray-200 text-center">
                <button className="text-sm text-primary-600 hover:text-primary-700 transition-colors">
                  View all notifications
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default NotificationDropdown