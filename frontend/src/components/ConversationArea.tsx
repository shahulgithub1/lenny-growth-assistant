import React, { useState, useEffect, useRef } from 'react';
import { useApp } from '../contexts/AppContext';
import { apiClient, Message, Session } from '../lib/api';
import { EmptyState } from './EmptyState';
import { MessageBubble } from './MessageBubble';
import { MessageComposer } from './MessageComposer';
import { LoadingMessage } from './LoadingMessage';
import { ErrorMessage } from './ErrorMessage';

export const ConversationArea: React.FC = () => {
  const { currentSession, setCurrentSession, sessions, setSessions } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (currentSession?.messages) {
      setMessages(currentSession.messages);
    } else {
      setMessages([]);
    }
    setError(null);
  }, [currentSession]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (content: string) => {
    if (!currentSession) {
      // Create new session if none exists
      try {
        const newSession = await apiClient.createSession();
        setCurrentSession(newSession);
        setSessions([newSession, ...sessions]);
        // Continue with sending the message
        await sendMessageToSession(newSession.id, content);
      } catch (err) {
        setError('Failed to create session. Please try again.');
        console.error(err);
      }
      return;
    }

    await sendMessageToSession(currentSession.id, content);
  };

  const sendMessageToSession = async (sessionId: string, content: string) => {
    setIsLoading(true);
    setError(null);

    // Add user message optimistically
    const userMessage: Message = {
      id: `temp-user-${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await apiClient.sendMessage(sessionId, {
        content,
        model_provider: 'ollama', // Can be made configurable
      });

      // Remove temp user message and add assistant response
      // (The backend stores both user and assistant messages, but only returns the assistant message)
      const finalUserMessage = { ...userMessage, id: `user-${Date.now()}` };
      
      setMessages(prev => {
        const withoutTemp = prev.filter(m => m.id !== userMessage.id);
        return [...withoutTemp, finalUserMessage, response];
      });

      // Update session with messages and title
      if (currentSession) {
        // Get the updated messages list for the session
        const updatedMessages = messages.filter(m => m.id !== userMessage.id).concat([finalUserMessage, response]);
        
        const title = messages.length === 0 
          ? content.slice(0, 60) + (content.length > 60 ? '...' : '')
          : currentSession.title;
        
        const updatedSession: Session = { 
          ...currentSession, 
          title, 
          message_count: (currentSession.message_count || 0) + 2,
          messages: updatedMessages
        };
        setCurrentSession(updatedSession);
        setSessions(
          sessions.map((s: Session) => (s.id === sessionId ? updatedSession : s))
        );
      }
    } catch (err: any) {
      setError(
        err.response?.data?.message ||
        'Failed to send message. Please check that the backend and Ollama are running.'
      );
      // Remove the optimistic user message on error
      setMessages(prev => prev.filter(m => m.id !== userMessage.id));
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (prompt: string) => {
    handleSendMessage(prompt);
  };

  const handleRetry = () => {
    setError(null);
    // Could implement retry logic here
  };

  if (!currentSession) {
    return (
      <div className="flex-1 flex flex-col h-screen min-w-0">
        <EmptyState onExampleClick={handleExampleClick} />
        <MessageComposer onSend={handleSendMessage} disabled={isLoading} />
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-screen min-w-0">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto p-4 md:p-6">
          {messages.length === 0 && !isLoading ? (
            <EmptyState onExampleClick={handleExampleClick} />
          ) : (
            <>
              {messages.map(message => (
                <MessageBubble key={message.id} message={message} />
              ))}
              {isLoading && <LoadingMessage stage="Searching Lenny's transcripts..." />}
              {error && <ErrorMessage message={error} onRetry={handleRetry} />}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>
      <MessageComposer onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
};
