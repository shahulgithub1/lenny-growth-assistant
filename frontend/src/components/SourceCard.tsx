import React from 'react';
import { Source } from '../lib/api';

interface SourceCardProps {
  source: Source;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source }) => {
  return (
    <div className="bg-source-bg border border-source-border rounded-md p-3 hover:shadow-sm transition-shadow">
      <div className="flex items-start space-x-2">
        <span className="text-lg flex-shrink-0">📄</span>
        <div className="flex-1 min-w-0">
          <div className="font-medium text-source-text text-sm">
            {source.episode_title}
            {source.guest && <span className="font-normal"> · {source.guest}</span>}
          </div>
          {source.excerpt && (
            <p className="text-sm text-source-text mt-1.5 italic line-clamp-3">
              "{source.excerpt}"
            </p>
          )}
        </div>
      </div>
    </div>
  );
};
