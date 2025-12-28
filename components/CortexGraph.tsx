import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as d3 from 'd3';
import { ConceptNode, ConceptLink, GraphData } from '../types';

interface CortexGraphProps {
  data: GraphData;
  onNodeClick: (nodeId: string) => void;
  selectedNodeId: string | null;
  width: number;
  height: number;
}

const CortexGraph: React.FC<CortexGraphProps> = ({ data, onNodeClick, selectedNodeId, width, height }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const hoveredNodeRef = useRef<string | null>(null);

  const simulationRef = useRef<d3.Simulation<ConceptNode, ConceptLink> | null>(null);

  // Sync ref with state
  useEffect(() => {
    hoveredNodeRef.current = hoveredNodeId;
  }, [hoveredNodeId]);

  // Helper to check connections
  const isConnected = useCallback((a: ConceptNode, b: ConceptNode) => {
    return data.links.some(l => {
      const sourceId = typeof l.source === 'object' ? (l.source as ConceptNode).id : l.source;
      const targetId = typeof l.target === 'object' ? (l.target as ConceptNode).id : l.target;
      return (
        (sourceId === a.id && targetId === b.id) ||
        (sourceId === b.id && targetId === a.id)
      );
    });
  }, [data.links]);

  // Handle Selection Physics (Re-heat and Center)
  useEffect(() => {
    if (!simulationRef.current) return;

    const simulation = simulationRef.current;

    // If a node is selected, create a force to pull it to center
    if (selectedNodeId) {
      simulation
        .force("center", null) // Disable global centering
        .force("focus", d3.forceRadial(0, width / 2, height / 2).strength((d: any) => d.id === selectedNodeId ? 1.0 : 0.0)) // Pull selected to center strongly
        .force("alignment", d3.forceX(width / 2).strength((d: any) => d.id === selectedNodeId ? 0.5 : 0.05)) // Helper to keep overall structure centered-ish
        .force("alignmentY", d3.forceY(height / 2).strength((d: any) => d.id === selectedNodeId ? 0.5 : 0.05))
        .alpha(0.5) // Re-heat physics
        .restart();
    } else {
      // Reset to default
      simulation
        .force("focus", null)
        .force("alignment", null)
        .force("alignmentY", null)
        .force("center", d3.forceCenter(width / 2, height / 2).strength(0.1))
        .alpha(0.3)
        .restart();
    }

  }, [selectedNodeId, width, height]);

  // Initialize Simulation layout
  useEffect(() => {
    if (!canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Deep copy to protect strict mode props
    const nodes: ConceptNode[] = data.nodes.map(d => ({ ...d }));
    const links: ConceptLink[] = data.links.map(d => ({ ...d }));

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id((d: any) => d.id).distance(220))
      .force("charge", d3.forceManyBody().strength(-600))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius((d: any) => d.val + 20))
      .alphaDecay(0.08); // Faster stabilize

    simulationRef.current = simulation;


    // Animation Loop
    let animationFrameId: number;
    let t = 0;

    const render = () => {
      if (!ctx) return;
      t += 0.05;

      const currentHoverId = hoveredNodeRef.current;

      ctx.clearRect(0, 0, width, height);

      // Draw Links
      links.forEach(link => {
        const source = link.source as ConceptNode;
        const target = link.target as ConceptNode;

        const isHoveredLink = currentHoverId && (
          (source.id === currentHoverId && target.id !== currentHoverId) ||
          (target.id === currentHoverId && source.id !== currentHoverId)
        );

        ctx.beginPath();
        if (source.x !== undefined && source.y !== undefined && target.x !== undefined && target.y !== undefined) {
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
        }

        if (isHoveredLink) {
          ctx.strokeStyle = "rgba(6, 182, 212, 0.8)";
          ctx.lineWidth = 3;
          ctx.shadowBlur = 10;
          ctx.shadowColor = "#06b6d4";
        } else {
          ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
          ctx.lineWidth = 1;
        }
        ctx.stroke();
        ctx.shadowBlur = 0;
      });

      // Draw Nodes
      nodes.forEach(node => {
        if (node.x === undefined || node.y === undefined) return;

        const isHovered = currentHoverId === node.id;

        // Check neighbor
        let isNeighbor = false;
        if (currentHoverId) {
          const hoverNodeObj = nodes.find(n => n.id === currentHoverId);
          if (hoverNodeObj) isNeighbor = isConnected(node, hoverNodeObj);
        }

        const baseRadius = node.val;
        const breathing = Math.sin(t + (node.index || 0) * 0.5) * 2;
        const radius = isHovered ? baseRadius * 1.3 : baseRadius + breathing;

        ctx.beginPath();
        ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);

        if (isHovered) {
          ctx.fillStyle = "#06b6d4";
          ctx.shadowBlur = 30;
          ctx.shadowColor = "#06b6d4";
        } else if (isNeighbor) {
          ctx.fillStyle = "#a855f7";
          ctx.shadowBlur = 15;
          ctx.shadowColor = "#a855f7";
        } else {
          ctx.fillStyle = "#1e293b";
          ctx.strokeStyle = "#06b6d4";
          ctx.lineWidth = 1.5;
          ctx.shadowBlur = 10;
          ctx.shadowColor = "rgba(6, 182, 212, 0.3)";
        }

        ctx.fill();
        if (!isHovered && !isNeighbor) ctx.stroke();

        ctx.shadowBlur = 0;
        ctx.fillStyle = isHovered || isNeighbor ? "#ffffff" : "rgba(255, 255, 255, 0.6)";
        ctx.font = isHovered ? "bold 14px Roboto Mono" : "12px Roboto Mono";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.id, node.x, node.y + radius + 15);
      });

      animationFrameId = requestAnimationFrame(render);
    };

    simulation.on("tick", render);

    return () => {
      cancelAnimationFrame(animationFrameId);
      simulation.stop();
    };
  }, [width, height, data, isConnected]); // Hover removed from dependencies

  // Handlers
  const handleMouseMove = (e: React.MouseEvent) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect || !simulationRef.current) return;

    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const nodes = simulationRef.current.nodes();
    let found: string | null = null;

    for (const node of nodes) {
      if (node.x !== undefined && node.y !== undefined) {
        const dx = mouseX - node.x;
        const dy = mouseY - node.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        // Generous hit area
        if (dist < node.val + 10) {
          found = node.id;
          break;
        }
      }
    }

    if (found !== hoveredNodeRef.current) {
      setHoveredNodeId(found);
    }

    if (canvasRef.current) {
      canvasRef.current.style.cursor = found ? 'pointer' : 'default';
    }
  };

  const handleClick = () => {
    if (hoveredNodeId) {
      onNodeClick(hoveredNodeId);
    }
  };

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      className="absolute top-0 left-0 w-full h-full"
      onMouseMove={handleMouseMove}
      onClick={handleClick}
      onMouseLeave={() => setHoveredNodeId(null)}
    />
  );
};

export default CortexGraph;