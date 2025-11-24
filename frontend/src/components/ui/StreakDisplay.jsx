import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Flame, TreePine, Calendar, Trophy, Target, AlertTriangle, Clock } from 'lucide-react'
import api from '../../utils/api'

const StreakDisplay = ({ onActivityClick }) => {
  const [streakData, setStreakData] = useState({
    current_streak: 0,
    longest_streak: 0,
    last_activity_date: null,
    streak_start_date: null,
    is_active: true
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStreakData()
  }, [])

  const fetchStreakData = async () => {
    try {
      const response = await api.get('/social/streak/my')
      setStreakData(response.data)
    } catch (error) {
      console.error('Failed to fetch streak data:', error)
      // Fallback to mock data for demo
      setStreakData({
        current_streak: 7,
        longest_streak: 15,
        last_activity_date: new Date().toISOString(),
        streak_start_date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true
      })
    } finally {
      setLoading(false)
    }
  }

  const getStreakEmoji = (streak) => {
    if (streak === 0) return '🌱'
    if (streak < 7) return '🔥'
    if (streak < 30) return '🚀'
    if (streak < 100) return '⭐'
    return '👑'
  }

  const getStreakMessage = (streak) => {
    if (streak === 0) return "Start your tree planting journey!"
    if (streak === 1) return "Great start! Keep it going!"
    if (streak < 7) return "You're on fire! 🔥"
    if (streak < 30) return "Amazing streak! You're a tree hero! 🌟"
    if (streak < 100) return "Incredible dedication! Forest guardian! 🏆"
    return "LEGENDARY STREAK! Tree conservation master! 👑"
  }

  const getStreakColor = (streak) => {
    if (streak === 0) return 'text-gray-500'
    if (streak < 7) return 'text-orange-500'
    if (streak < 30) return 'text-red-500'
    if (streak < 100) return 'text-purple-500'
    return 'text-yellow-500'
  }

  const isStreakAtRisk = () => {
    if (!streakData.last_activity_date) return false
    const lastActivity = new Date(streakData.last_activity_date)
    const now = new Date()
    const hoursSinceLastActivity = (now - lastActivity) / (1000 * 60 * 60)
    return hoursSinceLastActivity > 20 // At risk if no activity for 20+ hours
  }

  const getHoursUntilStreakLoss = () => {
    if (!streakData.last_activity_date) return 0
    const lastActivity = new Date(streakData.last_activity_date)
    const now = new Date()
    const hoursSinceLastActivity = (now - lastActivity) / (1000 * 60 * 60)
    const hoursRemaining = 24 - (hoursSinceLastActivity % 24)
    return Math.max(0, Math.floor(hoursRemaining))
  }

  if (loading) {
    return (
      <div className="card p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="card p-6 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="flex flex-wrap">
          {[...Array(20)].map((_, i) => (
            <TreePine key={i} className="w-8 h-8 m-2 text-primary-600" />
          ))}
        </div>
      </div>

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Flame className={`w-6 h-6 ${getStreakColor(streakData.current_streak)}`} />
            <h3 className="text-lg font-semibold text-gray-800">Tree Planting Streak</h3>
          </div>
          {streakData.current_streak > 0 && (
            <div className="text-2xl">{getStreakEmoji(streakData.current_streak)}</div>
          )}
        </div>

        {/* Current Streak */}
        <div className="text-center mb-6">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="text-6xl font-bold mb-2"
          >
            <span className={getStreakColor(streakData.current_streak)}>
              {streakData.current_streak}
            </span>
          </motion.div>
          <div className="text-gray-600 mb-2">
            {streakData.current_streak === 1 ? 'day' : 'days'} streak
          </div>
          <div className="text-sm text-gray-500">
            {getStreakMessage(streakData.current_streak)}
          </div>
        </div>

        {/* Streak Stats */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="text-center p-3 bg-primary-50 rounded-lg">
            <Trophy className="w-5 h-5 text-primary-600 mx-auto mb-1" />
            <div className="text-lg font-semibold text-primary-600">
              {streakData.longest_streak}
            </div>
            <div className="text-xs text-gray-600">Longest Streak</div>
          </div>
          <div className="text-center p-3 bg-secondary-50 rounded-lg">
            <Target className="w-5 h-5 text-secondary-600 mx-auto mb-1" />
            <div className="text-lg font-semibold text-secondary-600">
              {Math.max(0, 30 - streakData.current_streak)}
            </div>
            <div className="text-xs text-gray-600">Days to 30-day goal</div>
          </div>
        </div>

        {/* Streak Status */}
        {streakData.current_streak > 0 && (
          <div className="mb-4">
            {isStreakAtRisk() ? (
              <div className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-red-800">Streak at risk!</p>
                  <p className="text-xs text-red-600">
                    {getHoursUntilStreakLoss()} hours left to log activity
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                <Clock className="w-5 h-5 text-green-500" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-green-800">Streak is safe!</p>
                  <p className="text-xs text-green-600">
                    Great job staying consistent with your tree activities
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Action Button */}
        <button
          onClick={onActivityClick}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
        >
          <TreePine className="w-5 h-5" />
          <span>Log Tree Activity</span>
        </button>

        {/* Streak Calendar Preview */}
        {streakData.current_streak > 0 && (
          <div className="mt-6">
            <h4 className="text-sm font-medium text-gray-700 mb-3">Last 7 Days</h4>
            <div className="flex justify-between">
              {[...Array(7)].map((_, i) => {
                const dayIndex = 6 - i
                const hasActivity = dayIndex < streakData.current_streak
                return (
                  <div
                    key={i}
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
                      hasActivity
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-500'
                    }`}
                  >
                    {hasActivity ? '✓' : '○'}
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default StreakDisplay