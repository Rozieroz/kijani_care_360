const Logo = ({ size = 'medium', showText = true, className = '' }) => {
  const sizeClasses = {
    small: 'w-8 h-8',
    medium: 'w-10 h-10',
    large: 'w-16 h-16',
    xlarge: 'w-24 h-24'
  }

  const textSizeClasses = {
    small: 'text-lg',
    medium: 'text-xl',
    large: 'text-3xl',
    xlarge: 'text-4xl'
  }
  

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <img 
        src="/logo.png" 
        alt="KijaniCare360 Logo" 
        className={`${sizeClasses[size]} object-contain`}
        onError={(e) => {
          // Fallback to TreePine icon if logo fails to load
          e.target.style.display = 'none'
          e.target.nextSibling.style.display = 'flex'
        }}
      />
      <div 
        className={`${sizeClasses[size]} bg-primary-600 rounded-lg items-center justify-center hidden`}
        style={{ display: 'none' }}
      >
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      </div>
      {showText && (
        <span className={`${textSizeClasses[size]} font-bold gradient-text`}>
          KijaniCare360
        </span>
      )}
    </div>
  )
}

export default Logo