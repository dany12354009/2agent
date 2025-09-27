"use client";

import * as React from "react";
import { PricingCard } from "@/components/pricing-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const plans = {
  monthly: [
    {
      name: "Free",
      price: "$0",
      cadence: "month",
      description: "For experiments and quick spikes.",
      features: ["3 debates/day", "Community workspace", "Public builds"],
    },
    {
      name: "Pro",
      price: "$29",
      cadence: "month",
      description: "Ship production features with guardrails.",
      features: ["Unlimited debates", "Parallel test runner", "Private repos"],
      highlighted: true,
    },
    {
      name: "Team",
      price: "$99",
      cadence: "seat",
      description: "For squads that want CI-integrated agents.",
      features: ["Org workspaces", "SSO + SCIM", "Branch rules"],
    },
  ],
  yearly: [
    {
      name: "Free",
      price: "$0",
      cadence: "month",
      description: "For experiments and quick spikes.",
      features: ["3 debates/day", "Community workspace", "Public builds"],
    },
    {
      name: "Pro",
      price: "$24",
      cadence: "month",
      description: "Ship production features with guardrails.",
      features: ["Unlimited debates", "Parallel test runner", "Private repos"],
      highlighted: true,
    },
    {
      name: "Team",
      price: "$79",
      cadence: "seat",
      description: "For squads that want CI-integrated agents.",
      features: ["Org workspaces", "SSO + SCIM", "Branch rules"],
    },
  ],
};

export default function PricingPage() {
  const [billing, setBilling] = React.useState<"monthly" | "yearly">("monthly");

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-12 px-6 py-20">
      <section className="space-y-6 text-center">
        <Badge className="bg-accent/20 text-accent">Pricing</Badge>
        <h1 className="text-4xl font-semibold text-text">Choose your loop cadence</h1>
        <p className="mx-auto max-w-2xl text-lg text-text-muted">
          Predictable billing, no usage surprises. Switch between monthly and yearly to see what fits your team.
        </p>
        <div className="mx-auto flex items-center justify-center gap-3 rounded-full border border-border/70 bg-surface/80 p-1">
          <Button
            type="button"
            variant={billing === "monthly" ? "primary" : "ghost"}
            size="sm"
            className="px-6"
            onClick={() => setBilling("monthly")}
          >
            Monthly
          </Button>
          <Button
            type="button"
            variant={billing === "yearly" ? "primary" : "ghost"}
            size="sm"
            className="px-6"
            onClick={() => setBilling("yearly")}
          >
            Yearly <span className="ml-2 rounded-full bg-accent/20 px-2 text-xs text-accent">Save 20%</span>
          </Button>
        </div>
      </section>
      <section className="grid gap-6 md:grid-cols-3">
        {plans[billing].map((plan) => (
          <PricingCard key={plan.name} {...plan} />
        ))}
      </section>
    </div>
  );
}
