import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';
import { Button } from './Button';

interface MessageComposerProps {
  onSend: (content: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageComposer: React.FC<MessageComposerProps> = ({
  onSend,
  disabled = false,
  placeholder = 'Type your question...',
}) => {
  const [content, setContent] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (content.trim() && !disabled) {
      onSend(content.trim());
      setContent('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [content]);

  return (
    <div className="border-t border-border-primary bg-surface-base">
      <div className="max-w-4xl mx-auto p-4">
        <div className="flex items-center space-x-3">
          <textarea
            ref={textareaRef}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="
              flex-1 min-w-0 bg-bg-primary border-2 border-border-primary rounded-md
              px-4 py-3 text-body text-text-primary resize-none
              transition-colors duration-150
              placeholder:text-text-tertiary
              focus:outline-none focus:border-border-focus focus:ring-4 focus:ring-blue-50
              disabled:opacity-50 disabled:cursor-not-allowed
            "
            aria-label="Message input"
          />
          <Button
            onClick={handleSend}
            disabled={disabled || !content.trim()}
            className="flex-shrink-0"
          >
            Send
          </Button>
        </div>
        <div className="text-xs text-text-tertiary mt-1.5 ml-1">
          Press Enter to send · Shift + Enter for new line
        </div>
      </div>
    </div>
  );
};
