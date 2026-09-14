import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', className = '' }) => {
  const sizeStyles = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  return (
    <div className={`inline-block ${sizeStyles[size]} ${className}`}>
      <div className="w-full h-full border-3 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>
  );
};

export const LoadingDots: React.FC<{ className?: string }> = ({ className = '' }) => {
  return (
    <div className={`flex space-x-1 ${className}`}>
      <div className="w-2 h-2 bg-text-tertiary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
      <div className="w-2 h-2 bg-text-tertiary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
      <div className="w-2 h-2 bg-text-tertiary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
    </div>
  );
};
