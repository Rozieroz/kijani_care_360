import { useState } from 'react'
// try uncommenting/importing if you keep logo in src/assets
// import localLogo from '../../assets/logo.png'

const Logo = ({ size = 'medium', showText = true, className = '' }) => {
    const [errored, setErrored] = useState(false)

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

    // src import recommended if not using public/
    const srcPath = '/logo.png' // or use localLogo if imported above

    return (
        <div className={`flex items-center space-x-2 ${className}`}>
            {!errored ? (
                <img
                    src={srcPath}
                    alt="KijaniCare360 Logo"
                    className={`${sizeClasses[size]} object-contain`}
                    onLoad={() => console.info('Logo loaded:', srcPath)}
                    onError={(e) => {
                        console.error('Logo load error:', srcPath, e?.nativeEvent || e)
                        setErrored(true)
                    }}
                />
            ) : (
                <div className={`${sizeClasses[size]} bg-primary-600 rounded-lg flex items-center justify-center`}>
                    <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                </div>
            )}

            {showText && (
                <span className={`${textSizeClasses[size]} font-bold gradient-text`}>
                    KijaniCare360
                </span>
            )}
        </div>
    )
}

export default Logo