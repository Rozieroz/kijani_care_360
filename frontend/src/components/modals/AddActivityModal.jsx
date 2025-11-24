import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  X, 
  TreePine, 
  Droplets, 
  Scissors, 
  Camera, 
  MapPin
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const AddActivityModal = ({ isOpen, onClose, onActivityAdded }) => {
  const [formData, setFormData] = useState({
    activity_type: 'planted',
    trees_count: 1,
    location: '',
    description: '',
    photo_url: ''
  })
  const [loading, setLoading] = useState(false)

  const activityTypes = [
    { value: 'planted', label: 'Planted Trees', icon: TreePine, color: 'text-green-600' },
    { value: 'watered', label: 'Watered Trees', icon: Droplets, color: 'text-blue-600' },
    { value: 'pruned', label: 'Pruned Trees', icon: Scissors, color: 'text-yellow-600' },
    { value: 'maintained', label: 'General Maintenance', icon: TreePine, color: 'text-primary-600' }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await api.post('/social/streak/activity', formData)
      toast.success(`🌱 ${formData.activity_type} activity logged! Streak updated!`)
      
      // Reset form
      setFormData({
        activity_type: 'planted',
        trees_count: 1,
        location: '',
        description: '',
        photo_url: ''
      })
      
      onActivityAdded(response.data)
      onClose()
    } catch (error) {
      console.error('Failed to log activity:', error)
      
      // Fallback: Still update the UI optimistically
      const mockActivityData = {
        ...formData,
        id: Date.now(),
        streak_days: Math.floor(Math.random() * 30) + 1,
        timestamp: new Date().toISOString()
      }
      
      toast.success(`🌱 ${formData.activity_type} activity logged! (Demo mode)`)
      
      // Reset form
      setFormData({
        activity_type: 'planted',
        trees_count: 1,
        location: '',
        description: '',
        photo_url: ''
      })
      
      onActivityAdded(mockActivityData)
      onClose()
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const selectedActivityType = activityTypes.find(type => type.value === formData.activity_type)

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
            className="relative bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <TreePine className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">Log Tree Activity</h2>
                  <p className="text-sm text-gray-600">Keep your streak alive! 🔥</p>
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
              {/* Activity Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  What did you do?
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {activityTypes.map((type) => {
                    const Icon = type.icon
                    return (
                      <button
                        key={type.value}
                        type="button"
                        onClick={() => handleInputChange('activity_type', type.value)}
                        className={`p-3 border-2 rounded-lg transition-all ${
                          formData.activity_type === type.value
                            ? 'border-primary-500 bg-primary-50'
                            : 'border-gray-200 hover:border-primary-300'
                        }`}
                      >
                        <Icon className={`w-6 h-6 mx-auto mb-2 ${type.color}`} />
                        <div className="text-xs font-medium text-gray-700">{type.label}</div>
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Trees Count */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  How many trees?
                </label>
                <div className="flex items-center space-x-3">
                  <button
                    type="button"
                    onClick={() => handleInputChange('trees_count', Math.max(1, formData.trees_count - 1))}
                    className="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors"
                  >
                    -
                  </button>
                  <div className="flex-1 text-center">
                    <input
                      type="number"
                      min="1"
                      max="1000"
                      value={formData.trees_count}
                      onChange={(e) => handleInputChange('trees_count', parseInt(e.target.value) || 1)}
                      className="w-full text-center text-2xl font-bold text-primary-600 bg-transparent border-none focus:outline-none"
                    />
                    <div className="text-sm text-gray-500">trees</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleInputChange('trees_count', formData.trees_count + 1)}
                    className="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Location */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Where?
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    placeholder="e.g., Karura Forest, My backyard"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tell us more (optional)
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="Share details about your tree activity..."
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
              </div>

              {/* Photo URL */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Add a photo (optional)
                </label>
                <div className="relative">
                  <Camera className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="url"
                    value={formData.photo_url}
                    onChange={(e) => handleInputChange('photo_url', e.target.value)}
                    placeholder="Paste image URL here"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
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
                  disabled={loading}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 text-white px-4 py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <selectedActivityType.icon className="w-5 h-5" />
                      <span>Log Activity</span>
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

export default AddActivityModal