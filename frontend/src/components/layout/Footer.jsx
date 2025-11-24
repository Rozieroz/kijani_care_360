import { Link } from 'react-router-dom'
import { TreePine, Mail, Phone, MapPin, Github, Twitter, Linkedin } from 'lucide-react'
import Logo from '../ui/Logo'

const Footer = () => {
  return (
    <footer className="bg-primary-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="mb-4">
              <Logo size="medium" showText={true} className="text-white" />
            </div>
            <p className="text-primary-200 mb-4 max-w-md">
              Empowering tree conservation across Kenya through AI-powered guidance, 
              community engagement, and data-driven insights. Building a greener future, 
              one tree at a time.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-primary-300 hover:text-white transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-primary-300 hover:text-white transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="#" className="text-primary-300 hover:text-white transition-colors">
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/analytics" className="text-primary-200 hover:text-white transition-colors">
                  Tree Coverage Data
                </Link>
              </li>
              <li>
                <Link to="/community" className="text-primary-200 hover:text-white transition-colors">
                  Community Forum
                </Link>
              </li>
              <li>
                <Link to="/chatbot" className="text-primary-200 hover:text-white transition-colors">
                  AI Tree Expert
                </Link>
              </li>
              <li>
                <a href="#" className="text-primary-200 hover:text-white transition-colors">
                  Tree Species Guide
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-primary-300" />
                <span className="text-primary-200">info@kijanicare360.com</span>
              </li>
              <li className="flex items-center space-x-2">
                <Phone className="w-4 h-4 text-primary-300" />
                <span className="text-primary-200">+254 700 000 000</span>
              </li>
              <li className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-primary-300" />
                <span className="text-primary-200">Nairobi, Kenya</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-primary-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-primary-300 text-sm">
            © 2024 KijaniCare360. All rights reserved. Building a greener Kenya 🇰🇪
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="text-primary-300 hover:text-white text-sm transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-primary-300 hover:text-white text-sm transition-colors">
              Terms of Service
            </a>
            <a href="#" className="text-primary-300 hover:text-white text-sm transition-colors">
              Support
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer