import React, { useEffect } from 'react';
import { useApp } from '../contexts/AppContext';
import { Button } from './Button';
import { apiClient, Session } from '../lib/api';

export const SessionSidebar: React.FC = () => {
  const { currentSession, setCurrentSession, sessions, setSessions, toggleSidebar, isSidebarOpen } = useApp();

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await apiClient.listSessions();
      setSessions(data.sessions);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      const newSession = await apiClient.createSession();
      setSessions([newSession, ...sessions]);
      setCurrentSession(newSession);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const handleSelectSession = async (session: Session) => {
    try {
      const fullSession = await apiClient.getSession(session.id);
      setCurrentSession(fullSession);
    } catch (error) {
      console.error('Failed to load session:', error);
    }
  };

  const handleDeleteSession = async (session: Session) => {
    try {
      await apiClient.deleteSession(session.id);
      
      // Remove from sessions list
      const updatedSessions = sessions.filter(s => s.id !== session.id);
      setSessions(updatedSessions);
      
      // If deleted session was current, navigate to another or clear
      if (currentSession?.id === session.id) {
        if (updatedSessions.length > 0) {
          // Load the most recent session
          const nextSession = await apiClient.getSession(updatedSessions[0].id);
          setCurrentSession(nextSession);
        } else {
          // No sessions left
          setCurrentSession(null);
        }
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
      alert('Failed to delete conversation. Please try again.');
    }
  };

  const groupSessionsByTime = (sessions: Session[]) => {
    const now = new Date();
    const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    return {
      today: sessions.filter(s => new Date(s.updated_at) > oneDayAgo),
      yesterday: sessions.filter(s => {
        const date = new Date(s.updated_at);
        return date <= oneDayAgo && date > sevenDaysAgo;
      }),
      older: sessions.filter(s => new Date(s.updated_at) <= sevenDaysAgo),
    };
  };

  const grouped = groupSessionsByTime(sessions);

  // Only show backdrop on mobile when sidebar is open
  const showBackdrop = isSidebarOpen;

  return (
    <div className="w-full md:w-[280px] bg-bg-secondary border-r border-border-primary h-screen flex flex-col flex-shrink-0">
      {/* Mobile overlay backdrop */}
      {showBackdrop && (
        <div 
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleSidebar}
          aria-hidden="true"
        />
      )}
      
      {/* Sidebar content */}
      <div className="relative z-50 w-full bg-bg-secondary h-full flex flex-col overflow-hidden">
        <div className="p-4 border-b border-border-secondary flex-shrink-0">
          <Button
            onClick={handleNewChat}
            variant="primary"
            className="w-full"
            aria-label="Create new chat session"
          >
            + New Chat
          </Button>
        </div>

      <div className="flex-1 overflow-y-auto min-h-0">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-text-tertiary text-sm">
            <div className="text-2xl mb-2">📚</div>
            <div>No conversations yet</div>
            <div className="mt-1">Click "New Chat" to start</div>
          </div>
        ) : (
          <div className="p-2">
            {grouped.today.length > 0 && (
              <SessionGroup
                title="Today"
                sessions={grouped.today}
                currentSessionId={currentSession?.id}
                onSelect={handleSelectSession}
                onDelete={handleDeleteSession}
              />
            )}
            {grouped.yesterday.length > 0 && (
              <SessionGroup
                title="Last 7 Days"
                sessions={grouped.yesterday}
                currentSessionId={currentSession?.id}
                onSelect={handleSelectSession}
                onDelete={handleDeleteSession}
              />
            )}
            {grouped.older.length > 0 && (
              <SessionGroup
                title="Older"
                sessions={grouped.older}
                currentSessionId={currentSession?.id}
                onSelect={handleSelectSession}
                onDelete={handleDeleteSession}
              />
            )}
          </div>
        )}
      </div>
      </div>
    </div>
  );
};

interface SessionGroupProps {
  title: string;
  sessions: Session[];
  currentSessionId?: string;
  onSelect: (session: Session) => void;
  onDelete: (session: Session) => void;
}

const SessionGroup: React.FC<SessionGroupProps> = ({ title, sessions, currentSessionId, onSelect, onDelete }) => {
  const [menuOpenForSession, setMenuOpenForSession] = React.useState<string | null>(null);
  const [deleteConfirmSession, setDeleteConfirmSession] = React.useState<Session | null>(null);

  const handleDeleteClick = (session: Session, e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpenForSession(null);
    setDeleteConfirmSession(session);
  };

  const handleConfirmDelete = () => {
    if (deleteConfirmSession) {
      onDelete(deleteConfirmSession);
      setDeleteConfirmSession(null);
    }
  };

  const handleCancelDelete = () => {
    setDeleteConfirmSession(null);
  };

  const toggleMenu = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpenForSession(menuOpenForSession === sessionId ? null : sessionId);
  };

  return (
    <div className="mb-4">
      <div className="text-xs font-semibold text-text-tertiary uppercase tracking-wider px-3 py-2">
        {title}
      </div>
      <div className="space-y-1">
        {sessions.map(session => (
          <div key={session.id} className="relative">
            <button
              onClick={() => onSelect(session)}
              className={`
                w-full text-left px-3 py-2.5 rounded-md transition-colors flex items-start justify-between group
                ${currentSessionId === session.id
                  ? 'bg-primary text-white'
                  : 'text-text-primary hover:bg-surface-hover'
                }
              `}
            >
              <div className="flex-1 min-w-0">
                <div className="font-medium text-sm truncate">
                  {session.title || 'New conversation'}
                </div>
                {session.message_count && session.message_count > 0 && (
                  <div className={`text-xs mt-0.5 ${currentSessionId === session.id ? 'text-blue-100' : 'text-text-tertiary'}`}>
                    {session.message_count} {session.message_count === 1 ? 'message' : 'messages'}
                  </div>
                )}
              </div>
              <button
                onClick={(e) => toggleMenu(session.id, e)}
                className={`ml-2 p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 ${
                  currentSessionId === session.id 
                    ? 'hover:bg-blue-600' 
                    : 'hover:bg-bg-tertiary'
                }`}
                aria-label="Session options"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 16 16">
                  <circle cx="8" cy="3" r="1.5" />
                  <circle cx="8" cy="8" r="1.5" />
                  <circle cx="8" cy="13" r="1.5" />
                </svg>
              </button>
            </button>
            
            {/* Dropdown menu */}
            {menuOpenForSession === session.id && (
              <>
                <div 
                  className="fixed inset-0 z-40" 
                  onClick={() => setMenuOpenForSession(null)}
                />
                <div className="absolute right-2 top-full mt-1 bg-surface-base border border-border-primary rounded-md shadow-lg z-50 py-1 min-w-[120px]">
                  <button
                    onClick={(e) => handleDeleteClick(session, e)}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>

      {/* Delete confirmation dialog */}
      {deleteConfirmSession && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
          <div className="bg-surface-base border border-border-primary rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-2">
              Delete conversation?
            </h3>
            <p className="text-sm text-text-secondary mb-6">
              This will permanently delete "{deleteConfirmSession.title || 'New conversation'}" and all its messages. This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <Button variant="ghost" onClick={handleCancelDelete}>
                Cancel
              </Button>
              <Button 
                variant="primary" 
                onClick={handleConfirmDelete}
                className="bg-red-600 hover:bg-red-700"
              >
                Delete
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
