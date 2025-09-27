"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface DiffViewerProps {
  diff: string;
  className?: string;
}

export function DiffViewer({ diff, className }: DiffViewerProps) {
  const lines = React.useMemo(() => diff.split(/\r?\n/), [diff]);

  return (
    <div
      className={cn(
        "overflow-hidden rounded-2xl border border-border/70 bg-[#0c1218] font-mono text-sm text-text",
        className
      )}
    >
      <div className="max-h-[340px] overflow-auto">
        {lines.map((line, index) => {
          const isAddition = line.startsWith("+");
          const isRemoval = line.startsWith("-");
          const isMeta = line.startsWith("@@") || line.startsWith("diff") || line.startsWith("index");

          return (
            <div
              key={index}
              className={cn(
                "flex items-start gap-3 px-4 py-1.5",
                isAddition && "bg-emerald-500/10 text-emerald-200",
                isRemoval && "bg-red-500/10 text-red-200",
                isMeta && "bg-surface/80 text-text"
              )}
            >
              <span className="w-10 shrink-0 text-right text-xs text-text-muted/70">
                {index + 1}
              </span>
              <code className="flex-1 whitespace-pre-wrap">{line || "\u00A0"}</code>
            </div>
          );
        })}
      </div>
    </div>
  );
}
