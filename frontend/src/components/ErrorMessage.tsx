import React from 'react';
import { Button } from './Button';

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'Something went wrong',
  message,
  onRetry,
}) => {
  return (
    <div className="flex justify-center mb-8">
      <div className="max-w-[680px] w-full">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <span className="text-2xl">⚠️</span>
            <div className="flex-1">
              <h3 className="font-semibold text-red-900 mb-1">{title}</h3>
              <p className="text-sm text-red-700 mb-4">{message}</p>
              {onRetry && (
                <Button variant="secondary" size="sm" onClick={onRetry}>
                  Retry
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
