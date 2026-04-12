'use client';

import Link from 'next/link';
import { useCopilot } from '@/context/CopilotContext';
import { getApiUrl } from '@/lib/api';
import { useRef, useState } from 'react';

interface ChartAnalysisResult {
  pattern: string;
  signal: string;
  confidence: string;
  confidence_score: number;
  description: string;
  reasoning: string;
  support_resistance: string;
  trendlines: string;
  breakout_notes: string;
  candlestick_notes: string;
  beginner_explanation: string;
  analysis_method: string;
  cv_fallback_summary?: string | null;
  vision_secondary_note?: string | null;
}

interface ErrorState {
  message: string;
  details?: string;
}

export default function ChartToolPage() {
  const { setLastChartAnalysis } = useCopilot();
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<ChartAnalysisResult | null>(null);
  const [error, setError] = useState<ErrorState | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    setError(null);
    setAnalysis(null);
    setFileName(null);
    setPreviewUrl(null);

    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      setError({ message: 'Invalid file type', details: 'Please upload PNG or JPG.' });
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError({ message: 'File too large', details: 'Max 5MB.' });
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) setPreviewUrl(e.target.result as string);
    };
    reader.readAsDataURL(file);

    setFileName(file.name);
    await analyzeChart(file);
  };

  const analyzeChart = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}/analyze-chart`, { method: 'POST', body: formData });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error((errorData as { error?: string }).error || `Server error: ${response.status}`);
      }

      const result = (await response.json()) as ChartAnalysisResult;
      setAnalysis(result);
      setLastChartAnalysis(result, '/dashboard/chart');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      const apiUrl = getApiUrl();
      setError({
        message: 'Failed to analyze chart',
        details:
          errorMessage === 'Failed to fetch'
            ? `Could not reach backend at ${apiUrl}. Is it running?`
            : errorMessage,
      });
      setFileName(null);
      setPreviewUrl(null);
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
    if (e.dataTransfer.files.length) handleFileSelect(e.dataTransfer.files[0]);
  };

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'Bullish':
        return 'bg-green-100 text-green-900 border-green-300 dark:bg-green-900/30 dark:text-green-100 dark:border-green-700';
      case 'Bearish':
        return 'bg-red-100 text-red-900 border-red-300 dark:bg-red-900/30 dark:text-red-100 dark:border-red-700';
      default:
        return 'bg-gray-100 text-gray-900 border-gray-300 dark:bg-gray-800 dark:text-gray-100 dark:border-gray-700';
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'High':
        return 'text-green-600 dark:text-green-400';
      case 'Medium':
        return 'text-yellow-600 dark:text-yellow-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const methodLabel = (m: string) =>
    m === 'vision_primary'
      ? 'AI vision (primary)'
      : m === 'cv_primary'
        ? 'Geometry fallback (vision low confidence)'
        : 'Computer vision';

  return (
    <div className="w-full">
      <section className="border-b border-gray-200 py-12 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Link
            href="/dashboard"
            className="mb-4 inline-flex items-center font-medium text-blue-600 dark:text-blue-400"
          >
            ← Back to Dashboard
          </Link>
          <h1 className="mb-4 text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            Chart pattern copilot
          </h1>
          <p className="max-w-3xl text-lg text-gray-600 dark:text-gray-400">
            Upload a screenshot from TradingView, Chartink, or your broker. We use AI vision plus geometry
            fallback for patterns, support/resistance, trendlines, and breakouts — with confidence and
            reasoning.
          </p>
          <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
            Ask the floating Copilot: “What does this pattern mean for a beginner?”
          </p>
        </div>
      </section>

      <section className="bg-white py-16 dark:bg-black">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2">
              {!analysis && !isLoading && !previewUrl && (
                <>
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`rounded-xl border-2 border-dashed p-12 text-center ${
                      isDragging
                        ? 'border-blue-400 bg-blue-50 dark:border-blue-600 dark:bg-blue-900/20'
                        : 'border-gray-300 bg-gray-50 dark:border-gray-700 dark:bg-gray-900'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".png,.jpg,.jpeg"
                      onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                      className="hidden"
                    />
                    <div className="mb-4 text-5xl">📈</div>
                    <h2 className="mb-2 text-2xl font-bold text-gray-900 dark:text-white">Upload chart image</h2>
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 font-medium text-white"
                    >
                      Choose image
                    </button>
                    {error && (
                      <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-left dark:border-red-800 dark:bg-red-900/20">
                        <p className="font-semibold text-red-900 dark:text-red-100">{error.message}</p>
                        {error.details && (
                          <p className="text-sm text-red-800 dark:text-red-200">{error.details}</p>
                        )}
                      </div>
                    )}
                  </div>
                </>
              )}

              {(previewUrl || isLoading) && !analysis && (
                <div className="space-y-6">
                  {previewUrl && (
                    <div className="rounded-lg border border-gray-200 p-4 dark:border-gray-800">
                      <p className="mb-2 font-medium text-gray-900 dark:text-white">Preview</p>
                      <div className="relative h-64 w-full overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-800">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={previewUrl} alt="Chart" className="h-full w-full object-contain" />
                      </div>
                    </div>
                  )}
                  {isLoading && (
                    <div className="flex flex-col items-center py-12">
                      <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
                      <p className="mt-4 text-gray-700 dark:text-gray-300">Running vision + CV analysis…</p>
                    </div>
                  )}
                </div>
              )}

              {analysis && !isLoading && (
                <div className="space-y-6">
                  <div className="rounded-lg border border-green-200 bg-green-50 p-4 dark:border-green-800 dark:bg-green-900/20">
                    <p className="text-sm text-green-900 dark:text-green-100">
                      Chart: <span className="font-medium">{fileName}</span>
                    </p>
                  </div>

                  <div className="rounded-xl border-2 border-gray-200 p-8 dark:border-gray-800">
                    <p className="text-sm text-gray-500 dark:text-gray-400">{methodLabel(analysis.analysis_method)}</p>
                    <h3 className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{analysis.pattern}</h3>

                    <div className="mt-4 flex flex-wrap gap-4">
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Signal</p>
                        <div
                          className={`mt-1 inline-block rounded-lg border px-4 py-2 text-lg font-semibold ${getSignalColor(
                            analysis.signal
                          )}`}
                        >
                          {analysis.signal}
                        </div>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Confidence</p>
                        <p className={`text-2xl font-bold ${getConfidenceColor(analysis.confidence)}`}>
                          {analysis.confidence}{' '}
                          <span className="text-lg text-gray-500 dark:text-gray-400">
                            ({analysis.confidence_score}/100)
                          </span>
                        </p>
                      </div>
                    </div>

                    <div className="mt-6 space-y-4 text-gray-700 dark:text-gray-300">
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Beginner view</p>
                        <p className="mt-1 leading-relaxed whitespace-pre-wrap">{analysis.description}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Reasoning</p>
                        <p className="mt-1 leading-relaxed">{analysis.reasoning}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Support / resistance</p>
                        <p className="mt-1">{analysis.support_resistance}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Trendlines</p>
                        <p className="mt-1">{analysis.trendlines}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Breakouts</p>
                        <p className="mt-1">{analysis.breakout_notes}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Candlestick context</p>
                        <p className="mt-1">{analysis.candlestick_notes}</p>
                      </div>
                      {analysis.cv_fallback_summary && (
                        <p className="text-sm text-gray-500 dark:text-gray-400">{analysis.cv_fallback_summary}</p>
                      )}
                      {analysis.vision_secondary_note && (
                        <p className="text-sm text-amber-800 dark:text-amber-200">
                          Vision note: {analysis.vision_secondary_note}
                        </p>
                      )}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => {
                      setAnalysis(null);
                      setFileName(null);
                      setPreviewUrl(null);
                      setError(null);
                      fileInputRef.current?.click();
                    }}
                    className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 py-3 font-medium text-white"
                  >
                    Analyze another chart
                  </button>
                </div>
              )}
            </div>

            <div className="space-y-6 lg:col-span-1">
              <div className="sticky top-24 rounded-xl border border-amber-200 bg-amber-50 p-6 dark:border-amber-900 dark:bg-amber-950/30">
                <h4 className="font-semibold text-amber-900 dark:text-amber-100">Disclaimer</h4>
                <p className="mt-2 text-xs text-amber-900 dark:text-amber-200">
                  Patterns on screenshots are educational. NSE/BSE prices need real-time data from your broker.
                  Not financial advice.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
