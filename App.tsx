import React, { useState, useEffect, useRef } from 'react';
import CortexGraph from './components/CortexGraph';
import ReaderPanel from './components/ReaderPanel';
import HUD from './components/HUD';
import { INITIAL_GRAPH_DATA, BOOK_CONTENT } from './constants';
import { Upload, FileText, Loader2 } from 'lucide-react';

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [loading, setLoading] = useState(false);
  const [fileLoaded, setFileLoaded] = useState(true); // Default to true for the prototype demo
  const graphContainerRef = useRef<HTMLDivElement>(null);

  // Resize handler for Canvas
  useEffect(() => {
    const handleResize = () => {
      if (graphContainerRef.current) {
        setDimensions({
          width: graphContainerRef.current.clientWidth,
          height: graphContainerRef.current.clientHeight
        });
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleNodeClick = (nodeId: string) => {
    setSelectedNodeId(nodeId);
  };

  const handleFileUpload = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setFileLoaded(true);
    }, 1500);
  };

  return (
    <div className="flex h-screen w-screen bg-[#050505] text-white overflow-hidden relative selection:bg-cyan-500/30">

      {/* Background Grid */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0)`,
          backgroundSize: '40px 40px'
        }}>
      </div>

      {/* Main Graph Area */}
      <div className="relative flex-1 h-full" ref={graphContainerRef}>
        <HUD resonance={selectedNodeId ? 98 : 45} />

        {fileLoaded ? (
          <CortexGraph
            data={INITIAL_GRAPH_DATA}
            onNodeClick={handleNodeClick}
            selectedNodeId={selectedNodeId}
            width={dimensions.width}
            height={dimensions.height}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            {loading ? (
              <div className="flex flex-col items-center gap-4">
                <Loader2 className="w-12 h-12 text-cyan-500 animate-spin" />
                <span className="text-cyan-500 font-mono animate-pulse">ANALYZING NEURAL PATHWAYS...</span>
              </div>
            ) : (
              <div className="text-center p-8 border border-white/10 rounded-lg bg-white/5 backdrop-blur-sm max-w-md">
                <FileText className="w-16 h-16 text-neutral-500 mx-auto mb-4" />
                <h1 className="text-2xl font-mono text-white mb-2">RESONANT READER</h1>
                <p className="text-neutral-400 mb-6">Upload a document to visualize its semantic topology.</p>
                <button
                  onClick={handleFileUpload}
                  className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-black font-bold rounded-sm flex items-center gap-2 mx-auto transition-all hover:shadow-[0_0_20px_rgba(6,182,212,0.4)]"
                >
                  <Upload className="w-5 h-5" />
                  UPLOAD PDF
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Sidebar - only visible if file loaded */}
      {fileLoaded && (
        <div className="w-[450px] relative z-10 shadow-2xl">
          <ReaderPanel sections={BOOK_CONTENT} selectedNodeId={selectedNodeId} />
        </div>
      )}

      {/* Footer / Overlay details */}
      <div className="absolute bottom-6 left-6 text-xs font-mono text-neutral-600 pointer-events-none">
        COGNITIVE_LAYER: ACTIVE <br />
        RENDER: CANVAS_WEBGL <br />
        SESSION: 0x4F2A1
      </div>

    </div>
  );
}