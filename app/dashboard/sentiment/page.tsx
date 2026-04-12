'use client';

import Link from 'next/link';
import { useState } from 'react';

interface NewsArticle {
  title: string;
  description: string | null;
  source: string;
  url: string;
  published_at: string | null;
}

interface SentimentResult {
  sentiment: string;
  sentiment_score: number;
  summary: string;
  key_reasons: string[];
  news_sources: NewsArticle[];
  query: string;
}

interface ErrorState {
  message: string;
  details?: string;
}

export default function SentimentToolPage() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [error, setError] = useState<ErrorState | null>(null);

  const handleAnalyze = async () => {
    if (!query.trim()) {
      setError({
        message: 'Invalid input',
        details: 'Please enter a query before analyzing.',
      });
      return;
    }

    if (query.length > 200) {
      setError({
        message: 'Query too long',
        details: 'Please keep your query under 200 characters.',
      });
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      console.log(`[Sentiment] API URL: ${apiUrl}`);
      console.log(`[Sentiment] Analyzing query: ${query}`);

      const response = await fetch(`${apiUrl}/analyze-sentiment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      console.log(`[Sentiment] Response status: ${response.status}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data: SentimentResult = await response.json();
      setResult(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      console.error(`[Sentiment] Error:`, err);

      setError({
        message: 'Failed to analyze sentiment',
        details:
          errorMessage === 'Failed to fetch'
            ? `Could not reach backend at ${apiUrl}. Check if backend is running and CORS is configured.`
            : errorMessage,
      });
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'Bullish':
        return 'bg-green-100 dark:bg-green-900/30 text-green-900 dark:text-green-100 border-green-300 dark:border-green-700';
      case 'Bearish':
        return 'bg-red-100 dark:bg-red-900/30 text-red-900 dark:text-red-100 border-red-300 dark:border-red-700';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-700';
    }
  };

  const getSentimentTextColor = (sentiment: string) => {
    switch (sentiment) {
      case 'Bullish':
        return 'text-green-600 dark:text-green-400';
      case 'Bearish':
        return 'text-red-600 dark:text-red-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const sentimentPercentage = result
    ? Math.round(((result.sentiment_score + 1) / 2) * 100)
    : 0;

  return (
    <div className="w-full">
      {/* Header */}
      <section className="py-12 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            href="/dashboard"
            className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium mb-4"
          >
            <svg
              className="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to Dashboard
          </Link>
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            📊 Market Sentiment AI
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Ask why the market or stocks are moving. Get AI-powered insights based on
            current news and sentiment analysis.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content Area */}
            <div className="lg:col-span-2">
              {!result && !isLoading && (
                <>
                  {/* Search Input */}
                  <div className="mb-12">
                    <div className="relative">
                      <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                        placeholder="Ask why the market or a stock is moving... e.g., 'Why is Apple stock rising?'"
                        className="w-full px-6 py-4 text-lg rounded-lg border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:border-blue-500 dark:focus:border-blue-400"
                      />
                      <button
                        onClick={handleAnalyze}
                        disabled={isLoading}
                        className="absolute right-2 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Analyze
                      </button>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-3">
                      Press Enter or click Analyze to get sentiment insights
                    </p>
                  </div>

                  {/* Error Message */}
                  {error && (
                    <div className="mt-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                      <h3 className="font-semibold text-red-900 dark:text-red-100 mb-1">
                        {error.message}
                      </h3>
                      {error.details && (
                        <p className="text-sm text-red-800 dark:text-red-200">
                          {error.details}
                        </p>
                      )}
                    </div>
                  )}

                  {/* Features */}
                  <div className="mt-16">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                      What You Can Do
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                        <div className="text-3xl mb-3">📈</div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                          Get Sentiment Insights
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Understand market sentiment with AI-powered analysis
                        </p>
                      </div>

                      <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                        <div className="text-3xl mb-3">📰</div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                          View Key News
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          See the articles driving current market sentiment
                        </p>
                      </div>

                      <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                        <div className="text-3xl mb-3">💡</div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                          Learn the Why
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Get easy-to-understand explanations of market movements
                        </p>
                      </div>

                      <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                        <div className="text-3xl mb-3">🎯</div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                          Track Patterns
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Understand recurring themes in financial news
                        </p>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Loading State */}
              {isLoading && (
                <div className="flex flex-col items-center justify-center py-20">
                  <div className="animate-spin">
                    <svg
                      className="w-12 h-12 text-blue-600 dark:text-blue-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                  </div>
                  <p className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
                    Analyzing market sentiment...
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    Fetching news and analyzing trends
                  </p>
                </div>
              )}

              {/* Results */}
              {result && !isLoading && (
                <div className="space-y-8">
                  {/* Query Confirmation */}
                  <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                    <p className="text-sm text-blue-900 dark:text-blue-100">
                      ✓ Query analyzed: <span className="font-medium">"{result.query}"</span>
                    </p>
                  </div>

                  {/* Sentiment Badge */}
                  <div className="p-8 rounded-lg border-2 border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-4">
                      Market Sentiment
                    </h3>

                    <div className="mb-6">
                      <div
                        className={`inline-block px-6 py-3 rounded-lg border-2 text-2xl font-bold ${getSentimentColor(
                          result.sentiment
                        )}`}
                      >
                        {result.sentiment}
                      </div>
                    </div>

                    {/* Sentiment Score Gauge */}
                    <div className="mb-6">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                          Bearish ← → Bullish
                        </span>
                        <span
                          className={`text-2xl font-bold ${getSentimentTextColor(
                            result.sentiment
                          )}`}
                        >
                          {sentimentPercentage}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-4 rounded-full transition-all"
                          style={{
                            width: `${Math.max(0, Math.min(100, sentimentPercentage))}%`,
                          }}
                        />
                      </div>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        Score: {result.sentiment_score.toFixed(2)}
                      </p>
                    </div>
                  </div>

                  {/* AI Summary */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                      💬 AI Analysis
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
                      {result.summary}
                    </p>
                  </div>

                  {/* Key Reasons */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      🔍 Key Themes
                    </h3>
                    <ul className="space-y-3">
                      {result.key_reasons.map((reason, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-3 text-gray-700 dark:text-gray-300"
                        >
                          <span className="text-blue-600 dark:text-blue-400 font-bold mt-1">
                            •
                          </span>
                          <span>{reason}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* News Sources */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      📰 Related News Articles
                    </h3>
                    <div className="space-y-4">
                      {result.news_sources.map((article, idx) => (
                        <a
                          key={idx}
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 hover:border-blue-400 dark:hover:border-blue-500 transition-all"
                        >
                          <h4 className="font-semibold text-blue-600 dark:text-blue-400 hover:underline mb-2">
                            {article.title}
                          </h4>
                          {article.description && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                              {article.description}
                            </p>
                          )}
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-gray-500 dark:text-gray-500">
                              {article.source}
                            </span>
                            {article.published_at && (
                              <span className="text-gray-500 dark:text-gray-500">
                                {new Date(article.published_at).toLocaleDateString()}
                              </span>
                            )}
                          </div>
                        </a>
                      ))}
                    </div>
                  </div>

                  {/* New Analysis Button */}
                  <button
                    onClick={() => {
                      setResult(null);
                      setQuery('');
                      setError(null);
                    }}
                    className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                  >
                    Analyze Another Query
                  </button>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-20 space-y-6">
                {/* Example Queries */}
                <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
                    💡 Try These Queries
                  </h4>
                  <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Why is Apple stock rising?</li>
                    <li>• Why is the market falling today?</li>
                    <li>• What about tech sector sentiment?</li>
                    <li>• Why is Tesla stock down?</li>
                    <li>• Is the market bullish right now?</li>
                  </ul>
                </div>

                {/* Sentiment Meanings */}
                <div className="p-6 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <h4 className="font-semibold text-green-900 dark:text-green-100 mb-3">
                    📚 Sentiment Guide
                  </h4>
                  <ul className="space-y-3 text-sm text-green-800 dark:text-green-200">
                    <li>
                      <strong>Bullish 📈</strong>
                      <br />
                      Positive sentiment with optimistic news
                    </li>
                    <li>
                      <strong>Bearish 📉</strong>
                      <br />
                      Negative sentiment with pessimistic news
                    </li>
                    <li>
                      <strong>Neutral ➡️</strong>
                      <br />
                      Mixed signals without clear direction
                    </li>
                  </ul>
                </div>

                {/* Disclaimer */}
                <div className="p-6 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800">
                  <h4 className="font-semibold text-amber-900 dark:text-amber-100 mb-3">
                    ⚠️ Disclaimer
                  </h4>
                  <p className="text-xs text-amber-800 dark:text-amber-200">
                    This sentiment analysis is for educational purposes only. It reflects
                    AI-analyzed news sentiment, not financial advice. Always do your own
                    research before making investment decisions.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
