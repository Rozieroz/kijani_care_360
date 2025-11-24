import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  MessageSquare, 
  Heart, 
  Share2, 
  Plus,
  TreePine,
  MapPin,
  Calendar,
  Camera,
  Award,
  TrendingUp,
  Filter,
  Search
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import PlaceholderImage from '../components/ui/PlaceholderImage'
import CreatePostModal from '../components/modals/CreatePostModal'
import api from '../utils/api'
import toast from 'react-hot-toast'

const Community = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('feed')
  const [posts, setPosts] = useState([])
  const [events, setEvents] = useState([])
  const [showCreatePost, setShowCreatePost] = useState(false)

  useEffect(() => {
    fetchCommunityData()
  }, [activeTab])

  const fetchCommunityData = async () => {
    try {
      if (activeTab === 'feed') {
        const response = await api.get('/community/feed')
        setPosts(response.data.map(post => ({
          id: post.id,
          user: { 
            name: post.username || 'Anonymous', 
            avatar: post.user_avatar || '👤', 
            location: post.location || 'Kenya' 
          },
          content: post.content,
          image: post.image_url,
          likes: post.likes_count,
          comments: post.comments_count,
          shares: post.shares_count,
          timestamp: new Date(post.created_at).toLocaleDateString(),
          tags: post.tags ? post.tags.split(',') : [],
          isLiked: post.is_liked
        })))
      } else if (activeTab === 'events') {
        const response = await api.get('/community/events')
        setEvents(response.data.map(event => ({
          id: event.id,
          title: event.title,
          date: new Date(event.event_date).toLocaleDateString(),
          time: new Date(event.event_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          location: event.location,
          attendees: event.attendee_count,
          organizer: event.organizer_name || 'Community Organizer',
          description: event.description,
          isAttending: event.is_attending
        })))
      }
    } catch (error) {
      console.error('Failed to fetch community data:', error)
      // Fallback to mock data
      if (activeTab === 'feed') {
        setPosts([
          {
            id: 1,
            user: { name: 'Sarah Wanjiku', avatar: '👩🏾', location: 'Nairobi' },
            content: 'Just planted 50 indigenous trees in Karura Forest! The community turnout was amazing. Together we can restore Kenya\'s green cover! 🌳',
            image: null,
            likes: 24,
            comments: 8,
            shares: 3,
            timestamp: '2 hours ago',
            tags: ['TreePlanting', 'KaruraForest', 'Indigenous'],
            isLiked: false
          },
          {
            id: 2,
            user: { name: 'John Kimani', avatar: '👨🏽', location: 'Mombasa' },
            content: 'Sharing some essential tips for new tree planters: 1) Choose native species 2) Plant during rainy season 3) Ensure proper spacing 4) Water regularly in first month. What other tips do you have? 💡',
            image: null,
            likes: 18,
            comments: 12,
            shares: 6,
            timestamp: '4 hours ago',
            tags: ['Tips', 'TreeCare', 'Beginners'],
            isLiked: true
          },
          {
            id: 3,
            user: { name: 'Grace Akinyi', avatar: '👩🏿', location: 'Kisumu' },
            content: 'Excited to announce our community tree planting event this weekend at Uhuru Park! Join us as we plant 100+ trees together. Every tree counts in our fight against climate change! 🌍',
            image: null,
            likes: 32,
            comments: 15,
            shares: 18,
            timestamp: '6 hours ago',
            tags: ['Event', 'Community', 'UhuruPark'],
            isLiked: false
          },
          {
            id: 4,
            user: { name: 'David Mwangi', avatar: '👨🏾', location: 'Nakuru' },
            content: 'Celebrating my 30-day tree planting streak! 🔥 Planted over 45 trees this month across different locations. The collaborative streak feature is amazing - my team has been so supportive!',
            image: null,
            likes: 28,
            comments: 9,
            shares: 4,
            timestamp: '8 hours ago',
            tags: ['Streak', 'Achievement', 'Collaboration'],
            isLiked: false
          },
          {
            id: 5,
            user: { name: 'Mary Njeri', avatar: '👩🏽', location: 'Eldoret' },
            content: 'Amazing progress update: Our school\'s tree nursery now has over 200 seedlings ready for planting! Students are so excited to contribute to reforestation. Education + Action = Change! 📚🌱',
            image: null,
            likes: 41,
            comments: 22,
            shares: 14,
            timestamp: '12 hours ago',
            tags: ['Education', 'Nursery', 'Students', 'Reforestation'],
            isLiked: true
          },
          {
            id: 6,
            user: { name: 'Peter Ochieng', avatar: '👨🏿', location: 'Kisii' },
            content: 'Just completed a tree survival assessment in our area. Happy to report 92% survival rate! Proper aftercare really makes a difference. Here\'s what worked for us... 📊',
            image: null,
            likes: 19,
            comments: 7,
            shares: 8,
            timestamp: '1 day ago',
            tags: ['Assessment', 'SurvivalRate', 'TreeCare'],
            isLiked: false
          }
        ])
      } else if (activeTab === 'events') {
        setEvents([
          {
            id: 1,
            title: 'Community Tree Planting - Karura Forest',
            description: 'Join us for a massive tree planting initiative in Karura Forest. We aim to plant 500+ indigenous trees in a single day!',
            date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toLocaleDateString(),
            time: '08:00',
            location: 'Karura Forest, Nairobi',
            attendees: 127,
            organizer: 'Kenya Forest Service',
            isAttending: false
          },
          {
            id: 2,
            title: 'Tree Care Workshop',
            description: 'Learn essential tree care techniques from forestry experts. Perfect for beginners and experienced planters alike.',
            date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toLocaleDateString(),
            time: '14:00',
            location: 'University of Nairobi, Botany Department',
            attendees: 45,
            organizer: 'Dr. Wangari Maathai Foundation',
            isAttending: true
          },
          {
            id: 3,
            title: 'Urban Forestry Seminar',
            description: 'Exploring innovative approaches to urban tree planting and maintenance in Kenyan cities.',
            date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString(),
            time: '10:00',
            location: 'KICC, Nairobi',
            attendees: 89,
            organizer: 'Green Belt Movement',
            isAttending: false
          }
        ])
      }
    }
  }

  const tabs = [
    { id: 'feed', name: 'Community Feed', icon: MessageSquare },
    { id: 'events', name: 'Events', icon: Calendar },
    { id: 'leaderboard', name: 'Leaderboard', icon: Award }
  ]

  const leaderboardData = [
    { rank: 1, name: 'Sarah Wanjiku', trees: 156, location: 'Nairobi', badge: '🏆' },
    { rank: 2, name: 'John Kimani', trees: 142, location: 'Mombasa', badge: '🥈' },
    { rank: 3, name: 'Grace Akinyi', trees: 128, location: 'Kisumu', badge: '🥉' },
    { rank: 4, name: 'David Mwangi', trees: 98, location: 'Nakuru', badge: '🌟' },
    { rank: 5, name: 'Mary Njeri', trees: 87, location: 'Eldoret', badge: '🌟' }
  ]

  const handleLike = async (postId) => {
    try {
      const response = await api.post(`/community/posts/${postId}/like`)
      
      setPosts(posts.map(post => 
        post.id === postId 
          ? { 
              ...post, 
              likes: response.data.likes_count,
              isLiked: response.data.is_liked
            }
          : post
      ))
    } catch (error) {
      console.error('Failed to like post:', error)
      // Fallback to optimistic update
      setPosts(posts.map(post => 
        post.id === postId 
          ? { 
              ...post, 
              likes: post.isLiked ? post.likes - 1 : post.likes + 1,
              isLiked: !post.isLiked
            }
          : post
      ))
    }
  }

  const handlePostCreated = (newPost) => {
    // Add the new post to the top of the feed
    const formattedPost = {
      id: newPost.id,
      user: { 
        name: newPost.username || user?.username || 'You', 
        avatar: '👤', 
        location: newPost.location || 'Kenya' 
      },
      content: newPost.content,
      image: newPost.image_url,
      likes: 0,
      comments: 0,
      shares: 0,
      timestamp: 'Just now',
      tags: newPost.tags ? newPost.tags.split(',').map(tag => tag.trim()) : [],
      isLiked: false
    }
    setPosts([formattedPost, ...posts])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">Community Hub</h1>
              <p className="text-gray-600">Connect, share, and grow together</p>
            </div>
            <button
              onClick={() => setShowCreatePost(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Share Update</span>
            </button>
          </div>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <div className="flex space-x-1 bg-white rounded-lg p-1 shadow-sm">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Content */}
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3">
            {activeTab === 'feed' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="space-y-6"
              >
                {/* Search and Filter */}
                <div className="card p-4">
                  <div className="flex space-x-4">
                    <div className="flex-1 relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Search posts..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                    <button className="btn-outline flex items-center space-x-2">
                      <Filter className="w-4 h-4" />
                      <span>Filter</span>
                    </button>
                  </div>
                </div>

                {/* Posts */}
                {posts.map((post) => (
                  <div key={post.id} className="card p-6">
                    {/* Post Header */}
                    <div className="flex items-center space-x-3 mb-4">
                      <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-lg">
                        {post.user.avatar}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-800">{post.user.name}</h3>
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <MapPin className="w-3 h-3" />
                          <span>{post.user.location}</span>
                          <span>•</span>
                          <span>{post.timestamp}</span>
                        </div>
                      </div>
                      <button
                        className="p-2 text-gray-400 hover:text-primary-600 transition-colors"
                        title="Send message"
                      >
                        <MessageSquare className="w-4 h-4" />
                      </button>
                    </div>

                    {/* Post Content */}
                    <p className="text-gray-700 mb-4">{post.content}</p>

                    {/* Post Image */}
                    {post.image && (
                      <div className="mb-4 rounded-lg overflow-hidden">
                        {post.image.startsWith('/api/placeholder') ? (
                          <PlaceholderImage width={400} height={256} className="w-full rounded-lg" />
                        ) : (
                          <img
                            src={post.image}
                            alt="Post content"
                            className="w-full h-64 object-cover"
                          />
                        )}
                      </div>
                    )}

                    {/* Tags */}
                    {post.tags && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {post.tags.map((tag) => (
                          <span
                            key={tag}
                            className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Post Actions */}
                    <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                      <div className="flex items-center space-x-6">
                        <button
                          onClick={() => handleLike(post.id)}
                          className="flex items-center space-x-2 text-gray-600 hover:text-red-500 transition-colors"
                        >
                          <Heart className="w-4 h-4" />
                          <span className="text-sm">{post.likes}</span>
                        </button>
                        <button className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors">
                          <MessageSquare className="w-4 h-4" />
                          <span className="text-sm">{post.comments}</span>
                        </button>
                        <button className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors">
                          <Share2 className="w-4 h-4" />
                          <span className="text-sm">{post.shares}</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </motion.div>
            )}

            {activeTab === 'events' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="space-y-6"
              >
                {events.map((event) => (
                  <div key={event.id} className="card p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-gray-800 mb-2">{event.title}</h3>
                        <p className="text-gray-600 mb-4">{event.description}</p>
                        
                        <div className="space-y-2">
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Calendar className="w-4 h-4" />
                            <span>{event.date} at {event.time}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <MapPin className="w-4 h-4" />
                            <span>{event.location}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Users className="w-4 h-4" />
                            <span>{event.attendees} attending</span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <button className="btn-primary mb-2">Join Event</button>
                        <p className="text-xs text-gray-500">by {event.organizer}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </motion.div>
            )}

            {activeTab === 'leaderboard' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="card p-6">
                  <h2 className="text-xl font-semibold text-gray-800 mb-6">Top Tree Planters</h2>
                  <div className="space-y-4">
                    {leaderboardData.map((person) => (
                      <div
                        key={person.rank}
                        className={`flex items-center space-x-4 p-4 rounded-lg ${
                          person.rank <= 3 ? 'bg-gradient-to-r from-primary-50 to-secondary-50' : 'bg-gray-50'
                        }`}
                      >
                        <div className="text-2xl">{person.badge}</div>
                        <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold">
                          {person.rank}
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-800">{person.name}</h3>
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <MapPin className="w-3 h-3" />
                            <span>{person.location}</span>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <button
                            className="p-2 text-gray-400 hover:text-primary-600 transition-colors"
                            title="Send message"
                          >
                            <MessageSquare className="w-4 h-4" />
                          </button>
                          <div className="text-right">
                            <div className="flex items-center space-x-1 text-primary-600 font-semibold">
                              <TreePine className="w-4 h-4" />
                              <span>{person.trees}</span>
                            </div>
                            <p className="text-xs text-gray-500">trees planted</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            {/* Community Stats */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Community Impact</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <TreePine className="w-4 h-4 text-primary-600" />
                    <span className="text-sm text-gray-600">Trees Planted</span>
                  </div>
                  <span className="font-semibold text-primary-600">12,847</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Users className="w-4 h-4 text-secondary-600" />
                    <span className="text-sm text-gray-600">Active Members</span>
                  </div>
                  <span className="font-semibold text-secondary-600">2,341</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="w-4 h-4 text-accent-600" />
                    <span className="text-sm text-gray-600">CO₂ Offset</span>
                  </div>
                  <span className="font-semibold text-accent-600">89.2 tons</span>
                </div>
              </div>
            </div>

            {/* Trending Topics */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Trending Topics</h3>
              <div className="space-y-2">
                {['#TreePlanting', '#IndigenousTrees', '#UrbanForestry', '#ClimateAction', '#KenyaForests'].map((tag) => (
                  <div key={tag} className="flex items-center justify-between">
                    <span className="text-sm text-primary-600 font-medium">{tag}</span>
                    <span className="text-xs text-gray-500">124 posts</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggested Users */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Suggested Connections</h3>
              <div className="space-y-3">
                {[
                  { name: 'Dr. Wangari Maathai Foundation', location: 'Nairobi', followers: '12.5K' },
                  { name: 'Kenya Forest Service', location: 'National', followers: '8.9K' },
                  { name: 'Green Belt Movement', location: 'Nairobi', followers: '15.2K' }
                ].map((user, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-800">{user.name}</p>
                      <p className="text-xs text-gray-600">{user.location} • {user.followers} followers</p>
                    </div>
                    <button className="text-xs btn-outline px-3 py-1">Follow</button>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Floating Action Button for Mobile */}
      <button
        onClick={() => setShowCreatePost(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center z-40 md:hidden"
      >
        <Plus className="w-6 h-6" />
      </button>

      {/* Create Post Modal */}
      <CreatePostModal
        isOpen={showCreatePost}
        onClose={() => setShowCreatePost(false)}
        onPostCreated={handlePostCreated}
      />
    </div>
  )
}

export default Community