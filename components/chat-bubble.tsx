import { cn } from "@/lib/utils";

const roleStyles: Record<string, string> = {
  Architect: "from-accent/60 to-accent/10",
  Coder: "from-purple-500/60 to-purple-500/10",
  Reviewer: "from-amber-500/60 to-amber-500/10",
};

const roleInitials: Record<string, string> = {
  Architect: "A",
  Coder: "C",
  Reviewer: "R",
};

export interface ChatBubbleProps {
  role: "Architect" | "Coder" | "Reviewer";
  message: string;
  timestamp?: string;
}

export function ChatBubble({ role, message, timestamp }: ChatBubbleProps) {
  return (
    <div className="flex gap-3">
      <div
        className={cn(
          "flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-br text-sm font-semibold text-background",
          roleStyles[role]
        )}
      >
        {roleInitials[role]}
      </div>
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-text">{role}</span>
          {timestamp && <span className="text-xs text-text-muted">{timestamp}</span>}
        </div>
        <p className="whitespace-pre-wrap text-sm text-text-muted">{message}</p>
      </div>
    </div>
  );
}
