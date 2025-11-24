import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { 
  Send, 
  Bot, 
  User, 
  TreePine, 
  Leaf, 
  Lightbulb,
  Camera,
  MapPin,
  Clock
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import RichTextRenderer from '../components/ui/RichTextRenderer'

const Chatbot = () => {
  const { user } = useAuth()
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Initial welcome message
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: `Hello ${user?.username}! 🌱 I'm your AI Tree Expert. I can help you with:

• Tree species selection for your region
• Planting and care techniques
• Disease and pest identification
• Seasonal planting advice
• Soil preparation tips

What would you like to know about trees today?`,
        timestamp: new Date()
      }
    ])
  }, [user])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      // Call the actual chatbot API endpoint
      const response = await api.post('/chatbot/query', {
        question: inputMessage,
        user_location: user?.location
      })

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      // Fallback response for demo
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: generateMockResponse(inputMessage),
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const generateMockResponse = (message) => {
    const lowerMessage = message.toLowerCase()
    
    if (lowerMessage.includes('mango') || lowerMessage.includes('fruit')) {
      return `🥭 Mango trees are excellent for Kenya! Here's what you need to know:

**Best Planting Time:** March-May (long rains) or October-December (short rains)
**Soil Requirements:** Well-drained, slightly acidic soil (pH 5.5-7.0)
**Spacing:** 8-10 meters apart for proper growth
**Care Tips:** 
- Water regularly for first 2 years
- Mulch around the base
- Prune dead branches annually

Would you like specific variety recommendations for your region?`
    }
    
    if (lowerMessage.includes('indigenous') || lowerMessage.includes('native')) {
      return `🌳 Indigenous trees are perfect for conservation! Here are top Kenyan natives:

**Coastal Region:** Baobab, Mbuyu, Mvule
**Highland Areas:** Cedar, Podo, Juniper
**Arid Regions:** Acacia species, Desert Rose
**General:** Mukwa, Meru Oak, African Olive

**Benefits:**
- Adapted to local climate
- Support native wildlife
- Require less water and care
- Preserve genetic diversity

Which region are you planting in?`
    }
    
    if (lowerMessage.includes('disease') || lowerMessage.includes('pest')) {
      return `🔍 Tree health is crucial! Common issues in Kenya:

**Fungal Diseases:**
- Root rot (overwatering)
- Leaf spot (humid conditions)
- Powdery mildew

**Pests:**
- Aphids, scale insects
- Termites (especially dry season)
- Caterpillars on young leaves

**Prevention:**
- Proper spacing for air circulation
- Avoid overwatering
- Regular inspection
- Organic neem oil treatment

Can you describe the symptoms you're seeing?`
    }
    
    if (lowerMessage.includes('soil') || lowerMessage.includes('preparation')) {
      return `🌱 Soil preparation is key to success! Here's how:

**Soil Testing:**
- Check pH level (most trees prefer 6.0-7.0)
- Test drainage by digging test holes
- Look for organic matter content

**Preparation Steps:**
1. Clear weeds and grass (2m radius)
2. Dig hole 2x wider than root ball
3. Mix soil with compost (1:1 ratio)
4. Add organic matter or manure
5. Ensure good drainage

**Red Soil Areas:** Add organic matter
**Clay Soil:** Improve drainage with sand
**Sandy Soil:** Add compost for retention

What's your soil type?`
    }
    
    return `🤖 I understand you're asking about "${message}". 

As your AI Tree Expert, I can provide detailed guidance on:
- Tree species selection
- Planting techniques
- Care and maintenance
- Problem diagnosis
- Seasonal advice

Could you be more specific about what aspect of tree care you'd like help with? For example:
- "What trees grow well in Nairobi?"
- "How do I treat yellow leaves?"
- "When should I plant in coastal Kenya?"`
  }

  const quickQuestions = [
    {
      icon: TreePine,
      text: "Best trees for my region",
      question: "What are the best trees to plant in my region?"
    },
    {
      icon: Leaf,
      text: "Tree care tips",
      question: "How do I take care of newly planted trees?"
    },
    {
      icon: MapPin,
      text: "Soil preparation",
      question: "How should I prepare soil for planting trees?"
    },
    {
      icon: Lightbulb,
      text: "Disease identification",
      question: "My tree has yellow leaves, what's wrong?"
    }
  ]

  const handleQuickQuestion = (question) => {
    setInputMessage(question)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bot className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-2">AI Tree Expert</h1>
          <p className="text-gray-600">Get personalized advice for your tree conservation journey</p>
        </motion.div>

        {/* Chat Container */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card h-[600px] flex flex-col"
        >
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex items-start space-x-3 max-w-[80%] ${
                  message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                }`}>
                  {/* Avatar */}
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.type === 'user' 
                      ? 'bg-primary-600' 
                      : 'bg-secondary-600'
                  }`}>
                    {message.type === 'user' ? (
                      <User className="w-4 h-4 text-white" />
                    ) : (
                      <Bot className="w-4 h-4 text-white" />
                    )}
                  </div>
                  
                  {/* Message Bubble */}
                  <div className={`rounded-lg p-4 ${
                    message.type === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {message.type === 'user' ? (
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    ) : (
                      <RichTextRenderer 
                        content={message.content} 
                        className="text-gray-800"
                      />
                    )}
                    <div className={`text-xs mt-2 ${
                      message.type === 'user' ? 'text-primary-200' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-secondary-600 rounded-full flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-gray-100 rounded-lg p-4">
                    <LoadingSpinner size="small" />
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Questions */}
          {messages.length === 1 && (
            <div className="px-6 py-4 border-t border-gray-200">
              <p className="text-sm text-gray-600 mb-3">Quick questions to get started:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {quickQuestions.map((item, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickQuestion(item.question)}
                    className="flex items-center space-x-2 p-3 text-left bg-primary-50 hover:bg-primary-100 rounded-lg transition-colors text-sm"
                  >
                    <item.icon className="w-4 h-4 text-primary-600" />
                    <span className="text-gray-700">{item.text}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="p-6 border-t border-gray-200">
            <div className="flex space-x-4">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask me anything about trees..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  disabled={isLoading}
                />
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
            
            {/* Additional Options */}
            <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
              <div className="flex items-center space-x-4">
                <button className="flex items-center space-x-1 hover:text-primary-600">
                  <Camera className="w-4 h-4" />
                  <span>Upload Image</span>
                </button>
                <button className="flex items-center space-x-1 hover:text-primary-600">
                  <MapPin className="w-4 h-4" />
                  <span>Share Location</span>
                </button>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>Available 24/7</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-6 text-center"
        >
          <p className="text-sm text-gray-600">
            💡 <strong>Pro tip:</strong> Be specific with your questions for better advice. 
            Include your location, tree species, and current conditions.
          </p>
        </motion.div>
      </div>
    </div>
  )
}

export default Chatbot