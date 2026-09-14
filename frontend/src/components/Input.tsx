import { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-text-primary mb-2">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={`
            w-full bg-bg-primary border-2 border-border-primary rounded-md
            px-4 py-3 text-body text-text-primary
            transition-colors duration-150
            placeholder:text-text-tertiary
            focus:outline-none focus:border-border-focus focus:ring-4 focus:ring-blue-50
            disabled:opacity-50 disabled:cursor-not-allowed
            ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-50' : ''}
            ${className}
          `}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
