"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface TabItem {
  value: string;
  label: string;
  badge?: string;
}

interface TabsContextValue {
  value: string;
  setValue: (value: string) => void;
}

const TabsContext = React.createContext<TabsContextValue | undefined>(undefined);

export function Tabs({
  value,
  onValueChange,
  className,
  children,
}: {
  value: string;
  onValueChange: (value: string) => void;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <TabsContext.Provider value={{ value, setValue: onValueChange }}>
      <div className={cn("flex flex-col", className)}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({
  className,
  children,
}: React.PropsWithChildren<{ className?: string }>) {
  return (
    <div
      role="tablist"
      className={cn(
        "mb-4 flex items-center gap-2 rounded-xl border border-border/70 bg-surface/80 p-1",
        className
      )}
    >
      {children}
    </div>
  );
}

export function TabsTrigger({
  value,
  className,
  children,
}: React.PropsWithChildren<{ value: string; className?: string }>) {
  const context = React.useContext(TabsContext);
  if (!context) {
    throw new Error("TabsTrigger must be used within Tabs");
  }
  const isActive = context.value === value;

  return (
    <button
      role="tab"
      type="button"
      onClick={() => context.setValue(value)}
      className={cn(
        "flex-1 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40",
        isActive
          ? "bg-accent/20 text-text"
          : "text-text-muted hover:bg-white/5",
        className
      )}
    >
      {children}
    </button>
  );
}

export function TabsContent({
  value,
  className,
  children,
}: React.PropsWithChildren<{ value: string; className?: string }>) {
  const context = React.useContext(TabsContext);
  if (!context) {
    throw new Error("TabsContent must be used within Tabs");
  }

  if (context.value !== value) return null;

  return <div className={cn(className)}>{children}</div>;
}
