"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  side?: "top" | "bottom" | "left" | "right";
}

export function Tooltip({ content, children, side = "top" }: TooltipProps) {
  const [open, setOpen] = React.useState(false);
  const timeout = React.useRef<NodeJS.Timeout | null>(null);

  const handleOpen = () => {
    if (timeout.current) clearTimeout(timeout.current);
    setOpen(true);
  };

  const handleClose = () => {
    timeout.current = setTimeout(() => setOpen(false), 80);
  };

  return (
    <span className="relative inline-flex">
      {React.cloneElement(children, {
        onMouseEnter: handleOpen,
        onMouseLeave: handleClose,
        onFocus: handleOpen,
        onBlur: handleClose,
      })}
      {open && (
        <span
          role="tooltip"
          className={cn(
            "pointer-events-none absolute z-40 rounded-lg border border-border/70 bg-surface/90 px-3 py-1 text-xs text-text",
            "shadow-glass",
            side === "top" && "bottom-full left-1/2 mb-2 -translate-x-1/2",
            side === "bottom" && "left-1/2 top-full mt-2 -translate-x-1/2",
            side === "left" && "right-full top-1/2 mr-2 -translate-y-1/2",
            side === "right" && "left-full top-1/2 ml-2 -translate-y-1/2"
          )}
        >
          {content}
        </span>
      )}
    </span>
  );
}
