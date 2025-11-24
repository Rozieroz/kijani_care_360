import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  TrendingUp, 
  TreePine, 
  Globe, 
  MapPin,
  Calendar,
  Download,
  Filter,
  Info
} from 'lucide-react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement } from 'chart.js'
import { Bar, Line, Doughnut } from 'react-chartjs-2'
import api from '../utils/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement)

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('year')
  const [selectedCounty, setSelectedCounty] = useState('all')
  const [analyticsData, setAnalyticsData] = useState({})

  useEffect(() => {
    fetchAnalyticsData()
  }, [timeRange, selectedCounty])

  const fetchAnalyticsData = async () => {
    try {
      const response = await api.get(`/frontend-analytics/dashboard-data?time_range=${timeRange}&county=${selectedCounty}`)
      setAnalyticsData(response.data)
    } catch (error) {
      console.error('Failed to fetch analytics data:', error)
      // Fallback to mock data
      setAnalyticsData({
        overview: {
          totalTrees: 2847293,
          forestCoverage: 8.83,
          carbonOffset: 156789,
          activeProjects: 342
        },
        countyData: [
          { name: 'Nairobi', trees: 45678, coverage: 12.5, change: 2.3 },
          { name: 'Kiambu', trees: 78234, coverage: 18.7, change: 4.1 },
          { name: 'Nakuru', trees: 56789, coverage: 15.2, change: 1.8 },
          { name: 'Mombasa', trees: 23456, coverage: 8.9, change: 3.2 },
          { name: 'Kisumu', trees: 34567, coverage: 11.4, change: 2.7 }
        ],
        monthlyPlanting: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [{
            label: 'Trees Planted',
            data: [12000, 15000, 25000, 35000, 28000, 18000, 15000, 20000, 30000, 40000, 32000, 22000],
            backgroundColor: 'rgba(34, 197, 94, 0.8)',
            borderColor: 'rgba(34, 197, 94, 1)',
            borderWidth: 2
          }]
        },
        speciesDistribution: {
          labels: ['Indigenous', 'Fruit Trees', 'Exotic', 'Bamboo', 'Others'],
          datasets: [{
            data: [45, 25, 15, 10, 5],
            backgroundColor: [
              'rgba(34, 197, 94, 0.8)',
              'rgba(132, 204, 22, 0.8)',
              'rgba(234, 179, 8, 0.8)',
              'rgba(59, 130, 246, 0.8)',
              'rgba(156, 163, 175, 0.8)'
            ],
            borderWidth: 2
          }]
        },
        survivalRate: {
          labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
          datasets: [{
            label: 'Survival Rate (%)',
            data: [72, 75, 78, 82, 85, 88],
            borderColor: 'rgba(34, 197, 94, 1)',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            tension: 0.4,
            fill: true
          }]
        }
      })
    }
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  }

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
      },
    },
  }

  const counties = [
    'All Counties', 'Nairobi', 'Kiambu', 'Nakuru', 'Mombasa', 'Kisumu', 
    'Machakos', 'Kajiado', 'Murang\'a', 'Nyeri', 'Laikipia'
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">Kenya Forest Analytics</h1>
              <p className="text-gray-600">Real-time data on Kenya's tree conservation efforts</p>
            </div>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <select
                value={selectedCounty}
                onChange={(e) => setSelectedCounty(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                {counties.map((county) => (
                  <option key={county} value={county.toLowerCase().replace(' ', '-')}>
                    {county}
                  </option>
                ))}
              </select>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="month">This Month</option>
                <option value="quarter">This Quarter</option>
                <option value="year">This Year</option>
                <option value="all">All Time</option>
              </select>
              <button className="btn-outline flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </motion.div>

        {/* Overview Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Trees Planted</p>
                <p className="text-2xl font-bold text-primary-600">
                  {analyticsData.overview?.totalTrees?.toLocaleString()}
                </p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +12.5% this year
                </p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <TreePine className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Forest Coverage</p>
                <p className="text-2xl font-bold text-secondary-600">
                  {analyticsData.overview?.forestCoverage}%
                </p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +0.8% this year
                </p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-full flex items-center justify-center">
                <Globe className="w-6 h-6 text-secondary-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Carbon Offset (tons)</p>
                <p className="text-2xl font-bold text-accent-600">
                  {analyticsData.overview?.carbonOffset?.toLocaleString()}
                </p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +18.3% this year
                </p>
              </div>
              <div className="w-12 h-12 bg-accent-100 rounded-full flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-accent-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Active Projects</p>
                <p className="text-2xl font-bold text-primary-700">
                  {analyticsData.overview?.activeProjects}
                </p>
                <p className="text-xs text-green-600 flex items-center mt-1">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +25 this month
                </p>
              </div>
              <div className="w-12 h-12 bg-primary-200 rounded-full flex items-center justify-center">
                <MapPin className="w-6 h-6 text-primary-700" />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Charts Grid */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Monthly Planting Trends */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Monthly Planting Trends</h2>
              <Info className="w-5 h-5 text-gray-400" />
            </div>
            {analyticsData.monthlyPlanting && (
              <Bar data={analyticsData.monthlyPlanting} options={chartOptions} />
            )}
          </motion.div>

          {/* Tree Survival Rate */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Tree Survival Rate</h2>
              <Info className="w-5 h-5 text-gray-400" />
            </div>
            {analyticsData.survivalRate && (
              <Line data={analyticsData.survivalRate} options={chartOptions} />
            )}
          </motion.div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Species Distribution */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Species Distribution</h2>
              <Info className="w-5 h-5 text-gray-400" />
            </div>
            {analyticsData.speciesDistribution && (
              <Doughnut data={analyticsData.speciesDistribution} options={doughnutOptions} />
            )}
          </motion.div>

          {/* County Rankings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="lg:col-span-2 card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Top Performing Counties</h2>
              <Info className="w-5 h-5 text-gray-400" />
            </div>
            <div className="space-y-4">
              {analyticsData.countyData?.map((county, index) => (
                <div key={county.name} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {index + 1}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800">{county.name}</h3>
                      <p className="text-sm text-gray-600">{county.coverage}% forest coverage</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center space-x-1 text-primary-600 font-semibold">
                      <TreePine className="w-4 h-4" />
                      <span>{county.trees.toLocaleString()}</span>
                    </div>
                    <p className="text-xs text-green-600 flex items-center justify-end">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      +{county.change}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Key Insights */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 card p-6"
        >
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Key Insights</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-4 bg-primary-50 rounded-lg">
              <h3 className="font-semibold text-primary-800 mb-2">Seasonal Patterns</h3>
              <p className="text-sm text-primary-700">
                Peak planting occurs during March-May (long rains) with 40% higher success rates.
              </p>
            </div>
            <div className="p-4 bg-secondary-50 rounded-lg">
              <h3 className="font-semibold text-secondary-800 mb-2">Species Success</h3>
              <p className="text-sm text-secondary-700">
                Indigenous species show 25% better survival rates compared to exotic varieties.
              </p>
            </div>
            <div className="p-4 bg-accent-50 rounded-lg">
              <h3 className="font-semibold text-accent-800 mb-2">Regional Leaders</h3>
              <p className="text-sm text-accent-700">
                Central Kenya counties lead in both planting volume and survival rates.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Analytics