import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import DOMPurify from 'dompurify';
import { Artifact } from '../lib/api';
import { Button } from './Button';
import { useApp } from '../contexts/AppContext';

export const ArtifactViewer: React.FC = () => {
  const { currentArtifact, closeArtifactViewer, isArtifactViewerOpen } = useApp();
  const [viewMode, setViewMode] = useState<'preview' | 'code'>('preview');

  if (!isArtifactViewerOpen || !currentArtifact) {
    return null;
  }

  const handleCopyCode = () => {
    navigator.clipboard.writeText(currentArtifact.content);
  };

  return (
    <div className="w-full md:w-[500px] border-l border-border-primary bg-surface-base flex flex-col h-screen min-w-0 overflow-hidden">
      {/* Header */}
      <div className="border-b border-border-primary p-3 md:p-4 flex-shrink-0">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1 min-w-0">
            <h2 className="text-lg font-semibold text-text-primary truncate">
              {currentArtifact.metadata?.title || 'Artifact'}
            </h2>
            <p className="text-sm text-text-secondary">
              {currentArtifact.type.toUpperCase()} Artifact
            </p>
          </div>
          <button
            onClick={closeArtifactViewer}
            className="ml-3 text-text-secondary hover:text-text-primary p-1 rounded hover:bg-bg-tertiary flex-shrink-0"
            aria-label="Close artifact viewer"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex space-x-2">
          <Button
            variant={viewMode === 'preview' ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setViewMode('preview')}
          >
            Preview
          </Button>
          <Button
            variant={viewMode === 'code' ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setViewMode('code')}
          >
            Code
          </Button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto min-h-0">
        {viewMode === 'preview' ? (
          <ArtifactPreview artifact={currentArtifact} />
        ) : (
          <ArtifactCode content={currentArtifact.content} type={currentArtifact.type} onCopy={handleCopyCode} />
        )}
      </div>
    </div>
  );
};

interface ArtifactPreviewProps {
  artifact: Artifact;
}

const ArtifactPreview: React.FC<ArtifactPreviewProps> = ({ artifact }) => {
  if (artifact.type === 'markdown') {
    return (
      <div className="p-4 md:p-6 prose prose-sm max-w-none">
        <ReactMarkdown>{artifact.content}</ReactMarkdown>
      </div>
    );
  }

  if (artifact.type === 'html' || artifact.type === 'css') {
    // Sanitize HTML to remove dangerous content
    const sanitizedHTML = DOMPurify.sanitize(artifact.content, {
      ALLOWED_TAGS: [
        'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'a', 'strong', 'em', 'br', 'hr',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'img', 'section', 'article', 'header', 'footer', 'nav',
        'style', 'svg', 'path', 'circle', 'rect', 'line',
      ],
      ALLOWED_ATTR: ['class', 'id', 'style', 'href', 'src', 'alt', 'title', 'width', 'height', 'viewBox', 'fill', 'stroke'],
      ALLOW_DATA_ATTR: false,
    });

    return (
      <div className="w-full h-full">
        <iframe
          sandbox="allow-same-origin"
          srcDoc={sanitizedHTML}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            backgroundColor: 'white',
          }}
          title="Artifact Preview"
        />
      </div>
    );
  }

  return (
    <div className="p-6 text-center text-text-secondary">
      <p>Preview not available for this artifact type</p>
    </div>
  );
};

interface ArtifactCodeProps {
  content: string;
  type: string;
  onCopy: () => void;
}

const ArtifactCode: React.FC<ArtifactCodeProps> = ({ content, onCopy }) => {
  return (
    <div className="relative">
      <div className="absolute top-4 right-4 z-10">
        <Button variant="secondary" size="sm" onClick={onCopy}>
          Copy Code
        </Button>
      </div>
      <pre className="p-6 text-sm overflow-auto bg-bg-tertiary">
        <code className="font-mono text-text-primary">{content}</code>
      </pre>
    </div>
  );
};
