import { TreePine } from 'lucide-react'

const PlaceholderImage = ({ width = 400, height = 300, className = '', alt = "Placeholder" }) => {
  return (
    <div 
      className={`bg-gradient-to-br from-primary-100 to-secondary-100 flex items-center justify-center ${className}`}
      style={{ width: `${width}px`, height: `${height}px` }}
    >
      <div className="text-center">
        <TreePine className="w-12 h-12 text-primary-600 mx-auto mb-2" />
        <p className="text-sm text-primary-700 font-medium">Tree Conservation</p>
        <p className="text-xs text-primary-600">Image Coming Soon</p>
      </div>
    </div>
  )
}

export default PlaceholderImage