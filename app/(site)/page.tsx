import Link from "next/link";
import { Button } from "@/components/ui/button";
import { DemoTeaser } from "@/components/demo-teaser";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Shield, GitBranch, FileDiff, PlayCircle, Terminal, Download } from "lucide-react";

const loop = [
  {
    title: "Architect",
    description: "Scopes the build, aligns on requirements, and issues instructions to the coder.",
  },
  {
    title: "Coder",
    description: "Writes diffs, updates files, and reruns tests until the reviewer is satisfied.",
  },
  {
    title: "Reviewer",
    description: "Audits changes, runs checks, and keeps the loop safe before shipping.",
  },
];

const features = [
  {
    title: "Debate Log",
    description: "Transparent reasoning between agents.",
    icon: Terminal,
  },
  {
    title: "Code Diffs",
    description: "See exactly what changed.",
    icon: FileDiff,
  },
  {
    title: "Tests",
    description: "Failing tests loop back into fixes.",
    icon: PlayCircle,
  },
  {
    title: "One-Click Export",
    description: "Download ZIP + README.",
    icon: Download,
  },
  {
    title: "Guardrails",
    description: "Safety by design.",
    icon: Shield,
  },
  {
    title: "Branches",
    description: "Ship PRs with clean history.",
    icon: GitBranch,
  },
];

const logos = ["Linear", "Vercel", "Cursor", "Replit", "Anthropic", "GitHub"];

export default function HomePage() {
  return (
    <div className="relative overflow-hidden">
      <div className="mx-auto flex max-w-6xl flex-col gap-24 px-6 py-24">
        <section className="grid gap-16 lg:grid-cols-[1.2fr_1fr] lg:items-center">
          <div className="space-y-8">
            <Badge className="bg-accent/20 text-accent">Two AIs. One repo.</Badge>
            <h1 className="text-5xl font-semibold leading-tight text-text">
              Two AIs. <span className="text-gradient">One repo.</span>
            </h1>
            <p className="max-w-xl text-lg text-text-muted">
              2Agent plans, debates, codes, and reviews until it ships. Give the prompt once—our agents loop until the Reviewer approves.
            </p>
            <div className="flex flex-col gap-4 sm:flex-row">
              <Button asChild className="h-12 px-6 text-base">
                <Link href="/demo">Start a build</Link>
              </Button>
              <Button asChild variant="ghost" className="h-12 px-6 text-base text-text">
                <Link href="/demo">View demo</Link>
              </Button>
            </div>
            <div className="flex flex-wrap gap-6 text-xs uppercase tracking-[0.2em] text-text-muted/80">
              {logos.map((logo) => (
                <span key={logo}>{logo}</span>
              ))}
            </div>
          </div>
          <DemoTeaser />
        </section>

        <section className="space-y-8">
          <div className="flex items-center justify-between">
            <h2 className="text-3xl font-semibold text-text">How it works</h2>
            <Link href="/docs" className="text-sm text-accent">
              Read the docs <ArrowRight className="ml-2 inline h-4 w-4" />
            </Link>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {loop.map((step) => (
              <div key={step.title} className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
                <h3 className="text-xl font-semibold text-text">{step.title}</h3>
                <p className="mt-3 text-sm text-text-muted">{step.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-10">
          <h2 className="text-3xl font-semibold text-text">Everything in the loop</h2>
          <div className="grid gap-6 md:grid-cols-2">
            {features.map(({ title, description, icon: Icon }) => (
              <div
                key={title}
                className="flex gap-4 rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-accent/15 text-accent">
                  <Icon className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-text">{title}</h3>
                  <p className="mt-2 text-sm text-text-muted">{description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-8 rounded-3xl border border-border/70 bg-surface/80 p-8 shadow-glass md:grid-cols-2">
          <div>
            <h2 className="text-3xl font-semibold text-text">Pricing</h2>
            <p className="mt-2 text-sm text-text-muted">Simple tiers for hobbyists, pros, and teams.</p>
            <Button asChild variant="secondary" className="mt-6">
              <Link href="/pricing">Explore pricing</Link>
            </Button>
          </div>
          <div className="grid gap-4 text-sm text-text-muted">
            <div className="rounded-2xl border border-border/60 bg-background/40 p-4">
              <strong className="text-text">Free</strong> — short runs, small projects
            </div>
            <div className="rounded-2xl border border-border/60 bg-background/40 p-4">
              <strong className="text-text">Pro</strong> — longer debates, test runner, private repos
            </div>
            <div className="rounded-2xl border border-border/60 bg-background/40 p-4">
              <strong className="text-text">Team</strong> — SSO, CI integration, org dashboards
            </div>
          </div>
        </section>

        <section className="rounded-3xl border border-border/70 bg-gradient-to-br from-accent/20 via-transparent to-surface/90 p-10 shadow-subtle">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-3xl font-semibold text-text">Ready to ship with agents?</h2>
              <p className="mt-2 text-sm text-text-muted">Drop a prompt, watch the debate, and merge when you\'re convinced.</p>
            </div>
            <Button asChild className="h-12 px-8 text-base">
              <Link href="/demo">Start a build</Link>
            </Button>
          </div>
        </section>
      </div>
    </div>
  );
}
