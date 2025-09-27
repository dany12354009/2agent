"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Copy, WrapText } from "lucide-react";
import { useToast } from "@/components/toaster";

interface CodeViewerProps {
  code: string;
  language?: string;
  className?: string;
}

export function CodeViewer({ code, language = "tsx", className }: CodeViewerProps) {
  const [wrap, setWrap] = React.useState(false);
  const { publish } = useToast();

  const lines = React.useMemo(() => code.split(/\r?\n/), [code]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    publish({ title: "Copied", description: `${language.toUpperCase()} snippet copied.` });
  };

  return (
    <div className={cn("space-y-3", className)}>
      <div className="flex items-center justify-between">
        <span className="rounded-full border border-border/70 bg-surface/80 px-3 py-1 text-xs font-medium uppercase tracking-wide text-text-muted">
          {language}
        </span>
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => setWrap((prev) => !prev)}
            className="h-9 px-3 text-xs uppercase text-text-muted"
          >
            <WrapText className="h-4 w-4" /> {wrap ? "No wrap" : "Wrap"}
          </Button>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="h-9 px-3 text-xs uppercase text-text-muted"
          >
            <Copy className="h-4 w-4" /> Copy
          </Button>
        </div>
      </div>
      <pre
        className={cn(
          "relative overflow-auto rounded-2xl border border-border/70 bg-[#0c1218] p-4 font-mono text-sm text-text",
          wrap ? "whitespace-pre-wrap" : "whitespace-pre"
        )}
      >
        {lines.map((line, index) => (
          <div key={index} className="flex">
            <span className="w-12 shrink-0 select-none pr-4 text-right text-xs text-text-muted/70">
              {index + 1}
            </span>
            <code className="flex-1">{line || "\u00A0"}</code>
          </div>
        ))}
      </pre>
    </div>
  );
}
