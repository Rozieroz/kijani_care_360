import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  X, 
  Users, 
  Copy,
  Mail,
  MessageCircle,
  Share2,
  Check,
  UserPlus
} from 'lucide-react'
import api from '../../utils/api'
import toast from 'react-hot-toast'

const InviteToStreakModal = ({ isOpen, onClose, groupData }) => {
  const [inviteLink, setInviteLink] = useState('')
  const [emailInvites, setEmailInvites] = useState('')
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(false)

  const generateInviteLink = async () => {
    try {
      const response = await api.post(`/social/streak/groups/${groupData?.group_id}/invite-link`)
      setInviteLink(response.data.invite_link)
    } catch (error) {
      console.error('Failed to generate invite link:', error)
      // Fallback link for demo
      setInviteLink(`https://kijanicare360.com/join-streak/${groupData?.group_id || 'demo'}`)
    }
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(inviteLink)
      setCopied(true)
      toast.success('Invite link copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
      toast.error('Failed to copy link')
    }
  }

  const sendEmailInvites = async () => {
    if (!emailInvites.trim()) {
      toast.error('Please enter at least one email address')
      return
    }

    setLoading(true)
    try {
      const emails = emailInvites.split(',').map(email => email.trim()).filter(email => email)
      await api.post(`/social/streak/groups/${groupData?.group_id}/invite-emails`, {
        emails: emails
      })
      toast.success(`Invitations sent to ${emails.length} email${emails.length !== 1 ? 's' : ''}!`)
      setEmailInvites('')
    } catch (error) {
      console.error('Failed to send email invites:', error)
      toast.error('Failed to send invitations')
    } finally {
      setLoading(false)
    }
  }

  const shareViaWhatsApp = () => {
    const message = `Join my tree planting streak group "${groupData?.group_name || 'Tree Warriors'}" on KijaniCare360! Let's plant trees together and make a difference. ${inviteLink}`
    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`
    window.open(whatsappUrl, '_blank')
  }

  const shareViaTwitter = () => {
    const message = `Join my tree planting streak group "${groupData?.group_name || 'Tree Warriors'}" on @KijaniCare360! 🌱 Let's plant trees together and fight climate change. ${inviteLink} #TreePlanting #ClimateAction`
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}`
    window.open(twitterUrl, '_blank')
  }

  // Generate invite link when modal opens
  useState(() => {
    if (isOpen && !inviteLink) {
      generateInviteLink()
    }
  }, [isOpen])

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
                  <UserPlus className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">Invite Friends</h2>
                  <p className="text-sm text-gray-600">
                    Invite friends to join "{groupData?.group_name || 'your streak group'}"
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Invite Link */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Share Invite Link
                </label>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={inviteLink}
                    readOnly
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm"
                    placeholder="Generating invite link..."
                  />
                  <button
                    onClick={copyToClipboard}
                    disabled={!inviteLink}
                    className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white rounded-lg transition-colors flex items-center space-x-2"
                  >
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    <span>{copied ? 'Copied!' : 'Copy'}</span>
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Anyone with this link can join your streak group
                </p>
              </div>

              {/* Social Sharing */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Share on Social Media
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={shareViaWhatsApp}
                    disabled={!inviteLink}
                    className="flex items-center justify-center space-x-2 p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <MessageCircle className="w-5 h-5 text-green-600" />
                    <span className="text-sm font-medium">WhatsApp</span>
                  </button>
                  <button
                    onClick={shareViaTwitter}
                    disabled={!inviteLink}
                    className="flex items-center justify-center space-x-2 p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <Share2 className="w-5 h-5 text-blue-500" />
                    <span className="text-sm font-medium">Twitter</span>
                  </button>
                </div>
              </div>

              {/* Email Invites */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Invite by Email
                </label>
                <textarea
                  value={emailInvites}
                  onChange={(e) => setEmailInvites(e.target.value)}
                  placeholder="Enter email addresses separated by commas&#10;e.g., friend1@email.com, friend2@email.com"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
                <button
                  onClick={sendEmailInvites}
                  disabled={loading || !emailInvites.trim()}
                  className="mt-3 w-full bg-secondary-600 hover:bg-secondary-700 disabled:opacity-50 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <Mail className="w-4 h-4" />
                  )}
                  <span>{loading ? 'Sending...' : 'Send Invitations'}</span>
                </button>
              </div>

              {/* Group Info */}
              <div className="bg-primary-50 p-4 rounded-lg">
                <h4 className="font-medium text-primary-800 mb-2">About This Group</h4>
                <div className="space-y-1 text-sm text-primary-700">
                  <p>• Track tree planting activities together</p>
                  <p>• Maintain collaborative streaks</p>
                  <p>• Motivate each other to reach goals</p>
                  <p>• Share achievements and progress</p>
                </div>
              </div>

              {/* Current Members */}
              {groupData?.group_members && groupData.group_members.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3">
                    Current Members ({groupData.group_members.length})
                  </h4>
                  <div className="space-y-2">
                    {groupData.group_members.slice(0, 3).map((member) => (
                      <div key={member.id} className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-sm">
                          {member.avatar}
                        </div>
                        <span className="text-sm text-gray-700">{member.name}</span>
                      </div>
                    ))}
                    {groupData.group_members.length > 3 && (
                      <p className="text-xs text-gray-500 ml-11">
                        +{groupData.group_members.length - 3} more members
                      </p>
                    )}
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

export default InviteToStreakModal