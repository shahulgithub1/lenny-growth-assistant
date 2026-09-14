import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  disabled,
  ...props
}) => {
  const baseStyles = 'font-medium rounded-md transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variantStyles = {
    primary: 'bg-primary text-white hover:bg-primary-hover focus-visible:ring-primary',
    secondary: 'bg-transparent text-text-primary border border-border-primary hover:bg-surface-hover focus-visible:ring-border-focus',
    ghost: 'bg-transparent text-text-secondary hover:bg-bg-tertiary focus-visible:ring-border-focus',
  };
  
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-body',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
