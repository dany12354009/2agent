import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const commitments = [
  {
    title: "Mission",
    copy: "Give every developer a multi-agent teammate that debates, plans, and ships production-quality work.",
  },
  {
    title: "Safety",
    copy: "We model guardrails in every loop. Sensitive prompts are refused, and reviewers enforce policy before shipping.",
  },
  {
    title: "Contact",
    copy: "Reach us at founders@2agent.dev for enterprise pilots, research, or integrations.",
  },
];

export default function AboutPage() {
  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-12 px-6 py-20">
      <section className="space-y-6">
        <Badge className="bg-accent/20 text-accent">About</Badge>
        <h1 className="text-4xl font-semibold text-text">Trust the loop</h1>
        <p className="max-w-3xl text-lg text-text-muted">
          2Agent started as an experiment inside a developer tools lab. We pair two specialized models—the Architect and the Coder—with a ruthless Reviewer that protects your repo.
        </p>
      </section>
      <section className="grid gap-6 md:grid-cols-3">
        {commitments.map((item) => (
          <div key={item.title} className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
            <h2 className="text-xl font-semibold text-text">{item.title}</h2>
            <p className="mt-3 text-sm text-text-muted">{item.copy}</p>
          </div>
        ))}
      </section>
      <section className="rounded-3xl border border-border/70 bg-surface/80 p-10 shadow-glass">
        <h2 className="text-3xl font-semibold text-text">Build with confidence</h2>
        <p className="mt-3 max-w-2xl text-sm text-text-muted">
          Our deployment pipeline signs every artifact, stores debate logs for audit, and integrates with your existing branch protections.
        </p>
        <Button asChild className="mt-6">
          <a href="mailto:founders@2agent.dev">Talk with us</a>
        </Button>
      </section>
    </div>
  );
}
