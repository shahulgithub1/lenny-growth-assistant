import React, { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  hover = false,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`
        bg-surface-base border border-border-primary rounded-lg p-6
        shadow-sm
        ${hover ? 'hover:border-border-focus hover:shadow-md transition-all duration-200 cursor-pointer' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
};
