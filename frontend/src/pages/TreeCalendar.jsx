import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Calendar as CalendarIcon, 
  ChevronLeft, 
  ChevronRight,
  Plus,
  TreePine,
  Droplets,
  Scissors,
  Leaf,
  Sun,
  Cloud,
  AlertCircle
} from 'lucide-react'
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths } from 'date-fns'
import AddCalendarEventModal from '../components/modals/AddCalendarEventModal'
import api from '../utils/api'
import toast from 'react-hot-toast'

const TreeCalendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [events, setEvents] = useState([])
  const [showAddEvent, setShowAddEvent] = useState(false)

  useEffect(() => {
    fetchCalendarEvents()
  }, [currentDate])

  const fetchCalendarEvents = async () => {
    try {
      const year = currentDate.getFullYear()
      const month = currentDate.getMonth() + 1
      const response = await api.get(`/calendar/events?year=${year}&month=${month}`)
      
      const formattedEvents = response.data.events.map(event => ({
        ...event,
        date: new Date(event.date)
      }))
      
      setEvents(formattedEvents)
    } catch (error) {
      console.error('Failed to fetch calendar events:', error)
      // Fallback to mock data
      setEvents([
        {
          id: 1,
          date: new Date(2024, 0, 15),
          type: 'planting',
          title: 'Plant Mango Seedlings',
          description: 'Best time to plant mango trees in Nairobi region',
          priority: 'high'
        },
        {
          id: 2,
          date: new Date(2024, 0, 18),
          type: 'watering',
          title: 'Water Young Trees',
          description: 'Weekly watering for newly planted trees',
          priority: 'medium'
        }
      ])
    }
  }

  const monthStart = startOfMonth(currentDate)
  const monthEnd = endOfMonth(currentDate)
  const calendarDays = eachDayOfInterval({ start: monthStart, end: monthEnd })

  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1))
  const prevMonth = () => setCurrentDate(subMonths(currentDate, 1))

  const getEventsForDate = (date) => {
    return events.filter(event => isSameDay(event.date, date))
  }

  const getEventIcon = (type) => {
    switch (type) {
      case 'planting': return TreePine
      case 'watering': return Droplets
      case 'pruning': return Scissors
      case 'community': return Leaf
      default: return CalendarIcon
    }
  }

  const getEventColor = (type) => {
    switch (type) {
      case 'planting': return 'bg-primary-500'
      case 'watering': return 'bg-blue-500'
      case 'pruning': return 'bg-yellow-500'
      case 'community': return 'bg-secondary-500'
      default: return 'bg-gray-500'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'border-l-red-500'
      case 'medium': return 'border-l-yellow-500'
      case 'low': return 'border-l-green-500'
      default: return 'border-l-gray-500'
    }
  }

  const selectedDateEvents = getEventsForDate(selectedDate)

  const handleEventAdded = (newEvent) => {
    setEvents(prev => [...prev, newEvent])
    toast.success('Event added to calendar successfully! 📅')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">Tree Care Calendar</h1>
              <p className="text-gray-600">Plan and track your tree conservation activities</p>
            </div>
            <button
              onClick={() => setShowAddEvent(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add Activity</span>
            </button>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Calendar */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-2"
          >
            <div className="card p-6">
              {/* Calendar Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-800">
                  {format(currentDate, 'MMMM yyyy')}
                </h2>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={prevMonth}
                    className="p-2 hover:bg-primary-100 rounded-lg transition-colors"
                  >
                    <ChevronLeft className="w-5 h-5 text-gray-600" />
                  </button>
                  <button
                    onClick={nextMonth}
                    className="p-2 hover:bg-primary-100 rounded-lg transition-colors"
                  >
                    <ChevronRight className="w-5 h-5 text-gray-600" />
                  </button>
                </div>
              </div>

              {/* Calendar Grid */}
              <div className="grid grid-cols-7 gap-1 mb-4">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                  <div key={day} className="p-3 text-center text-sm font-medium text-gray-600">
                    {day}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-7 gap-1">
                {calendarDays.map(day => {
                  const dayEvents = getEventsForDate(day)
                  const isSelected = isSameDay(day, selectedDate)
                  const isToday = isSameDay(day, new Date())

                  return (
                    <div
                      key={day.toString()}
                      onClick={() => setSelectedDate(day)}
                      className={`
                        min-h-[80px] p-2 border border-gray-200 cursor-pointer transition-colors
                        ${isSelected ? 'bg-primary-100 border-primary-300' : 'hover:bg-gray-50'}
                        ${!isSameMonth(day, currentDate) ? 'text-gray-400 bg-gray-50' : ''}
                        ${isToday ? 'bg-primary-50 border-primary-200' : ''}
                      `}
                    >
                      <div className={`text-sm font-medium mb-1 ${isToday ? 'text-primary-600' : ''}`}>
                        {format(day, 'd')}
                      </div>
                      <div className="space-y-1">
                        {dayEvents.slice(0, 2).map(event => {
                          const Icon = getEventIcon(event.type)
                          return (
                            <div
                              key={event.id}
                              className={`text-xs p-1 rounded text-white ${getEventColor(event.type)}`}
                            >
                              <div className="flex items-center space-x-1">
                                <Icon className="w-3 h-3" />
                                <span className="truncate">{event.title}</span>
                              </div>
                            </div>
                          )
                        })}
                        {dayEvents.length > 2 && (
                          <div className="text-xs text-gray-500">
                            +{dayEvents.length - 2} more
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </motion.div>

          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6"
          >
            {/* Selected Date Events */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">
                {format(selectedDate, 'EEEE, MMMM d')}
              </h3>
              {selectedDateEvents.length > 0 ? (
                <div className="space-y-3">
                  {selectedDateEvents.map(event => {
                    const Icon = getEventIcon(event.type)
                    return (
                      <div
                        key={event.id}
                        className={`p-3 border-l-4 bg-gray-50 rounded-r-lg ${getPriorityColor(event.priority)}`}
                      >
                        <div className="flex items-center space-x-2 mb-2">
                          <Icon className="w-4 h-4 text-gray-600" />
                          <span className="font-medium text-gray-800">{event.title}</span>
                        </div>
                        <p className="text-sm text-gray-600">{event.description}</p>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="text-center py-8">
                  <CalendarIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500">No activities scheduled for this date</p>
                  <button
                    onClick={() => setShowAddEvent(true)}
                    className="mt-2 text-primary-600 hover:text-primary-700 text-sm font-medium"
                  >
                    Add an activity
                  </button>
                </div>
              )}
            </div>

            {/* Weather Forecast */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Weather Forecast</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Sun className="w-5 h-5 text-yellow-500" />
                    <span className="text-sm">Today</span>
                  </div>
                  <span className="font-medium">28°C</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Cloud className="w-5 h-5 text-gray-500" />
                    <span className="text-sm">Tomorrow</span>
                  </div>
                  <span className="font-medium">25°C</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Droplets className="w-5 h-5 text-blue-500" />
                    <span className="text-sm">Friday</span>
                  </div>
                  <span className="font-medium">22°C</span>
                </div>
              </div>
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-blue-800 font-medium">Rain expected Friday</span>
                </div>
                <p className="text-xs text-blue-700 mt-1">Perfect time for watering activities!</p>
              </div>
            </div>

            {/* Quick Tips */}
            <div className="card p-6">
              <h3 className="font-semibold text-gray-800 mb-4">January Tips</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-2">
                  <TreePine className="w-4 h-4 text-primary-600 mt-0.5" />
                  <p className="text-sm text-gray-600">
                    Best time to plant indigenous trees in most Kenyan regions
                  </p>
                </div>
                <div className="flex items-start space-x-2">
                  <Droplets className="w-4 h-4 text-blue-600 mt-0.5" />
                  <p className="text-sm text-gray-600">
                    Water young trees daily during dry spells
                  </p>
                </div>
                <div className="flex items-start space-x-2">
                  <Leaf className="w-4 h-4 text-secondary-600 mt-0.5" />
                  <p className="text-sm text-gray-600">
                    Monitor for pests and diseases in humid conditions
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Add Calendar Event Modal */}
      <AddCalendarEventModal
        isOpen={showAddEvent}
        onClose={() => setShowAddEvent(false)}
        onEventAdded={handleEventAdded}
        selectedDate={selectedDate}
      />
    </div>
  )
}

export default TreeCalendar