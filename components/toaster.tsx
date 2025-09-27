"use client";

import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import { cn } from "@/lib/utils";

export interface ToastItem {
  id: string;
  title: string;
  description?: string;
  variant?: "default" | "success" | "error";
}

type ToastContextValue = {
  toasts: ToastItem[];
  publish: (toast: Omit<ToastItem, "id">) => void;
  dismiss: (id: string) => void;
};

const ToastContext = React.createContext<ToastContextValue | undefined>(undefined);

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within <Toaster />");
  }
  return context;
}

export function Toaster({ children }: { children?: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastItem[]>([]);

  const publish = React.useCallback((toast: Omit<ToastItem, "id">) => {
    setToasts((current) => {
      const id = crypto.randomUUID();
      return [...current, { ...toast, id }];
    });
  }, []);

  const dismiss = React.useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, publish, dismiss }}>
      {children}
      <div className="pointer-events-none fixed bottom-6 right-6 z-50 flex w-full max-w-sm flex-col gap-3">
        <AnimatePresence initial={false}>
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              layout
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 16 }}
              transition={{ duration: 0.18 }}
            >
              <button
                onClick={() => dismiss(toast.id)}
                className={cn(
                  "pointer-events-auto flex w-full flex-col gap-1 rounded-2xl border border-border/60 bg-surface/90 p-4 text-left shadow-lg",
                  toast.variant === "success" && "border-accent/50",
                  toast.variant === "error" && "border-red-500/60"
                )}
              >
                <span className="text-sm font-semibold text-text">{toast.title}</span>
                {toast.description && (
                  <span className="text-xs text-text-muted">{toast.description}</span>
                )}
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}
