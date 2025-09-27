import * as React from "react";
import { cn } from "@/lib/utils";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", ...props }, ref) => {
    return (
      <input
        type={type}
        ref={ref}
        className={cn(
          "flex h-11 w-full rounded-xl border border-border/60 bg-surface/70 px-4 text-base text-text placeholder:text-text-muted/70",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40",
          "transition-colors duration-150",
          className
        )}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";
