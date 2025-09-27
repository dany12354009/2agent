"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
}

export function Modal({ open, onClose, title, description, children }: ModalProps) {
  React.useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };
    if (open) {
      document.addEventListener("keydown", handleKey);
    }
    return () => document.removeEventListener("keydown", handleKey);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            role="dialog"
            aria-modal
            className="glass-panel w-full max-w-md rounded-3xl border border-border/70 p-8 shadow-glass"
            initial={{ opacity: 0, scale: 0.92 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.92 }}
            transition={{ duration: 0.16 }}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                {title && (
                  <h3 className="text-lg font-semibold text-text">{title}</h3>
                )}
                {description && (
                  <p className="mt-1 text-sm text-text-muted">{description}</p>
                )}
              </div>
              <button
                onClick={onClose}
                className="rounded-full border border-border/60 bg-white/5 px-2 py-1 text-xs uppercase tracking-wide text-text-muted hover:bg-white/10"
              >
                Close
              </button>
            </div>
            <div className="mt-6 text-sm text-text-muted">{children}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
