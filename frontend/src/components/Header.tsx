import React from 'react';
import { useApp } from '../contexts/AppContext';

export const Header: React.FC = () => {
  const { toggleSidebar, isSidebarOpen } = useApp();

  return (
    <header className="md:hidden bg-surface-base border-b border-border-primary px-4 py-3 flex items-center justify-between">
      <button
        onClick={toggleSidebar}
        className="p-2 hover:bg-bg-tertiary rounded-md"
        aria-label={isSidebarOpen ? 'Close sidebar' : 'Open sidebar'}
      >
        <svg className="w-6 h-6 text-text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      
      <div className="flex items-center space-x-2">
        <span className="text-xl">🔷</span>
        <span className="font-semibold text-text-primary">Lenny Assistant</span>
      </div>
      
      <div className="w-10"></div> {/* Spacer for centering */}
    </header>
  );
};
