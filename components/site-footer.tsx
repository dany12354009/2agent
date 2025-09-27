import Link from "next/link";

type InternalFooterLink = { label: string; href: "/docs" | "/pricing"; external?: false };
type ExternalFooterLink = { label: string; href: string; external: true };

type FooterLink = InternalFooterLink | ExternalFooterLink;

const footerLinks: FooterLink[] = [
  { label: "Docs", href: "/docs" },
  { label: "Pricing", href: "/pricing" },
  { label: "GitHub", href: "https://github.com/2agent", external: true },
  { label: "Terms", href: "#", external: true },
  { label: "Privacy", href: "#", external: true },
];

export function SiteFooter() {
  return (
    <footer className="border-t border-border/60 bg-background/70">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-10 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-text">© {new Date().getFullYear()} 2Agent</p>
          <p className="text-xs text-text-muted">Two AIs. One repo.</p>
        </div>
        <nav className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-text-muted">
          {footerLinks.map((link) =>
            link.external ? (
              <a
                key={link.href}
                href={link.href}
                className="hover:text-text"
                target={link.href.startsWith("http") ? "_blank" : undefined}
                rel={link.href.startsWith("http") ? "noreferrer" : undefined}
              >
                {link.label}
              </a>
            ) : (
              <Link key={link.href} href={link.href} className="hover:text-text">
                {link.label}
              </Link>
            )
          )}
        </nav>
      </div>
    </footer>
  );
}
