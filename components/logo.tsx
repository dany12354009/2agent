export function Logo({ className = "h-9 w-9" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="4" y="4" width="56" height="56" rx="16" fill="url(#grad)" />
      <path
        d="M24 20c4-4 12-4 16 0 4 4 4 12 0 16l-8 8"
        stroke="#0B0F12"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M40 44c-4 4-12 4-16 0-4-4-4-12 0-16l8-8"
        stroke="#0B0F12"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <defs>
        <linearGradient id="grad" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
          <stop stopColor="#15C2B8" />
          <stop offset="1" stopColor="#0F141A" />
        </linearGradient>
      </defs>
    </svg>
  );
}
