'use client';

interface LogoProps {
  className?: string;
  showText?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const sizes = {
  sm: { container: 'w-7 h-7', text: 'text-lg' },
  md: { container: 'w-8 h-8', text: 'text-xl' },
  lg: { container: 'w-12 h-12', text: 'text-2xl' },
};

export default function Logo({ className = '', showText = true, size = 'md' }: LogoProps) {
  const sizeClasses = sizes[size];

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Logo SVG */}
      <div className={`${sizeClasses.container} relative`}>
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#2563eb" />
              <stop offset="100%" stopColor="#7c3aed" />
            </linearGradient>
          </defs>
          
          {/* Background rounded square */}
          <rect x="5" y="5" width="90" height="90" rx="18" fill="url(#logoGradient)"/>
          
          {/* Brain/AI Network Nodes */}
          <circle cx="50" cy="35" r="6" fill="white"/>
          <circle cx="35" cy="50" r="5" fill="white" opacity="0.9"/>
          <circle cx="65" cy="50" r="5" fill="white" opacity="0.9"/>
          <circle cx="42" cy="68" r="4" fill="white" opacity="0.8"/>
          <circle cx="58" cy="68" r="4" fill="white" opacity="0.8"/>
          
          {/* Neural connections */}
          <line x1="50" y1="35" x2="35" y2="50" stroke="white" strokeWidth="2" opacity="0.6"/>
          <line x1="50" y1="35" x2="65" y2="50" stroke="white" strokeWidth="2" opacity="0.6"/>
          <line x1="35" y1="50" x2="42" y2="68" stroke="white" strokeWidth="2" opacity="0.5"/>
          <line x1="65" y1="50" x2="58" y2="68" stroke="white" strokeWidth="2" opacity="0.5"/>
          <line x1="35" y1="50" x2="65" y2="50" stroke="white" strokeWidth="1.5" opacity="0.4"/>
          
          {/* Stock chart arrow trending up */}
          <path d="M28 72 L38 62 L48 68 L58 52 L72 38" stroke="white" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
          <polygon points="72,38 68,42 66,36" fill="white"/>
        </svg>
      </div>

      {/* Logo Text */}
      {showText && (
        <span className={`font-bold ${sizeClasses.text} text-gray-900 dark:text-white tracking-tight`}>
          StockSense<span className="text-blue-600 dark:text-blue-400">AI</span>
        </span>
      )}
    </div>
  );
}
