import React from 'react';
import { Card } from './Card';

interface EmptyStateProps {
  onExampleClick?: (prompt: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onExampleClick }) => {
  const examples = [
    'How should a startup improve retention?',
    'What does product-market fit look like?',
    'What are the key principles of growth loops?',
    'Turn this into a Ship 30 essay',
  ];

  return (
    <div className="flex items-center justify-center min-h-[50vh] md:min-h-[60vh] px-4">
      <div className="max-w-2xl w-full text-center">
        <div className="text-5xl md:text-6xl mb-4 md:mb-6">🔷</div>
        <h1 className="text-2xl md:text-3xl font-semibold text-text-primary mb-2 md:mb-3">
          The Lenny Growth Assistant
        </h1>
        <p className="text-base md:text-lg text-text-secondary mb-8 md:mb-12 max-w-lg mx-auto leading-relaxed px-4">
          Your research assistant for product and growth strategy, grounded in Lenny Rachitsky's podcast library.
        </p>

        <div className="border-t border-border-secondary pt-6 md:pt-8 mb-6 md:mb-8">
          <div className="text-sm font-medium text-text-secondary mb-3 md:mb-4">
            Try asking:
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-3">
            {examples.map((example, idx) => (
              <Card
                key={idx}
                hover
                onClick={() => onExampleClick?.(example)}
                className="text-left p-4 text-sm text-text-primary"
              >
                {example}
              </Card>
            ))}
          </div>
        </div>

        <div className="text-xs text-text-tertiary">
          Powered by Claude Agent SDK and Lenny's Podcast Transcripts
        </div>
      </div>
    </div>
  );
};
