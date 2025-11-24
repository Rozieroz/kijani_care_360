import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  User, 
  Edit3, 
  TreePine, 
  Award, 
  Calendar,
  MapPin,
  Mail,
  Camera,
  Save,
  X,
  Leaf,
  TrendingUp,
  Target,
  Star,
  MessageSquare
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import StreakDisplay from '../components/ui/StreakDisplay'
import CollaborativeStreak from '../components/ui/CollaborativeStreak'
import AddActivityModal from '../components/modals/AddActivityModal'
import InviteToStreakModal from '../components/modals/InviteToStreakModal'
import api from '../utils/api'
import toast from 'react-hot-toast'

const Profile = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [showActivityModal, setShowActivityModal] = useState(false)
  const [showCollaborativeStreak, setShowCollaborativeStreak] = useState(true)
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [streakGroupData, setStreakGroupData] = useState(null)
  const [userPosts, setUserPosts] = useState([])
  const [postsLoading, setPostsLoading] = useState(false)
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    location: '',
    phone: '',
    bio: '',
    joinDate: '',
    stats: {
      treesPlanted: 0,
      treesAlive: 0,
      carbonOffset: 0,
      communityRank: 0,
      streakDays: 0
    },
    achievements: [],
    recentActivities: [],
    goals: []
  })

  useEffect(() => {
    if (user) {
      fetchProfileData()
      fetchUserPosts()
    }
  }, [user])

  const fetchProfileData = async () => {
    try {
      const response = await api.get('/profile/me')
      setProfileData(response.data)
    } catch (error) {
      console.error('Failed to fetch profile data:', error)
      // Fallback to basic user data
      setProfileData({
        username: user.username || '',
        email: user.email || '',
        location: user.location || '',
        phone: user.phone || '',
        bio: 'Passionate about tree conservation and environmental sustainability.',
        joinDate: user.created_at || '2024-01-01',
        stats: {
          treesPlanted: 24,
          treesAlive: 22,
          carbonOffset: 156,
          communityRank: 15,
          streakDays: 7
        },
        achievements: [
          { id: 1, title: 'First Tree Planted', description: 'Planted your first tree', icon: TreePine, earned: true, date: '2024-01-05' },
          { id: 2, title: 'Green Thumb', description: 'Maintained 90% survival rate', icon: Leaf, earned: true, date: '2024-01-10' },
          { id: 3, title: 'Community Helper', description: 'Helped 10 community members', icon: User, earned: false },
          { id: 4, title: 'Carbon Warrior', description: 'Offset 500kg of CO₂', icon: TrendingUp, earned: false },
          { id: 5, title: 'Tree Master', description: 'Plant 100 trees', icon: Award, earned: false },
          { id: 6, title: 'Streak Champion', description: '30-day activity streak', icon: Star, earned: false }
        ],
        recentActivities: [
          { id: 1, type: 'plant', description: 'Planted 3 Mango trees', date: '2024-01-15', location: 'Nairobi' },
          { id: 2, type: 'water', description: 'Watered trees in backyard', date: '2024-01-14', location: 'Home' },
          { id: 3, type: 'community', description: 'Joined tree planting event', date: '2024-01-12', location: 'Karura Forest' }
        ],
        goals: [
          { id: 1, title: 'Plant 50 trees this year', progress: 48, target: 50, type: 'planting' },
          { id: 2, title: 'Maintain 95% survival rate', progress: 92, target: 95, type: 'care' },
          { id: 3, title: 'Join 5 community events', progress: 2, target: 5, type: 'community' }
        ]
      })
    }
  }

  const fetchUserPosts = async () => {
    setPostsLoading(true)
    try {
      const response = await api.get('/social/posts/my-posts')
      setUserPosts(response.data)
    } catch (error) {
      console.error('Failed to fetch user posts:', error)
      // Fallback to mock data
      setUserPosts([
        {
          id: 1,
          content: 'Just completed my 7-day tree planting streak! 🌱 Planted 15 indigenous trees this week in different locations around Nairobi. The impact we can make together is incredible!',
          image_url: null,
          likes_count: 12,
          comments_count: 3,
          shares_count: 2,
          created_at: '2024-01-15T10:30:00Z',
          tags: 'TreePlanting,Streak,Indigenous',
          location: 'Nairobi',
          post_type: 'achievement'
        },
        {
          id: 2,
          content: 'Sharing some tips for new tree planters: 1) Choose native species 2) Plant during rainy season 3) Ensure proper spacing 4) Water regularly in first month. What other tips do you have?',
          image_url: null,
          likes_count: 8,
          comments_count: 5,
          shares_count: 4,
          created_at: '2024-01-12T14:20:00Z',
          tags: 'Tips,TreeCare,Beginners',
          location: 'Kenya',
          post_type: 'tip'
        },
        {
          id: 3,
          content: 'Excited to announce our community tree planting event this weekend at Karura Forest! Join us as we plant 100+ trees together. Every tree counts in our fight against climate change! 🌳',
          image_url: null,
          likes_count: 25,
          comments_count: 8,
          shares_count: 12,
          created_at: '2024-01-10T09:15:00Z',
          tags: 'Event,Community,KaruraForest',
          location: 'Karura Forest',
          post_type: 'event'
        }
      ])
    } finally {
      setPostsLoading(false)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      await api.put('/profile/me', {
        username: profileData.username,
        location: profileData.location,
        phone: profileData.phone
      })
      setIsEditing(false)
    } catch (error) {
      console.error('Failed to update profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const getActivityIcon = (type) => {
    switch (type) {
      case 'plant': return TreePine
      case 'water': return Leaf
      case 'community': return User
      default: return Calendar
    }
  }

  const getGoalColor = (progress, target) => {
    const percentage = (progress / target) * 100
    if (percentage >= 100) return 'bg-green-500'
    if (percentage >= 75) return 'bg-primary-500'
    if (percentage >= 50) return 'bg-yellow-500'
    return 'bg-gray-400'
  }

  const handleActivityAdded = (newActivity) => {
    // Update profile data with new activity
    setProfileData(prev => ({
      ...prev,
      stats: {
        ...prev.stats,
        treesPlanted: prev.stats.treesPlanted + (newActivity.trees_count || 1),
        streakDays: newActivity.streak_days || prev.stats.streakDays
      },
      recentActivities: [
        {
          id: Date.now(),
          type: newActivity.activity_type,
          description: `${newActivity.activity_type} ${newActivity.trees_count} trees`,
          date: new Date().toLocaleDateString(),
          location: newActivity.location || 'Unknown'
        },
        ...prev.recentActivities.slice(0, 4) // Keep only 5 most recent
      ]
    }))
    
    toast.success('Activity logged successfully! 🌱')
  }

  const handleInviteToStreak = () => {
    // Fetch current streak group data and show invite modal
    setStreakGroupData({
      group_id: 1,
      group_name: 'Nairobi Tree Warriors',
      group_members: [
        { id: 1, name: 'You', avatar: '👤' },
        { id: 2, name: 'Sarah K.', avatar: '👩🏾' },
        { id: 3, name: 'John M.', avatar: '👨🏽' }
      ]
    })
    setShowInviteModal(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-8 mb-8"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-8">
            {/* Avatar */}
            <div className="relative">
              <div className="w-32 h-32 bg-primary-600 rounded-full flex items-center justify-center text-4xl text-white font-bold">
                {profileData.username.charAt(0).toUpperCase()}
              </div>
              <button className="absolute bottom-2 right-2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow">
                <Camera className="w-4 h-4 text-gray-600" />
              </button>
            </div>

            {/* Profile Info */}
            <div className="flex-1">
              {isEditing ? (
                <div className="space-y-4">
                  <input
                    type="text"
                    value={profileData.username}
                    onChange={(e) => handleInputChange('username', e.target.value)}
                    className="text-2xl font-bold bg-transparent border-b-2 border-primary-300 focus:border-primary-600 outline-none"
                  />
                  <textarea
                    value={profileData.bio}
                    onChange={(e) => handleInputChange('bio', e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    rows="3"
                    placeholder="Tell us about yourself..."
                  />
                  <div className="grid md:grid-cols-2 gap-4">
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      className="input-field"
                      placeholder="Email"
                    />
                    <input
                      type="text"
                      value={profileData.location}
                      onChange={(e) => handleInputChange('location', e.target.value)}
                      className="input-field"
                      placeholder="Location"
                    />
                    <input
                      type="tel"
                      value={profileData.phone}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      className="input-field"
                      placeholder="Phone"
                    />
                  </div>
                </div>
              ) : (
                <div>
                  <h1 className="text-3xl font-bold text-gray-800 mb-2">{profileData.username}</h1>
                  <p className="text-gray-600 mb-4">{profileData.bio}</p>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <Mail className="w-4 h-4" />
                      <span>{profileData.email}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MapPin className="w-4 h-4" />
                      <span>{profileData.location}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>Joined {new Date(profileData.joinDate).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-3">
              {isEditing ? (
                <>
                  <button
                    onClick={handleSave}
                    disabled={loading}
                    className="btn-primary flex items-center space-x-2"
                  >
                    {loading ? <LoadingSpinner size="small" /> : <Save className="w-4 h-4" />}
                    <span>Save</span>
                  </button>
                  <button
                    onClick={() => setIsEditing(false)}
                    className="btn-outline flex items-center space-x-2"
                  >
                    <X className="w-4 h-4" />
                    <span>Cancel</span>
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="btn-primary flex items-center space-x-2"
                >
                  <Edit3 className="w-4 h-4" />
                  <span>Edit Profile</span>
                </button>
              )}
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Streak Display */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.05 }}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-800">Your Streak</h2>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setShowCollaborativeStreak(!showCollaborativeStreak)}
                    className="text-sm text-primary-600 hover:text-primary-700 transition-colors"
                  >
                    {showCollaborativeStreak ? 'Individual' : 'Collaborative'}
                  </button>
                </div>
              </div>
              {showCollaborativeStreak ? (
                <CollaborativeStreak 
                  onActivityClick={() => setShowActivityModal(true)}
                  onInviteClick={handleInviteToStreak}
                />
              ) : (
                <StreakDisplay onActivityClick={() => setShowActivityModal(true)} />
              )}
            </motion.div>
            {/* Stats Overview */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Impact</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="card p-4 text-center">
                  <TreePine className="w-8 h-8 text-primary-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-primary-600">{profileData.stats.treesPlanted}</div>
                  <div className="text-sm text-gray-600">Trees Planted</div>
                </div>
                <div className="card p-4 text-center">
                  <Leaf className="w-8 h-8 text-secondary-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-secondary-600">{profileData.stats.treesAlive}</div>
                  <div className="text-sm text-gray-600">Trees Alive</div>
                </div>
                <div className="card p-4 text-center">
                  <TrendingUp className="w-8 h-8 text-accent-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-accent-600">{profileData.stats.carbonOffset}kg</div>
                  <div className="text-sm text-gray-600">CO₂ Offset</div>
                </div>
                <div className="card p-4 text-center">
                  <Award className="w-8 h-8 text-primary-700 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-primary-700">#{profileData.stats.communityRank}</div>
                  <div className="text-sm text-gray-600">Community Rank</div>
                </div>
                <div className="card p-4 text-center">
                  <Star className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-yellow-600">{profileData.stats.streakDays}</div>
                  <div className="text-sm text-gray-600">Day Streak</div>
                </div>
              </div>
            </motion.div>

            {/* Goals Progress */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Goals Progress</h2>
              <div className="card p-6">
                <div className="space-y-6">
                  {profileData.goals.map((goal) => (
                    <div key={goal.id}>
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-medium text-gray-800">{goal.title}</h3>
                        <span className="text-sm text-gray-600">
                          {goal.progress}/{goal.target}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className={`h-3 rounded-full transition-all duration-300 ${getGoalColor(goal.progress, goal.target)}`}
                          style={{ width: `${Math.min((goal.progress / goal.target) * 100, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Recent Activities */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activities</h2>
              <div className="card p-6">
                <div className="space-y-4">
                  {profileData.recentActivities.map((activity) => {
                    const Icon = getActivityIcon(activity.type)
                    return (
                      <div key={activity.id} className="flex items-center space-x-4 p-3 bg-primary-50 rounded-lg">
                        <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                          <Icon className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium text-gray-800">{activity.description}</p>
                          <p className="text-sm text-gray-600">{activity.location} • {activity.date}</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </motion.div>

            {/* User Posts */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">My Posts</h2>
              {postsLoading ? (
                <div className="card p-6">
                  <div className="animate-pulse space-y-4">
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                    <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                  </div>
                </div>
              ) : userPosts.length > 0 ? (
                <div className="space-y-6">
                  {userPosts.map((post) => (
                    <div key={post.id} className="card p-6">
                      {/* Post Header */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-lg">
                            {profileData.username.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-800">{profileData.username}</h3>
                            <div className="flex items-center space-x-2 text-sm text-gray-600">
                              <MapPin className="w-3 h-3" />
                              <span>{post.location}</span>
                              <span>•</span>
                              <span>{new Date(post.created_at).toLocaleDateString()}</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          {post.post_type === 'achievement' && <span className="text-lg">🏆</span>}
                          {post.post_type === 'tip' && <span className="text-lg">💡</span>}
                          {post.post_type === 'event' && <span className="text-lg">📅</span>}
                          {post.post_type === 'general' && <span className="text-lg">💬</span>}
                        </div>
                      </div>

                      {/* Post Content */}
                      <p className="text-gray-700 mb-4">{post.content}</p>

                      {/* Post Image */}
                      {post.image_url && (
                        <div className="mb-4 rounded-lg overflow-hidden">
                          <img
                            src={post.image_url}
                            alt="Post content"
                            className="w-full h-64 object-cover"
                          />
                        </div>
                      )}

                      {/* Tags */}
                      {post.tags && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {post.tags.split(',').map((tag) => (
                            <span
                              key={tag}
                              className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full"
                            >
                              #{tag.trim()}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Post Stats */}
                      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                        <div className="flex items-center space-x-6 text-sm text-gray-600">
                          <div className="flex items-center space-x-1">
                            <span>{post.likes_count}</span>
                            <span>likes</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <span>{post.comments_count}</span>
                            <span>comments</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <span>{post.shares_count}</span>
                            <span>shares</span>
                          </div>
                        </div>
                        <div className="text-xs text-gray-500">
                          {new Date(post.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="card p-8 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <MessageSquare className="w-8 h-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-600 mb-2">No posts yet</h3>
                  <p className="text-gray-500 mb-4">Share your tree planting journey with the community!</p>
                  <button 
                    onClick={() => navigate('/community')}
                    className="btn-primary"
                  >
                    Create Your First Post
                  </button>
                </div>
              )}
            </motion.div>
          </div>

          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {/* Achievements */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Achievements</h3>
              <div className="grid grid-cols-2 gap-3">
                {profileData.achievements.map((achievement) => (
                  <div
                    key={achievement.id}
                    className={`p-3 rounded-lg text-center transition-all ${
                      achievement.earned 
                        ? 'bg-primary-100 text-primary-600 shadow-sm' 
                        : 'bg-gray-100 text-gray-400'
                    }`}
                  >
                    <achievement.icon className="w-6 h-6 mx-auto mb-1" />
                    <p className="text-xs font-medium">{achievement.title}</p>
                    {achievement.earned && achievement.date && (
                      <p className="text-xs text-primary-500 mt-1">{achievement.date}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => setShowActivityModal(true)}
                  className="w-full btn-primary text-left flex items-center space-x-2"
                >
                  <TreePine className="w-4 h-4" />
                  <span>Log Tree Activity</span>
                </button>
                <button className="w-full btn-outline text-left flex items-center space-x-2">
                  <Target className="w-4 h-4" />
                  <span>Set New Goal</span>
                </button>
                <button className="w-full btn-outline text-left flex items-center space-x-2">
                  <User className="w-4 h-4" />
                  <span>Invite Friends</span>
                </button>
              </div>
            </div>

            {/* Profile Completion */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Profile Completion</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Profile Info</span>
                  <span className="text-primary-600 font-medium">85%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-primary-600 h-2 rounded-full" style={{ width: '85%' }}></div>
                </div>
                <div className="text-xs text-gray-500">
                  Add phone number and bio to complete your profile
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Floating Action Button for Mobile */}
      <button
        onClick={() => setShowActivityModal(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center z-40 md:hidden"
      >
        <TreePine className="w-6 h-6" />
      </button>

      {/* Add Activity Modal */}
      <AddActivityModal
        isOpen={showActivityModal}
        onClose={() => setShowActivityModal(false)}
        onActivityAdded={handleActivityAdded}
      />

      {/* Invite to Streak Modal */}
      <InviteToStreakModal
        isOpen={showInviteModal}
        onClose={() => setShowInviteModal(false)}
        groupData={streakGroupData}
      />
    </div>
  )
}

export default Profile