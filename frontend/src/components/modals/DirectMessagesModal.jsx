import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  X, 
  Send, 
  Search,
  MessageCircle,
  TreePine,
  Phone,
  Video,
  MoreVertical,
  Paperclip,
  Smile
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const DirectMessagesModal = ({ isOpen, onClose }) => {
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      fetchConversations()
    }
  }, [isOpen])

  useEffect(() => {
    if (activeConversation) {
      fetchMessages(activeConversation.id)
    }
  }, [activeConversation])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchConversations = async () => {
    try {
      const response = await api.get('/social/messages/conversations')
      setConversations(response.data)
    } catch (error) {
      console.error('Failed to fetch conversations:', error)
      // Fallback to mock data
      setConversations([
        {
          id: 1,
          participant: {
            id: 2,
            name: 'Sarah Wanjiku',
            avatar: '👩🏾',
            online: true,
            last_seen: null
          },
          last_message: {
            content: 'Great job on your tree planting streak! 🌱',
            timestamp: '2 min ago',
            unread: true
          }
        },
        {
          id: 2,
          participant: {
            id: 3,
            name: 'John Kimani',
            avatar: '👨🏽',
            online: false,
            last_seen: '1 hour ago'
          },
          last_message: {
            content: 'Want to join our weekend planting event?',
            timestamp: '1 hour ago',
            unread: false
          }
        },
        {
          id: 3,
          participant: {
            id: 4,
            name: 'Grace Akinyi',
            avatar: '👩🏿',
            online: false,
            last_seen: '2 days ago'
          },
          last_message: {
            content: 'Thanks for the tree care tips!',
            timestamp: '2 days ago',
            unread: false
          }
        }
      ])
    }
  }

  const fetchMessages = async (conversationId) => {
    setLoading(true)
    try {
      const response = await api.get(`/social/messages/conversations/${conversationId}`)
      setMessages(response.data)
    } catch (error) {
      console.error('Failed to fetch messages:', error)
      // Fallback to mock data
      setMessages([
        {
          id: 1,
          sender_id: 2,
          content: 'Hey! I saw your amazing tree planting progress. Keep it up! 🌳',
          timestamp: '2024-01-15T10:30:00Z',
          is_own: false
        },
        {
          id: 2,
          sender_id: 1,
          content: 'Thank you! Your streak group idea is brilliant. We should collaborate more!',
          timestamp: '2024-01-15T10:32:00Z',
          is_own: true
        },
        {
          id: 3,
          sender_id: 2,
          content: 'Absolutely! I\'m organizing a weekend planting event in Karura Forest. Would you like to join?',
          timestamp: '2024-01-15T10:35:00Z',
          is_own: false
        },
        {
          id: 4,
          sender_id: 1,
          content: 'Count me in! What time and what should I bring?',
          timestamp: '2024-01-15T10:36:00Z',
          is_own: true
        },
        {
          id: 5,
          sender_id: 2,
          content: 'Great job on your tree planting streak! 🌱',
          timestamp: '2024-01-15T11:00:00Z',
          is_own: false
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!newMessage.trim() || !activeConversation) return

    const messageData = {
      conversation_id: activeConversation.id,
      content: newMessage.trim()
    }

    try {
      const response = await api.post('/social/messages', messageData)
      
      // Add message to local state
      const newMsg = {
        id: response.data.id || Date.now(),
        sender_id: 1, // Current user
        content: newMessage.trim(),
        timestamp: new Date().toISOString(),
        is_own: true
      }
      
      setMessages(prev => [...prev, newMsg])
      setNewMessage('')
      
      // Update conversation list
      setConversations(prev => prev.map(conv => 
        conv.id === activeConversation.id 
          ? {
              ...conv,
              last_message: {
                content: newMessage.trim(),
                timestamp: 'Just now',
                unread: false
              }
            }
          : conv
      ))
      
    } catch (error) {
      console.error('Failed to send message:', error)
      toast.error('Failed to send message. Please try again.')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const filteredConversations = conversations.filter(conv =>
    conv.participant.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black bg-opacity-50"
            onClick={onClose}
          />
          
          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative bg-white rounded-xl shadow-xl max-w-4xl w-full h-[600px] flex overflow-hidden"
          >
            {/* Conversations List */}
            <div className="w-1/3 border-r border-gray-200 flex flex-col">
              {/* Header */}
              <div className="p-4 border-b border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-800">Messages</h2>
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-500" />
                  </button>
                </div>
                
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search conversations..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                  />
                </div>
              </div>

              {/* Conversations */}
              <div className="flex-1 overflow-y-auto">
                {filteredConversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    onClick={() => setActiveConversation(conversation)}
                    className={`w-full p-4 text-left hover:bg-gray-50 transition-colors border-b border-gray-100 ${
                      activeConversation?.id === conversation.id ? 'bg-primary-50 border-primary-200' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="relative">
                        <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-lg">
                          {conversation.participant.avatar}
                        </div>
                        {conversation.participant.online && (
                          <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <h3 className="font-medium text-gray-800 truncate">{conversation.participant.name}</h3>
                          <span className="text-xs text-gray-500">{conversation.last_message.timestamp}</span>
                        </div>
                        <p className="text-sm text-gray-600 truncate">{conversation.last_message.content}</p>
                        {!conversation.participant.online && conversation.participant.last_seen && (
                          <p className="text-xs text-gray-400">Last seen {conversation.participant.last_seen}</p>
                        )}
                      </div>
                      {conversation.last_message.unread && (
                        <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col">
              {activeConversation ? (
                <>
                  {/* Chat Header */}
                  <div className="p-4 border-b border-gray-200 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="relative">
                        <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                          {activeConversation.participant.avatar}
                        </div>
                        {activeConversation.participant.online && (
                          <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                        )}
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-800">{activeConversation.participant.name}</h3>
                        <p className="text-sm text-gray-500">
                          {activeConversation.participant.online 
                            ? 'Online' 
                            : `Last seen ${activeConversation.participant.last_seen}`
                          }
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <Phone className="w-5 h-5 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <Video className="w-5 h-5 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <MoreVertical className="w-5 h-5 text-gray-600" />
                      </button>
                    </div>
                  </div>

                  {/* Messages */}
                  <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {loading ? (
                      <div className="flex items-center justify-center h-full">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                      </div>
                    ) : (
                      messages.map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${message.is_own ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                              message.is_own
                                ? 'bg-primary-600 text-white'
                                : 'bg-gray-100 text-gray-800'
                            }`}
                          >
                            <p className="text-sm">{message.content}</p>
                            <p className={`text-xs mt-1 ${
                              message.is_own ? 'text-primary-100' : 'text-gray-500'
                            }`}>
                              {formatTime(message.timestamp)}
                            </p>
                          </div>
                        </div>
                      ))
                    )}
                    <div ref={messagesEndRef} />
                  </div>

                  {/* Message Input */}
                  <div className="p-4 border-t border-gray-200">
                    <div className="flex items-center space-x-3">
                      <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <Paperclip className="w-5 h-5 text-gray-600" />
                      </button>
                      <div className="flex-1 relative">
                        <textarea
                          value={newMessage}
                          onChange={(e) => setNewMessage(e.target.value)}
                          onKeyPress={handleKeyPress}
                          placeholder="Type a message..."
                          rows={1}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                        />
                      </div>
                      <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <Smile className="w-5 h-5 text-gray-600" />
                      </button>
                      <button
                        onClick={sendMessage}
                        disabled={!newMessage.trim()}
                        className="p-2 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full transition-colors"
                      >
                        <Send className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center">
                  <div className="text-center">
                    <MessageCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-600 mb-2">Select a conversation</h3>
                    <p className="text-gray-500">Choose a conversation to start messaging</p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

export default DirectMessagesModal