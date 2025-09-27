import Link from "next/link";
import { Logo } from "@/components/logo";
import { Button } from "@/components/ui/button";

type NavRoute = "/" | "/demo" | "/pricing" | "/docs" | "/about";

const navLinks: { href: NavRoute; label: string }[] = [
  { href: "/", label: "Home" },
  { href: "/demo", label: "Live Demo" },
  { href: "/pricing", label: "Pricing" },
  { href: "/docs", label: "Docs" },
  { href: "/about", label: "About" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/70 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <Logo className="h-8 w-8" />
          <div>
            <span className="text-lg font-semibold text-text">2Agent</span>
            <p className="text-xs text-text-muted">Two AIs. One repo.</p>
          </div>
        </Link>
        <nav className="hidden items-center gap-8 text-sm text-text-muted md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="transition-colors hover:text-text"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Link
            href="/auth"
            className="hidden text-sm font-medium text-text-muted transition-colors hover:text-text md:inline"
          >
            Sign in
          </Link>
          <Button asChild>
            <Link href="/demo">Start a build</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
