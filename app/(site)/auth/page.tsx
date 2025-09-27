"use client";

import * as React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";

export default function AuthPage() {
  const [open, setOpen] = React.useState(true);
  const [email, setEmail] = React.useState("");
  const [submitted, setSubmitted] = React.useState(false);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="flex min-h-[60vh] items-center justify-center px-6 py-20">
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Sign in"
        description="We\'ll email you a one-time magic link to continue."
      >
        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <label className="space-y-2 text-sm text-text">
            Email
            <Input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@company.com"
              required
            />
          </label>
          <Button type="submit" className="w-full" disabled={submitted}>
            {submitted ? "Link sent" : "Send magic link"}
          </Button>
        </form>
      </Modal>
    </div>
  );
}
