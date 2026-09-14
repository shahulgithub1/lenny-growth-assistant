import { QueryClient, QueryClientProvider } from 'react-query';
import { AppProvider, useApp } from './contexts/AppContext';
import { SessionSidebar } from './components/SessionSidebar';
import { ConversationArea } from './components/ConversationArea';
import { ArtifactViewer } from './components/ArtifactViewer';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AppContent() {
  const { isArtifactViewerOpen, isSidebarOpen } = useApp();

  return (
    <div className="flex h-screen bg-bg-primary overflow-hidden">
      {/* Sidebar - hidden on mobile, shown on desktop */}
      <div className={`${isSidebarOpen ? 'block' : 'hidden'} md:block flex-shrink-0`}>
        <SessionSidebar />
      </div>
      
      {/* Main conversation area - responsive with min-width: 0 to prevent overflow */}
      <div className="flex-1 flex min-w-0">
        <ConversationArea />
      </div>
      
      {/* Artifact viewer - slides in on desktop, modal on mobile */}
      {isArtifactViewerOpen && (
        <>
          {/* Mobile: Full-screen modal */}
          <div className="md:hidden fixed inset-0 z-50 bg-surface-base">
            <ArtifactViewer />
          </div>
          
          {/* Desktop: Side panel with min-width: 0 */}
          <div className="hidden md:block flex-shrink-0 min-w-0">
            <ArtifactViewer />
          </div>
        </>
      )}
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </QueryClientProvider>
  );
}

export default App;
