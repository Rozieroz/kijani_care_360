import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  TreePine, 
  Leaf, 
  Users, 
  BarChart3, 
  MessageCircle, 
  Calendar,
  ArrowRight,
  CheckCircle,
  Globe,
  Shield,
  Zap
} from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: MessageCircle,
      title: 'AI Tree Expert',
      description: 'Get personalized advice on tree species, planting techniques, and care from our AI-powered forestry expert.',
      color: 'text-primary-600'
    },
    {
      icon: Calendar,
      title: 'Smart Planting Calendar',
      description: 'Never miss the perfect planting season with our intelligent calendar based on Kenyan climate patterns.',
      color: 'text-secondary-600'
    },
    {
      icon: Users,
      title: 'Community Network',
      description: 'Connect with fellow tree enthusiasts, share experiences, and collaborate on conservation projects.',
      color: 'text-accent-600'
    },
    {
      icon: BarChart3,
      title: 'Impact Analytics',
      description: 'Track your environmental impact and see real-time data on Kenya\'s forest coverage and restoration efforts.',
      color: 'text-primary-600'
    }
  ]

  const stats = [
    { number: '10M+', label: 'Trees Planted', icon: TreePine },
    { number: '47', label: 'Counties Covered', icon: Globe },
    { number: '50K+', label: 'Active Users', icon: Users },
    { number: '200+', label: 'Tree Species', icon: Leaf }
  ]

  const benefits = [
    'Expert guidance for optimal tree survival rates',
    'Climate-specific planting recommendations',
    'Community-driven conservation efforts',
    'Real-time environmental impact tracking',
    'Native species preservation programs',
    'Sustainable forestry practices'
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section role="region" aria-label="Hero" className="relative bg-gradient-to-br from-emerald-50 via-white to-emerald-200">
        <div aria-hidden="true" className="absolute inset-0 eco-pattern opacity-30 pointer-events-none"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold mb-6">
                <span className="text-gray-800">Reforest Kenya</span>
                <br />
                <span className="text-gray-800">One Tree at a Time</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Join Kenya's largest tree conservation platform. Get AI-powered guidance, 
                connect with your community, and make a lasting environmental impact.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/register"
                  className="btn-primary text-lg px-8 py-4 flex items-center justify-center space-x-2"
                >
                  <span>Start Planting Today</span>
                  <TreePine className="w-5 h-5" />
                </Link>
                <Link
                  to="/analytics"
                  className="btn-outline text-lg px-8 py-4 flex items-center justify-center space-x-2"
                >
                  <span>View Impact Data</span>
                  <BarChart3 className="w-5 h-5" />
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="w-8 h-8 text-primary-600" />
                </div>
                <div className="text-3xl font-bold text-primary-600 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-br from-primary-50 to-secondary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-4">
              Everything You Need for Successful Tree Conservation
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our comprehensive platform combines AI technology, community wisdom, 
              and scientific data to maximize your environmental impact.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="card p-8 hover:scale-105 transition-transform duration-300"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br from-primary-100 to-secondary-100 flex items-center justify-center mb-6`}>
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-4">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-6">
                Why Choose KijaniCare360?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                We're not just another environmental app. We're Kenya's most comprehensive 
                tree conservation platform, built by Kenyans for Kenyans.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={benefit}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    className="flex items-center space-x-3"
                  >
                    <CheckCircle className="w-5 h-5 text-primary-600 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="grid grid-cols-2 gap-6"
            >
              <div className="space-y-6">
                <div className="card p-6 text-center">
                  <Shield className="w-8 h-8 text-primary-600 mx-auto mb-3" />
                  <h4 className="font-semibold text-gray-800 mb-2">Trusted Platform</h4>
                  <p className="text-sm text-gray-600">Verified by Kenya Forest Service</p>
                </div>
                <div className="card p-6 text-center">
                  <Zap className="w-8 h-8 text-secondary-600 mx-auto mb-3" />
                  <h4 className="font-semibold text-gray-800 mb-2">Fast Results</h4>
                  <p className="text-sm text-gray-600">See impact within weeks</p>
                </div>
              </div>
              <div className="space-y-6">
                <div className="card p-6 text-center">
                  <Globe className="w-8 h-8 text-accent-600 mx-auto mb-3" />
                  <h4 className="font-semibold text-gray-800 mb-2">National Reach</h4>
                  <p className="text-sm text-gray-600">All 47 counties covered</p>
                </div>
                <div className="card p-6 text-center">
                  <Users className="w-8 h-8 text-primary-600 mx-auto mb-3" />
                  <h4 className="font-semibold text-gray-800 mb-2">Strong Community</h4>
                  <p className="text-sm text-gray-600">50,000+ active members</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-600 to-teal-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Make a Difference?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join thousands of Kenyans who are already transforming our environment. 
              Your journey to a greener Kenya starts today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-white text-primary-600 hover:bg-primary-50 font-medium py-3 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <span>Get Started Free</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/analytics"
                className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-medium py-3 px-8 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
              >
                <span>Explore Data</span>
                <BarChart3 className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home