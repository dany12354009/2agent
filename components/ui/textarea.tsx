import * as React from "react";
import { cn } from "@/lib/utils";

export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={cn(
          "min-h-[160px] w-full rounded-xl border border-border/60 bg-surface/80 px-4 py-3 text-base text-text placeholder:text-text-muted/70",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40",
          "transition-colors duration-150",
          className
        )}
        {...props}
      />
    );
  }
);

Textarea.displayName = "Textarea";
