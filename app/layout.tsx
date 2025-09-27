import "./globals.css";
import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { cn } from "@/lib/utils";
import { Toaster } from "@/components/toaster";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetBrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
});

export const metadata: Metadata = {
  title: "2Agent — Two AIs. One repo.",
  description: "2Agent plans, debates, codes, and reviews until it ships.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body
        className={cn(
          "bg-background text-text font-sans antialiased",
          inter.variable,
          jetBrainsMono.variable
        )}
      >
        <Toaster>{children}</Toaster>
      </body>
    </html>
  );
}
