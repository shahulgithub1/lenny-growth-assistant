import React from 'react';
import { LoadingDots } from './LoadingSpinner';

interface LoadingMessageProps {
  stage?: string;
}

export const LoadingMessage: React.FC<LoadingMessageProps> = ({ stage }) => {
  return (
    <div className="flex justify-start mb-8">
      <div className="max-w-[680px] w-full">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0 w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-semibold text-sm mt-1">
            L
          </div>
          <div className="flex-1 bg-ai-bg border border-ai-border rounded-lg px-6 py-4">
            <LoadingDots className="mb-2" />
            <div className="text-sm text-text-secondary mt-2">
              {stage || 'Thinking...'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
