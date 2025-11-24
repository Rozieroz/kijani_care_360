import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Flame, 
  TreePine, 
  Users, 
  Trophy, 
  Target, 
  AlertTriangle, 
  Clock,
  Plus,
  UserPlus,
  Crown,
  Star
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const CollaborativeStreak = ({ onActivityClick, onInviteClick }) => {
  const [streakData, setStreakData] = useState({
    group_streak: 0,
    group_members: [],
    group_name: '',
    individual_contribution: 0,
    group_goal: 30,
    last_group_activity: null,
    is_group_active: false,
    group_id: null
  })
  const [loading, setLoading] = useState(true)
  const [showCreateGroup, setShowCreateGroup] = useState(false)

  useEffect(() => {
    fetchCollaborativeStreakData()
  }, [])

  const fetchCollaborativeStreakData = async () => {
    try {
      const response = await api.get('/social/streak/collaborative')
      setStreakData(response.data)
    } catch (error) {
      console.error('Failed to fetch collaborative streak data:', error)
      // Fallback to mock data for demo
      setStreakData({
        group_streak: 12,
        group_members: [
          { id: 1, name: 'You', avatar: '👤', contribution: 5, last_activity: '2 hours ago' },
          { id: 2, name: 'Sarah K.', avatar: '👩🏾', contribution: 4, last_activity: '4 hours ago' },
          { id: 3, name: 'John M.', avatar: '👨🏽', contribution: 3, last_activity: '1 day ago' }
        ],
        group_name: 'Nairobi Tree Warriors',
        individual_contribution: 5,
        group_goal: 30,
        last_group_activity: new Date().toISOString(),
        is_group_active: true,
        group_id: 1
      })
    } finally {
      setLoading(false)
    }
  }

  const createStreakGroup = async (groupName) => {
    try {
      const response = await api.post('/social/streak/groups', { name: groupName })
      setStreakData(response.data)
      toast.success('🌱 Streak group created! Invite friends to join!')
      setShowCreateGroup(false)
    } catch (error) {
      console.error('Failed to create streak group:', error)
      toast.error('Failed to create group. Please try again.')
    }
  }

  const getStreakEmoji = (streak) => {
    if (streak === 0) return '🌱'
    if (streak < 7) return '🔥'
    if (streak < 30) return '🚀'
    if (streak < 100) return '⭐'
    return '👑'
  }

  const getStreakMessage = (streak, memberCount) => {
    if (streak === 0) return "Start your collaborative journey!"
    if (streak === 1) return `Great start with ${memberCount} members!`
    if (streak < 7) return `${memberCount} members keeping the fire alive! 🔥`
    if (streak < 30) return `Amazing team streak! ${memberCount} tree heroes! 🌟`
    if (streak < 100) return `Incredible group dedication! Forest guardians! 🏆`
    return `LEGENDARY TEAM STREAK! ${memberCount} conservation masters! 👑`
  }

  const getStreakColor = (streak) => {
    if (streak === 0) return 'text-gray-500'
    if (streak < 7) return 'text-orange-500'
    if (streak < 30) return 'text-red-500'
    if (streak < 100) return 'text-purple-500'
    return 'text-yellow-500'
  }

  const isGroupStreakAtRisk = () => {
    if (!streakData.last_group_activity) return false
    const lastActivity = new Date(streakData.last_group_activity)
    const now = new Date()
    const hoursSinceLastActivity = (now - lastActivity) / (1000 * 60 * 60)
    return hoursSinceLastActivity > 20
  }

  const getMostActiveMembers = () => {
    return streakData.group_members
      .sort((a, b) => b.contribution - a.contribution)
      .slice(0, 3)
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

  // No group yet - show create group option
  if (!streakData.group_id) {
    return (
      <div className="card p-6 relative overflow-hidden">
        <div className="text-center">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="w-8 h-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Start a Collaborative Streak</h3>
          <p className="text-gray-600 mb-6">
            Team up with friends to maintain streaks together and achieve more!
          </p>
          
          {showCreateGroup ? (
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Enter group name (e.g., Nairobi Tree Warriors)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && e.target.value.trim()) {
                    createStreakGroup(e.target.value.trim())
                  }
                }}
              />
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowCreateGroup(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={(e) => {
                    const input = e.target.parentElement.previousElementSibling
                    if (input.value.trim()) {
                      createStreakGroup(input.value.trim())
                    }
                  }}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Create Group
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setShowCreateGroup(true)}
              className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg transition-colors flex items-center space-x-2 mx-auto"
            >
              <Plus className="w-5 h-5" />
              <span>Create Streak Group</span>
            </button>
          )}
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
            <Users key={i} className="w-8 h-8 m-2 text-primary-600" />
          ))}
        </div>
      </div>

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Flame className={`w-6 h-6 ${getStreakColor(streakData.group_streak)}`} />
            <div>
              <h3 className="text-lg font-semibold text-gray-800">{streakData.group_name}</h3>
              <p className="text-sm text-gray-600">{streakData.group_members.length} members</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="text-2xl">{getStreakEmoji(streakData.group_streak)}</div>
            <button
              onClick={onInviteClick}
              className="p-2 bg-primary-100 hover:bg-primary-200 rounded-full transition-colors"
            >
              <UserPlus className="w-4 h-4 text-primary-600" />
            </button>
          </div>
        </div>

        {/* Group Streak */}
        <div className="text-center mb-6">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="text-5xl font-bold mb-2"
          >
            <span className={getStreakColor(streakData.group_streak)}>
              {streakData.group_streak}
            </span>
          </motion.div>
          <div className="text-gray-600 mb-2">
            {streakData.group_streak === 1 ? 'day' : 'days'} group streak
          </div>
          <div className="text-sm text-gray-500">
            {getStreakMessage(streakData.group_streak, streakData.group_members.length)}
          </div>
        </div>

        {/* Group Stats */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="text-center p-3 bg-primary-50 rounded-lg">
            <Trophy className="w-5 h-5 text-primary-600 mx-auto mb-1" />
            <div className="text-lg font-semibold text-primary-600">
              {streakData.individual_contribution}
            </div>
            <div className="text-xs text-gray-600">Your Contribution</div>
          </div>
          <div className="text-center p-3 bg-secondary-50 rounded-lg">
            <Target className="w-5 h-5 text-secondary-600 mx-auto mb-1" />
            <div className="text-lg font-semibold text-secondary-600">
              {Math.max(0, streakData.group_goal - streakData.group_streak)}
            </div>
            <div className="text-xs text-gray-600">Days to Goal</div>
          </div>
        </div>

        {/* Top Contributors */}
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Top Contributors</h4>
          <div className="space-y-2">
            {getMostActiveMembers().map((member, index) => (
              <div key={member.id} className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  {index === 0 && <Crown className="w-4 h-4 text-yellow-500" />}
                  {index === 1 && <Star className="w-4 h-4 text-gray-400" />}
                  {index === 2 && <Star className="w-4 h-4 text-orange-400" />}
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-sm">
                    {member.avatar}
                  </div>
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">{member.name}</p>
                  <p className="text-xs text-gray-500">{member.last_activity}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-primary-600">{member.contribution}</div>
                  <div className="text-xs text-gray-500">activities</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Group Status */}
        {streakData.group_streak > 0 && (
          <div className="mb-4">
            {isGroupStreakAtRisk() ? (
              <div className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-red-800">Group streak at risk!</p>
                  <p className="text-xs text-red-600">
                    No recent group activity. Encourage your team!
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                <Clock className="w-5 h-5 text-green-500" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-green-800">Group is active!</p>
                  <p className="text-xs text-green-600">
                    Great teamwork keeping the streak alive
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={onActivityClick}
            className="bg-primary-600 hover:bg-primary-700 text-white py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <TreePine className="w-4 h-4" />
            <span>Log Activity</span>
          </button>
          <button
            onClick={onInviteClick}
            className="bg-secondary-600 hover:bg-secondary-700 text-white py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <UserPlus className="w-4 h-4" />
            <span>Invite Friends</span>
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>Progress to {streakData.group_goal}-day goal</span>
            <span>{streakData.group_streak}/{streakData.group_goal}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min((streakData.group_streak / streakData.group_goal) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CollaborativeStreak