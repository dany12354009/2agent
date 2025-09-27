import { demoEvents } from "@/data/demo-run";
import { ChatBubble } from "@/components/chat-bubble";
import { formatTimestamp } from "@/lib/utils";

export function DemoTeaser() {
  return (
    <div className="rounded-3xl border border-border/60 bg-surface/80 p-6 shadow-glass">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-text">Agent loop</h3>
          <p className="text-sm text-text-muted">Architect → Coder → Reviewer</p>
        </div>
        <span className="rounded-full border border-accent/50 bg-accent/15 px-3 py-1 text-xs font-medium text-accent">
          Live demo preview
        </span>
      </div>
      <div className="space-y-4">
        {demoEvents.slice(0, 3).map((event) => (
          <ChatBubble
            key={event.id}
            role={event.role}
            message={event.message}
            timestamp={formatTimestamp(new Date(`2020-01-01T${event.timestamp}:00`))}
          />
        ))}
      </div>
    </div>
  );
}
