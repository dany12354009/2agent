import { DemoWorkbench } from "@/components/demo-workbench";
import { Badge } from "@/components/ui/badge";
import { ShieldAlert, Zap } from "lucide-react";

export default function DemoPage() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-12 px-6 py-20">
      <section className="space-y-6">
        <Badge className="bg-accent/20 text-accent">Live demo</Badge>
        <h1 className="text-4xl font-semibold text-text">Plan. Code. Review. Ship.</h1>
        <p className="max-w-3xl text-lg text-text-muted">
          Run the simulated 2Agent pipeline. We stream a deterministic debate, code diffs, and review notes to show how two agents collaborate until they ship.
        </p>
        <div className="flex flex-wrap gap-4 text-sm text-text-muted">
          <span className="flex items-center gap-2 rounded-full border border-border/70 bg-surface/70 px-3 py-1">
            <Zap className="h-4 w-4 text-accent" /> Cmd/Ctrl+Enter to run
          </span>
          <span className="flex items-center gap-2 rounded-full border border-border/70 bg-surface/70 px-3 py-1">
            <ShieldAlert className="h-4 w-4 text-accent" /> Guardrails for disallowed prompts
          </span>
        </div>
      </section>
      <DemoWorkbench />
    </div>
  );
}
