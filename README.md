# 2Agent Marketing & Demo Site

A production-style Next.js experience for 2Agent: a platform where two AI agents debate, plan, code, review, and ship.

## Stack

- Next.js (App Router) with TypeScript
- Tailwind CSS for styling
- Framer Motion micro-animations
- Lucide icons

## Running locally

```bash
pnpm install
pnpm dev
```

> npm or yarn also work if you prefer: replace `pnpm` with your package manager.

The site renders:

- **Home**: hero, how it works, features, pricing teaser.
- **Demo**: fully simulated multi-agent debate with file tree, code viewer, diffs, guardrails, ZIP export.
- **Pricing**: toggle between monthly/yearly plans.
- **Docs**: quickstart, safety overview, and code samples.
- **About**: mission, safety pledge, contact details.
- **Auth**: stubbed magic-link modal.

Keyboard shortcuts in the demo:

- `Cmd/Ctrl + Enter` — start the simulated run.
- `[` and `]` — cycle demo tabs (Debate, Files, Diffs, README).

## Design language

Dark, OpenAI-inspired UI with glass panels, rounded cards, and teal accent.
