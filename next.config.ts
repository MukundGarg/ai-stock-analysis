import type { NextConfig } from "next";

/**
 * Relaxed script-src allows 'unsafe-eval' so Next.js / dev tooling and some bundled code
 * are not blocked when the browser enforces CSP (also aligns with common Vercel setups).
 * connect-src must include your API origin via same-origin + https (set NEXT_PUBLIC_API_URL to https API).
 */
const nextConfig: NextConfig = {
  async headers() {
    const csp = [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob: https:",
      "font-src 'self' data:",
      "connect-src 'self' http://127.0.0.1:8000 http://localhost:8000 https: wss:",
      "frame-ancestors 'self'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join("; ");

    return [
      {
        source: "/:path*",
        headers: [{ key: "Content-Security-Policy", value: csp }],
      },
    ];
  },
};

export default nextConfig;
