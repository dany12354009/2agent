import { cn } from "@/lib/utils";

export function Badge({
  children,
  className,
}: React.PropsWithChildren<{ className?: string }>) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border border-accent/50 bg-accent/15 px-3 py-1 text-xs font-medium text-accent",
        className
      )}
    >
      {children}
    </span>
  );
}
