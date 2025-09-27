import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface PricingCardProps {
  name: string;
  price: string;
  cadence: string;
  description: string;
  features: string[];
  highlighted?: boolean;
}

export function PricingCard({
  name,
  price,
  cadence,
  description,
  features,
  highlighted,
}: PricingCardProps) {
  return (
    <div
      className={cn(
        "flex h-full flex-col gap-6 rounded-3xl border border-border/70 bg-surface/80 p-8 shadow-glass",
        highlighted && "border-accent/60 bg-surface/90"
      )}
    >
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold text-text">{name}</h3>
          {highlighted && <Badge className="bg-accent/25 text-accent">Popular</Badge>}
        </div>
        <p className="text-sm text-text-muted">{description}</p>
      </div>
      <div>
        <span className="text-4xl font-semibold text-text">{price}</span>
        <span className="ml-2 text-sm text-text-muted">/{cadence}</span>
      </div>
      <ul className="flex flex-1 flex-col gap-2 text-sm text-text-muted">
        {features.map((feature) => (
          <li key={feature} className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" aria-hidden />
            {feature}
          </li>
        ))}
      </ul>
      <Button variant={highlighted ? "primary" : "secondary"} className="w-full">
        Choose {name}
      </Button>
    </div>
  );
}
