'use client';

import Link from 'next/link';
import { getApiUrl } from '@/lib/api';
import { useEffect, useState } from 'react';

type Structured = {
  title: string;
  exchanges: Record<string, string>;
  typical_trading_hours_ist: Record<string, string>;
  fno_vs_equity: Record<string, string>;
  sebi_role: string;
  india_vs_us: string[];
  example_tickers_education_only: string[];
};

export default function IndiaLearnPage() {
  const [data, setData] = useState<Structured | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const api = getApiUrl();
    fetch(`${api}/learn/indian-markets`)
      .then((r) => {
        if (!r.ok) throw new Error('Could not load reference');
        return r.json();
      })
      .then(setData)
      .catch(() => setErr('Connect the backend to load live reference JSON, or read the static guide below.'));
  }, []);

  return (
    <div className="w-full">
      <section className="border-b border-gray-200 bg-gradient-to-br from-slate-50 to-white py-14 dark:from-black dark:to-gray-950 dark:border-gray-800">
        <div className="mx-auto max-w-3xl px-4">
          <Link href="/" className="mb-4 inline-block text-blue-600 dark:text-blue-400">
            ← Home
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">India markets 101</h1>
          <p className="mt-3 text-lg text-gray-600 dark:text-gray-400">
            Built for beginners trading or learning on <strong className="font-semibold">NSE</strong> and{' '}
            <strong className="font-semibold">BSE</strong>. Use this page with the Copilot for deeper Q&amp;A.
          </p>
          {err && <p className="mt-4 text-sm text-amber-800 dark:text-amber-200">{err}</p>}
        </div>
      </section>

      <article className="mx-auto max-w-3xl space-y-6 px-4 py-12 text-gray-800 dark:text-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">NSE vs BSE</h2>
        <p className="leading-relaxed">
          Both are regulated stock exchanges in India. Most large stocks are listed on both. The{' '}
          <strong className="font-semibold">NIFTY 50</strong> tracks 50 major NSE names; the{' '}
          <strong className="font-semibold">SENSEX</strong> tracks 30 major BSE names. Liquidity can differ slightly
          by stock and session.
        </p>

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Typical trading hours (IST)</h2>
        <ul className="list-inside list-disc space-y-2 leading-relaxed">
          <li>
            <strong className="font-semibold">Pre-open</strong> (~09:00–09:15 IST): order collection and indicative
            equilibrium price.
          </li>
          <li>
            <strong className="font-semibold">Regular session</strong>: 09:15–15:30 IST on working days (not exchange
            holidays).
          </li>
        </ul>
        {data?.typical_trading_hours_ist && (
          <pre className="overflow-x-auto rounded-lg bg-gray-100 p-4 text-xs dark:bg-gray-900">
            {JSON.stringify(data.typical_trading_hours_ist, null, 2)}
          </pre>
        )}

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Equity (cash) vs F&amp;O</h2>
        <p className="leading-relaxed">
          <strong className="font-semibold">Cash / equity</strong>: you buy shares outright (or with broker margin
          products for intraday). Holding period drives taxation treatment (LTCG/STCG rules apply — consult a tax
          professional).
        </p>
        <p className="leading-relaxed">
          <strong className="font-semibold">F&amp;O</strong>: futures and options on indices or stocks. Contracts
          expire; leverage magnifies gains and losses. SEBI sets eligibility norms. Most beginners should understand
          cash markets first.
        </p>

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">SEBI (simple)</h2>
        <p className="leading-relaxed">
          The Securities and Exchange Board of India oversees fair markets, disclosures from listed companies, and
          intermediaries. It does not “guarantee” stock performance — it sets rules to reduce fraud and improve
          transparency.
        </p>

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">How India often differs from the US</h2>
        <ul className="list-inside list-disc space-y-2 leading-relaxed">
          <li>Macro: RBI rates, INR, crude, monsoon (some sectors), FII/DII flows.</li>
          <li>Session structure: most retail activity is in the single day session vs US extended hours.</li>
          <li>Global spillover: US Fed, US indices, and geopolitics still move sentiment.</li>
        </ul>

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Beginner examples (education only)</h2>
        <p className="leading-relaxed">
          Large liquid names often used in textbooks: Reliance, TCS, HDFC Bank. They illustrate size and liquidity —
          not a recommendation to buy or sell.
        </p>

        {data && (
          <section className="mt-10 rounded-xl border border-gray-200 bg-gray-50 p-6 dark:border-gray-800 dark:bg-gray-900">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">API reference snapshot</h3>
            <pre className="mt-3 max-h-96 overflow-auto text-xs text-gray-700 dark:text-gray-300">
              {JSON.stringify(data, null, 2)}
            </pre>
          </section>
        )}
      </article>
    </div>
  );
}
