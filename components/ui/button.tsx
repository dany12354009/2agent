import { Slot } from "@radix-ui/react-slot";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export type ButtonVariant =
  | "primary"
  | "secondary"
  | "ghost"
  | "outline"
  | "danger";

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    "bg-accent text-background hover:bg-[#1bd7cb] shadow-subtle focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60",
  secondary:
    "bg-surface text-text hover:bg-surface/80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40",
  ghost:
    "bg-transparent hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/30",
  outline:
    "border border-border bg-transparent hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/30",
  danger:
    "bg-red-500/80 text-white hover:bg-red-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-400/70",
};

const sizeClasses = {
  sm: "h-9 px-3 text-sm",
  md: "h-11 px-4 text-base",
  lg: "h-12 px-6 text-base",
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: ButtonVariant;
  size?: keyof typeof sizeClasses;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", asChild, ...props }, ref) => {
    const Component = asChild ? Slot : "button";

    return (
      <Component
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all duration-150",
          "disabled:pointer-events-none disabled:opacity-50",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";
