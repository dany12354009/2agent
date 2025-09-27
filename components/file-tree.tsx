"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import type { FileNode } from "@/types/files";

interface FileTreeProps {
  nodes: FileNode[];
  activePath?: string;
  onSelect?: (node: FileNode) => void;
}

export function FileTree({ nodes, activePath, onSelect }: FileTreeProps) {
  const [expanded, setExpanded] = React.useState<Record<string, boolean>>({});

  const toggle = (path: string) => {
    setExpanded((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  const handleKey = (event: React.KeyboardEvent<HTMLDivElement>, node: FileNode) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (node.type === "folder") {
        toggle(node.path);
      } else {
        onSelect?.(node);
      }
    }
    if (event.key === "ArrowRight" && node.type === "folder") {
      event.preventDefault();
      setExpanded((prev) => ({ ...prev, [node.path]: true }));
    }
    if (event.key === "ArrowLeft" && node.type === "folder") {
      event.preventDefault();
      setExpanded((prev) => ({ ...prev, [node.path]: false }));
    }
  };

  return (
    <div className="space-y-1 text-sm text-text-muted">
      {nodes.map((node) => (
        <TreeNode
          key={node.path}
          node={node}
          depth={0}
          expanded={expanded}
          toggle={toggle}
          activePath={activePath}
          onSelect={onSelect}
          onKey={handleKey}
        />
      ))}
    </div>
  );
}

function TreeNode({
  node,
  depth,
  expanded,
  toggle,
  activePath,
  onSelect,
  onKey,
}: {
  node: FileNode;
  depth: number;
  expanded: Record<string, boolean>;
  toggle: (path: string) => void;
  activePath?: string;
  onSelect?: (node: FileNode) => void;
  onKey: (event: React.KeyboardEvent<HTMLDivElement>, node: FileNode) => void;
}) {
  const isFolder = node.type === "folder";
  const isExpanded = expanded[node.path];
  return (
    <div>
      <div
        role="treeitem"
        tabIndex={0}
        aria-expanded={isFolder ? isExpanded : undefined}
        onKeyDown={(event) => onKey(event, node)}
        onClick={() => {
          if (isFolder) {
            toggle(node.path);
          } else {
            onSelect?.(node);
          }
        }}
        className={cn(
          "flex cursor-pointer items-center justify-between rounded-lg px-2 py-1.5 transition-colors",
          activePath === node.path
            ? "bg-accent/15 text-text"
            : "hover:bg-white/5"
        )}
        style={{ paddingLeft: depth * 16 + 8 }}
      >
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase tracking-wide text-text-muted/80">
            {isFolder ? (isExpanded ? "▾" : "▸") : "•"}
          </span>
          <span className="font-mono text-xs text-text">{node.name}</span>
        </div>
      </div>
      {isFolder && isExpanded && node.children && (
        <div role="group" className="mt-1 space-y-1">
          {node.children.map((child) => (
            <TreeNode
              key={child.path}
              node={child}
              depth={depth + 1}
              expanded={expanded}
              toggle={toggle}
              activePath={activePath}
              onSelect={onSelect}
              onKey={onKey}
            />
          ))}
        </div>
      )}
    </div>
  );
}
