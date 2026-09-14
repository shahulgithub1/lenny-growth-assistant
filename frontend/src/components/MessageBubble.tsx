import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../lib/api';
import { SourceCard } from './SourceCard';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end mb-4 md:mb-6">
        <div className="max-w-[90%] md:max-w-[680px] bg-bg-tertiary rounded-lg px-4 md:px-6 py-3 md:py-4">
          <div className="text-text-primary whitespace-pre-wrap text-sm md:text-base">{message.content}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-6 md:mb-8">
      <div className="max-w-full md:max-w-[680px] w-full">
        <div className="flex items-start space-x-2 md:space-x-3">
          <div className="flex-shrink-0 w-7 h-7 md:w-8 md:h-8 bg-primary rounded-full flex items-center justify-center text-white font-semibold text-xs md:text-sm mt-1">
            L
          </div>
          <div className="flex-1 bg-ai-bg border border-ai-border rounded-lg px-4 md:px-6 py-3 md:py-4">
            <div className="prose prose-sm max-w-none text-text-primary">
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
                  strong: ({ children }) => <strong className="font-semibold text-text-primary">{children}</strong>,
                  ul: ({ children }) => <ul className="list-disc pl-5 mb-4 space-y-1">{children}</ul>,
                  ol: ({ children }) => <ol className="list-decimal pl-5 mb-4 space-y-1">{children}</ol>,
                  li: ({ children }) => <li className="text-text-primary">{children}</li>,
                  h1: ({ children }) => <h1 className="text-xl font-semibold mb-3 mt-4 first:mt-0">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-lg font-semibold mb-2 mt-3 first:mt-0">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-base font-semibold mb-2 mt-3 first:mt-0">{children}</h3>,
                  code: ({ children }) => (
                    <code className="bg-bg-tertiary px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>
                  ),
                  pre: ({ children }) => (
                    <pre className="bg-bg-tertiary p-4 rounded-md overflow-x-auto mb-4">
                      {children}
                    </pre>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>

            {message.sources && message.sources.length > 0 && (
              <div className="mt-6 pt-4 border-t border-ai-border">
                <div className="text-sm font-medium text-text-secondary mb-3">
                  Sources ({message.sources.length})
                </div>
                <div className="space-y-2">
                  {message.sources.map((source, idx) => (
                    <SourceCard key={`${source.chunk_id}-${idx}`} source={source} />
                  ))}
                </div>
              </div>
            )}

            {message.metadata?.model_provider && message.metadata?.model_name && (
              <div className="flex justify-between items-center mt-4 text-xs text-text-tertiary">
                <div>
                  {message.metadata.model_provider} · {message.metadata.model_name}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
