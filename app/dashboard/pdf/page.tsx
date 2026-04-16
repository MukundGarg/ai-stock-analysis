'use client';

import Link from 'next/link';
import { useCopilot } from '@/context/CopilotContext';
import { getApiUrl } from '@/lib/api';
import { normalizeAnalysis } from '@/utils/normalizeAnalysis';
import { useRef, useState } from 'react';

interface AnalysisResult {
  market_reaction: string;
  catalyst_type: string;
  institutional_interpretation: string;
  hidden_signals: string[];
  forward_watch: string[];
  analysis_mode?: 'ai' | 'fallback';
  fallback_reason?: string | null;
  setup_hint?: string | null;
  fallback_detail?: string | null;
}

interface ErrorState {
  message: string;
  details?: string;
}

export default function PDFToolPage() {
  const { setLastPdfAnalysis } = useCopilot();
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<ErrorState | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    setError(null);
    setAnalysis(null);
    setFileName(null);

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError({ message: 'Invalid file type', details: 'Please upload a PDF file only.' });
      return;
    }

    const maxSize = 25 * 1024 * 1024;
    if (file.size > maxSize) {
      setError({ message: 'File too large', details: 'Please upload a PDF smaller than 25MB.' });
      return;
    }

    setFileName(file.name);
    await analyzePDF(file);
  };

  const analyzePDF = async (file: File) => {
    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      const apiUrl = getApiUrl();

      const response = await fetch(`${apiUrl}/analyze-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error((errorData as { error?: string }).error || `Server error: ${response.status}`);
      }

      const result = (await response.json()) as AnalysisResult;
      const normalizedAnalysis = normalizeAnalysis(result);
      setAnalysis(normalizedAnalysis);
      setLastPdfAnalysis(result, '/dashboard/pdf');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      const apiUrl = getApiUrl();
      setError({
        message: 'Failed to analyze PDF',
        details:
          errorMessage === 'Failed to fetch'
            ? `Could not reach backend at ${apiUrl}. Is it running?`
            : errorMessage,
      });
      setFileName(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFileSelect(files[0]);
  };

  const handleButtonClick = () => fileInputRef.current?.click();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files;
    if (files?.length) handleFileSelect(files[0]);
  };

  return (
    <div className="w-full">
      <section className="border-b border-gray-200 py-12 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Link
            href="/dashboard"
            className="mb-4 inline-flex items-center font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
          >
            ← Back to Dashboard
          </Link>
          <h1 className="mb-4 text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            PDF report copilot
          </h1>
          <p className="max-w-3xl text-lg text-gray-600 dark:text-gray-400">
            Market intelligence engine: market reaction, catalyst classification, institutional interpretation, hidden signals, and forward watch.
          </p>
          <p className="mt-3 text-sm text-blue-800 dark:text-blue-200">
            Tip: open the Copilot button (bottom-right) to ask follow-ups about this file.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 dark:bg-black">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2">
              {!analysis && !isLoading && (
                <>
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`cursor-pointer rounded-xl border-2 border-dashed p-12 text-center transition-all ${
                      isDragging
                        ? 'border-blue-400 bg-blue-50 dark:border-blue-600 dark:bg-blue-900/20'
                        : 'border-gray-300 bg-gray-50 hover:border-blue-400 dark:border-gray-700 dark:bg-gray-900 dark:hover:border-blue-600'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf"
                      onChange={handleInputChange}
                      className="hidden"
                    />
                    <div className="mb-4 text-5xl">📄</div>
                    <h2 className="mb-2 text-2xl font-bold text-gray-900 dark:text-white">
                      Upload a PDF
                    </h2>
                    <p className="mb-4 text-gray-600 dark:text-gray-400">Drag and drop or click to browse</p>
                    <button
                      type="button"
                      onClick={handleButtonClick}
                      className="rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 font-medium text-white transition hover:from-blue-700 hover:to-purple-700"
                    >
                      Choose file
                    </button>
                    <p className="mt-4 text-sm text-gray-500">PDF up to 25MB · text-based PDFs work best</p>
                  </div>

                  {error && (
                    <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20">
                      <h3 className="mb-1 font-semibold text-red-900 dark:text-red-100">{error.message}</h3>
                      {error.details && (
                        <p className="text-sm text-red-800 dark:text-red-200">{error.details}</p>
                      )}
                    </div>
                  )}
                </>
              )}

              {isLoading && (
                <div className="flex flex-col items-center justify-center py-20">
                  <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
                  <p className="mt-4 text-lg font-medium text-gray-900 dark:text-white">Analyzing PDF…</p>
                </div>
              )}

              {!analysis && !isLoading && (
                <div className="text-center p-10">
                  <p>Loading analysis...</p>
                </div>
              )}

              {analysis && !isLoading && (
                <div className="space-y-8">
                  <div className="rounded-lg border border-green-200 bg-green-50 p-4 dark:border-green-800 dark:bg-green-900/20">
                    <p className="text-sm text-green-900 dark:text-green-100">
                      Analyzed: <span className="font-medium">{fileName}</span>
                    </p>
                  </div>

                  {analysis.analysis_mode === 'fallback' && (
                    <div
                      role="status"
                      className="rounded-xl border border-amber-300 bg-amber-50 p-5 dark:border-amber-800 dark:bg-amber-950/40"
                    >
                      <p className="font-semibold text-amber-950 dark:text-amber-100">
                        Limited mode (no full AI run)
                      </p>
                      {analysis.setup_hint && (
                        <p className="mt-2 text-sm leading-relaxed text-amber-950 dark:text-amber-100">
                          {analysis.setup_hint}
                        </p>
                      )}
                      {analysis.fallback_reason && (
                        <p className="mt-2 text-xs text-amber-900/80 dark:text-amber-200/90">
                          Reason code: {analysis.fallback_reason}
                        </p>
                      )}
                      {analysis.fallback_detail && (
                        <div className="mt-3 rounded-lg bg-amber-100/80 p-3 dark:bg-amber-950/50">
                          <p className="text-xs font-medium text-amber-950 dark:text-amber-100">
                            Technical detail (from LLM / server)
                          </p>
                          <pre className="mt-1 whitespace-pre-wrap break-words text-xs text-amber-950 dark:text-amber-100">
                            {analysis.fallback_detail}
                          </pre>
                        </div>
                      )}
                      <p className="mt-3 text-xs text-amber-900/80 dark:text-amber-200/90">
                        Quick check: open{' '}
                        <code className="rounded bg-amber-100 px-1 dark:bg-amber-900/60">
                          {getApiUrl()}/health
                        </code>{' '}
                        — if <code className="rounded bg-amber-100 px-1 dark:bg-amber-900/60">llm_configured</code>{' '}
                        is false, set AI_PROVIDER and GEMINI_API_KEY or GROQ_API_KEY on the API server and redeploy.
                      </p>
                    </div>
                  )}

                  <section className="rounded-xl border border-blue-200 bg-blue-50/50 p-6 dark:border-blue-900 dark:bg-blue-950/30">
                    <h3 className="mb-3 text-xl font-bold text-blue-900 dark:text-blue-100">Market Reaction</h3>
                    <p className="leading-relaxed text-blue-950 dark:text-blue-100">{analysis.market_reaction}</p>
                  </section>

                  <section className="rounded-xl border border-purple-200 bg-purple-50/50 p-6 dark:border-purple-900 dark:bg-purple-950/30">
                    <h3 className="mb-3 text-xl font-bold text-purple-900 dark:text-purple-100">Catalyst Type</h3>
                    <div className="inline-flex items-center rounded-full px-4 py-2 text-sm font-semibold bg-purple-600 text-white">
                      {analysis.catalyst_type}
                    </div>
                  </section>

                  <section className="rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
                    <h3 className="mb-3 text-xl font-bold text-gray-900 dark:text-white">Institutional Interpretation</h3>
                    <p className="leading-relaxed text-gray-700 dark:text-gray-300">{analysis.institutional_interpretation}</p>
                  </section>

                  <section className="rounded-xl border border-red-200 bg-red-50/50 p-6 dark:border-red-900 dark:bg-red-950/30">
                    <h3 className="mb-4 text-xl font-bold text-red-900 dark:text-red-100">Hidden Signals</h3>
                    <ul className="space-y-2 text-red-950 dark:text-red-100">
                      {analysis.hidden_signals?.map((x, i) => (
                        <li key={i}>• {x}</li>
                      )) || <li className="text-gray-500 dark:text-gray-400">No hidden signals detected</li>}
                    </ul>
                  </section>

                  <section className="rounded-xl border border-amber-200 bg-amber-50/50 p-6 dark:border-amber-900 dark:bg-amber-950/30">
                    <h3 className="mb-4 text-xl font-bold text-amber-900 dark:text-amber-100">Forward Watch</h3>
                    <ul className="space-y-2 text-amber-950 dark:text-amber-100">
                      {analysis.forward_watch?.map((x, i) => (
                        <li key={i}>• {x}</li>
                      )) || <li className="text-gray-500 dark:text-gray-400">No watchlist items</li>}
                    </ul>
                  </section>

                  <button
                    type="button"
                    onClick={() => {
                      setAnalysis(null);
                      setFileName(null);
                      setError(null);
                      fileInputRef.current?.click();
                    }}
                    className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 py-3 font-medium text-white hover:from-blue-700 hover:to-purple-700"
                  >
                    Analyze another PDF
                  </button>
                </div>
              )}
            </div>

            <div className="lg:col-span-1">
              <div className="sticky top-24 space-y-6">
                <div className="rounded-xl border border-blue-200 bg-blue-50 p-6 dark:border-blue-800 dark:bg-blue-900/20">
                  <h4 className="mb-2 font-semibold text-blue-900 dark:text-blue-100">Indian context</h4>
                  <p className="text-sm text-blue-900/90 dark:text-blue-200">
                    Figures may be in INR or USD depending on the filing. Cross-check with NSE/BSE filings when
                    investing.
                  </p>
                </div>
                <div className="rounded-xl border border-gray-200 bg-gray-50 p-6 dark:border-gray-800 dark:bg-gray-900">
                  <h4 className="mb-2 font-semibold text-gray-900 dark:text-white">Documents</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Annual / quarterly reports</li>
                    <li>• Investor presentations</li>
                    <li>• Earnings transcripts</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
