import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  TreePine, 
  Calendar, 
  MessageCircle, 
  Users, 
  TrendingUp,
  Leaf,
  Droplets,
  Sun,
  Cloud,
  Plus,
  Award,
  Target
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'

const Dashboard = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [dashboardData, setDashboardData] = useState({
    stats: {
      treesPlanted: 0,
      treesAlive: 0,
      carbonOffset: 0,
      communityRank: 0
    },
    recentActivities: [],
    upcomingTasks: [],
    weather: null,
    achievements: []
  })

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Real API calls to backend
      const [dashboardRes, weatherRes, statsRes] = await Promise.all([
        api.get('/dashboard/dashboard'),
        api.get('/dashboard/weather'),
        api.get('/dashboard/stats')
      ])

      const dashboard = dashboardRes.data
      const weather = weatherRes.data
      const stats = statsRes.data

      setDashboardData({
        stats: {
          treesPlanted: dashboard.user_stats.trees_planted || 0,
          treesAlive: Math.floor((dashboard.user_stats.trees_planted || 0) * 0.9), // 90% survival rate
          carbonOffset: Math.floor((dashboard.user_stats.trees_planted || 0) * 6.5), // ~6.5kg per tree
          communityRank: stats.community_rank || 0
        },
        recentActivities: dashboard.recent_activities.map(activity => ({
          id: activity.id,
          type: activity.activity_type,
          description: `${activity.activity_type.charAt(0).toUpperCase() + activity.activity_type.slice(1)} ${activity.trees_count} trees`,
          date: new Date(activity.activity_date).toLocaleDateString(),
          location: activity.location || 'Unknown'
        })),
        upcomingTasks: [
          { id: 1, task: 'Water newly planted seedlings', dueDate: new Date(Date.now() + 86400000).toLocaleDateString(), priority: 'high' },
          { id: 2, task: 'Check tree growth progress', dueDate: new Date(Date.now() + 2*86400000).toLocaleDateString(), priority: 'medium' },
          { id: 3, task: 'Community planting event', dueDate: new Date(Date.now() + 4*86400000).toLocaleDateString(), priority: 'low' }
        ],
        weather: {
          temperature: weather.current.temperature,
          condition: weather.current.condition,
          humidity: weather.current.humidity,
          rainfall: weather.planting_advice.recommendation
        },
        achievements: dashboard.achievements.map(ach => ({
          id: ach.id,
          title: ach.achievement.name,
          icon: TreePine, // Default icon, could be dynamic
          earned: true
        }))
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      // Fallback to mock data if API fails
      setDashboardData({
        stats: { treesPlanted: 0, treesAlive: 0, carbonOffset: 0, communityRank: 0 },
        recentActivities: [],
        upcomingTasks: [],
        weather: { temperature: 24, condition: 'Partly Cloudy', humidity: 65, rainfall: 'Light rain expected' },
        achievements: []
      })
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    {
      title: 'Log Tree Activity',
      description: 'Record planting, watering, or maintenance',
      icon: TreePine,
      color: 'bg-primary-600',
      action: () => console.log('Log activity')
    },
    {
      title: 'View Calendar',
      description: 'Check planting schedule and reminders',
      icon: Calendar,
      color: 'bg-secondary-600',
      link: '/calendar'
    },
    {
      title: 'Ask AI Expert',
      description: 'Get personalized tree care advice',
      icon: MessageCircle,
      color: 'bg-accent-600',
      link: '/chatbot'
    },
    {
      title: 'Join Community',
      description: 'Connect with other tree enthusiasts',
      icon: Users,
      color: 'bg-primary-700',
      link: '/community'
    }
  ]

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Welcome back, {user?.username}! 🌱
          </h1>
          <p className="text-gray-600">
            Here's your tree conservation impact and upcoming activities.
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Trees Planted</p>
                <p className="text-2xl font-bold text-primary-600">{dashboardData.stats.treesPlanted}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <TreePine className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Trees Alive</p>
                <p className="text-2xl font-bold text-secondary-600">{dashboardData.stats.treesAlive}</p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-full flex items-center justify-center">
                <Leaf className="w-6 h-6 text-secondary-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">CO₂ Offset (kg)</p>
                <p className="text-2xl font-bold text-accent-600">{dashboardData.stats.carbonOffset}</p>
              </div>
              <div className="w-12 h-12 bg-accent-100 rounded-full flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-accent-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Community Rank</p>
                <p className="text-2xl font-bold text-primary-700">#{dashboardData.stats.communityRank}</p>
              </div>
              <div className="w-12 h-12 bg-primary-200 rounded-full flex items-center justify-center">
                <Award className="w-6 h-6 text-primary-700" />
              </div>
            </div>
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <div key={action.title} className="card p-6 hover:scale-105 transition-transform cursor-pointer">
                {action.link ? (
                  <Link to={action.link} className="block">
                    <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center mb-3`}>
                      <action.icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-800 mb-1">{action.title}</h3>
                    <p className="text-sm text-gray-600">{action.description}</p>
                  </Link>
                ) : (
                  <div onClick={action.action}>
                    <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center mb-3`}>
                      <action.icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-800 mb-1">{action.title}</h3>
                    <p className="text-sm text-gray-600">{action.description}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Activities */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="lg:col-span-2"
          >
            <div className="card p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activities</h2>
              <div className="space-y-4">
                {dashboardData.recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-center space-x-4 p-3 bg-primary-50 rounded-lg">
                    <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                      <TreePine className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-800">{activity.description}</p>
                      <p className="text-sm text-gray-600">{activity.location} • {activity.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7 }}
            className="space-y-6"
          >
            {/* Weather Widget */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Today's Weather</h3>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-2xl font-bold text-gray-800">{dashboardData.weather?.temperature}°C</p>
                  <p className="text-sm text-gray-600">{dashboardData.weather?.condition}</p>
                </div>
                <Cloud className="w-8 h-8 text-gray-400" />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Humidity</span>
                  <span className="font-medium">{dashboardData.weather?.humidity}%</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Rainfall</span>
                  <span className="font-medium text-primary-600">{dashboardData.weather?.rainfall}</span>
                </div>
              </div>
            </div>

            {/* Upcoming Tasks */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Upcoming Tasks</h3>
              <div className="space-y-3">
                {dashboardData.upcomingTasks.map((task) => (
                  <div key={task.id} className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      task.priority === 'high' ? 'bg-red-500' :
                      task.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                    }`}></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800">{task.task}</p>
                      <p className="text-xs text-gray-600">{task.dueDate}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Achievements */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Achievements</h3>
              <div className="grid grid-cols-2 gap-3">
                {dashboardData.achievements.map((achievement) => (
                  <div
                    key={achievement.id}
                    className={`p-3 rounded-lg text-center ${
                      achievement.earned ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-400'
                    }`}
                  >
                    <achievement.icon className="w-6 h-6 mx-auto mb-1" />
                    <p className="text-xs font-medium">{achievement.title}</p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard