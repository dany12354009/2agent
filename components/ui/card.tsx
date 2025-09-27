import { cn } from "@/lib/utils";

export function Card({
  className,
  children,
}: React.PropsWithChildren<{ className?: string }>) {
  return (
    <div
      className={cn(
        "glass-panel rounded-2xl border border-border/70 shadow-glass",
        className
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className,
  children,
}: React.PropsWithChildren<{ className?: string }>) {
  return (
    <div className={cn("p-6 pb-3", className)}>
      {children}
    </div>
  );
}

export function CardContent({
  className,
  children,
}: React.PropsWithChildren<{ className?: string }>) {
  return <div className={cn("px-6 pb-6", className)}>{children}</div>;
}
