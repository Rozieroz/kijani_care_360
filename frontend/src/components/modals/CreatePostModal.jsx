import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  X, 
  Camera, 
  MapPin, 
  Hash,
  TreePine,
  Smile
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const CreatePostModal = ({ isOpen, onClose, onPostCreated }) => {
  const [formData, setFormData] = useState({
    content: '',
    image_url: '',
    location: '',
    tags: '',
    post_type: 'general'
  })
  const [loading, setLoading] = useState(false)

  const postTypes = [
    { value: 'general', label: 'General Update', emoji: '💬' },
    { value: 'achievement', label: 'Achievement', emoji: '🏆' },
    { value: 'event', label: 'Event', emoji: '📅' },
    { value: 'tip', label: 'Tree Tip', emoji: '💡' }
  ]

  const quickTags = [
    '#TreePlanting', '#Indigenous', '#Conservation', '#KenyaForests',
    '#ClimateAction', '#GreenKenya', '#Reforestation', '#NativeSpecies'
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.content.trim()) {
      toast.error('Please write something to share!')
      return
    }

    setLoading(true)

    try {
      const response = await api.post('/social/posts', {
        ...formData,
        content: formData.content.trim()
      })
      
      toast.success('🌱 Post shared with the community!')
      
      // Reset form
      setFormData({
        content: '',
        image_url: '',
        location: '',
        tags: '',
        post_type: 'general'
      })
      
      onPostCreated(response.data)
      onClose()
    } catch (error) {
      console.error('Failed to create post:', error)
      toast.error('Failed to share post. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const addQuickTag = (tag) => {
    const currentTags = formData.tags.split(',').map(t => t.trim()).filter(t => t)
    if (!currentTags.includes(tag)) {
      const newTags = [...currentTags, tag].join(', ')
      handleInputChange('tags', newTags)
    }
  }

  const selectedPostType = postTypes.find(type => type.value === formData.post_type)

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
            className="relative bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-secondary-100 rounded-full flex items-center justify-center">
                  <TreePine className="w-5 h-5 text-secondary-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">Share with Community</h2>
                  <p className="text-sm text-gray-600">Inspire others with your tree journey!</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {/* Post Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  What are you sharing?
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {postTypes.map((type) => (
                    <button
                      key={type.value}
                      type="button"
                      onClick={() => handleInputChange('post_type', type.value)}
                      className={`p-3 border-2 rounded-lg transition-all text-left ${
                        formData.post_type === type.value
                          ? 'border-secondary-500 bg-secondary-50'
                          : 'border-gray-200 hover:border-secondary-300'
                      }`}
                    >
                      <div className="text-lg mb-1">{type.emoji}</div>
                      <div className="text-sm font-medium text-gray-700">{type.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Content */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  What's happening? {selectedPostType?.emoji}
                </label>
                <textarea
                  value={formData.content}
                  onChange={(e) => handleInputChange('content', e.target.value)}
                  placeholder="Share your tree planting journey, tips, or achievements..."
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-transparent resize-none"
                  maxLength={2000}
                />
                <div className="text-right text-xs text-gray-500 mt-1">
                  {formData.content.length}/2000
                </div>
              </div>

              {/* Image URL */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Add a photo (optional)
                </label>
                <div className="relative">
                  <Camera className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="url"
                    value={formData.image_url}
                    onChange={(e) => handleInputChange('image_url', e.target.value)}
                    placeholder="Paste image URL here"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-transparent"
                  />
                </div>
                {formData.image_url && (
                  <div className="mt-3">
                    <img
                      src={formData.image_url}
                      alt="Preview"
                      className="w-full h-32 object-cover rounded-lg"
                      onError={(e) => {
                        e.target.style.display = 'none'
                      }}
                    />
                  </div>
                )}
              </div>

              {/* Location */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location (optional)
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    placeholder="Where are you planting?"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tags (optional)
                </label>
                <div className="relative mb-3">
                  <Hash className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={formData.tags}
                    onChange={(e) => handleInputChange('tags', e.target.value)}
                    placeholder="Add tags separated by commas"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary-500 focus:border-transparent"
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                  {quickTags.map((tag) => (
                    <button
                      key={tag}
                      type="button"
                      onClick={() => addQuickTag(tag)}
                      className="px-3 py-1 text-xs bg-gray-100 hover:bg-secondary-100 text-gray-700 rounded-full transition-colors"
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading || !formData.content.trim()}
                  className="flex-1 bg-secondary-600 hover:bg-secondary-700 text-white px-4 py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <Smile className="w-5 h-5" />
                      <span>Share Post</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

export default CreatePostModal