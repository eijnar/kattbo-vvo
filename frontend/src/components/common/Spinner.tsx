import React from 'react';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'; // Small, Medium, Large sizes
  color?: string; // Tailwind color classes (e.g., 'text-blue-500')
  className?: string; // Additional custom classes
}

const Spinner: React.FC<SpinnerProps> = ({ size = 'md', color = 'text-blue-500', className = '' }) => {
  // Determine spinner size based on the 'size' prop
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-16 h-16',
  };

  return (
    <div role="status" className={`flex items-center justify-center ${className}`}>
      <svg
        aria-hidden="true"
        className={`animate-spin ${sizeClasses[size]} ${color}`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8H4z"
        ></path>
      </svg>
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default Spinner;