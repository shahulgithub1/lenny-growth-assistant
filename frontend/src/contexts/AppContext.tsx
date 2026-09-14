import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Session, Artifact } from '../lib/api';

interface AppContextType {
  currentSession: Session | null;
  setCurrentSession: (session: Session | null) => void;
  sessions: Session[];
  setSessions: (sessions: Session[]) => void;
  currentArtifact: Artifact | null;
  setCurrentArtifact: (artifact: Artifact | null) => void;
  isArtifactViewerOpen: boolean;
  openArtifactViewer: (artifact: Artifact) => void;
  closeArtifactViewer: () => void;
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentArtifact, setCurrentArtifact] = useState<Artifact | null>(null);
  const [isArtifactViewerOpen, setIsArtifactViewerOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const openArtifactViewer = useCallback((artifact: Artifact) => {
    setCurrentArtifact(artifact);
    setIsArtifactViewerOpen(true);
  }, []);

  const closeArtifactViewer = useCallback(() => {
    setIsArtifactViewerOpen(false);
    // Keep artifact for a moment to allow smooth close animation
    setTimeout(() => setCurrentArtifact(null), 300);
  }, []);

  const toggleSidebar = useCallback(() => {
    setIsSidebarOpen(prev => !prev);
  }, []);

  return (
    <AppContext.Provider
      value={{
        currentSession,
        setCurrentSession,
        sessions,
        setSessions,
        currentArtifact,
        setCurrentArtifact,
        isArtifactViewerOpen,
        openArtifactViewer,
        closeArtifactViewer,
        isSidebarOpen,
        toggleSidebar,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
