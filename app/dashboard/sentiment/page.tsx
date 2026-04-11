'use client';

import Link from 'next/link';

export default function SentimentToolPage() {
  return (
    <div className="w-full">
      {/* Header */}
      <section className="py-12 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            href="/dashboard"
            className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium mb-4"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Dashboard
          </Link>
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            📈 Market Sentiment AI
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Track real-time market sentiment and understand investor psychology
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Sentiment Overview */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            {/* Overall Sentiment */}
            <div className="lg:col-span-2 p-8 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Overall Market Sentiment
              </h2>

              <div className="space-y-6">
                {/* Sentiment Gauge */}
                <div className="bg-white dark:bg-black rounded-lg p-6 border border-gray-300 dark:border-gray-700">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Fear ← → Greed
                    </span>
                    <span className="text-2xl font-bold text-green-600 dark:text-green-400">
                      67%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-3 rounded-full"
                      style={{ width: '67%' }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    Moderately Bullish - Investors are optimistic
                  </p>
                </div>

                {/* Sentiment Indicators */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 rounded-lg bg-white dark:bg-black border border-gray-300 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      Fear & Greed Index
                    </p>
                    <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                      Greed
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-white dark:bg-black border border-gray-300 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      Market Trend
                    </p>
                    <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                      ↗ Bullish
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-white dark:bg-black border border-gray-300 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      Volatility
                    </p>
                    <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                      Medium
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="p-6 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                <h4 className="font-semibold text-green-900 dark:text-green-100 mb-3">
                  📊 Current Status
                </h4>
                <ul className="space-y-2 text-sm text-green-800 dark:text-green-200">
                  <li>• Bullish market momentum</li>
                  <li>• Positive earnings season</li>
                  <li>• Strong investor interest</li>
                  <li>• Low unemployment rates</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Sector Sentiment */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Sentiment by Sector
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { sector: 'Technology', sentiment: '72%', trend: '↗ Bullish' },
                { sector: 'Healthcare', sentiment: '65%', trend: '→ Neutral' },
                { sector: 'Finance', sentiment: '58%', trend: '↗ Bullish' },
                { sector: 'Energy', sentiment: '45%', trend: '↘ Bearish' },
                { sector: 'Retail', sentiment: '62%', trend: '↗ Bullish' },
                { sector: 'Manufacturing', sentiment: '55%', trend: '→ Neutral' },
              ].map((sector, idx) => (
                <div
                  key={idx}
                  className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:border-blue-400 dark:hover:border-blue-600 transition-all"
                >
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {sector.sector}
                    </h3>
                    <span className="text-sm font-bold text-gray-900 dark:text-white">
                      {sector.sentiment}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                    <div
                      className="bg-blue-600 dark:bg-blue-500 h-2 rounded-full"
                      style={{ width: sector.sentiment }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {sector.trend}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Sentiment Drivers */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Key Sentiment Drivers
            </h2>
            <div className="space-y-4">
              {[
                { driver: 'Fed Interest Rate Decisions', impact: 'High', direction: 'up' },
                { driver: 'Earnings Reports', impact: 'High', direction: 'up' },
                { driver: 'Inflation Data', impact: 'Medium', direction: 'down' },
                { driver: 'Economic Growth', impact: 'High', direction: 'up' },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 flex justify-between items-center"
                >
                  <span className="text-gray-900 dark:text-white font-medium">
                    {item.driver}
                  </span>
                  <div className="flex gap-3">
                    <span className="text-sm px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100 rounded-full">
                      {item.impact}
                    </span>
                    <span className={`text-lg font-bold ${
                      item.direction === 'up'
                        ? 'text-green-600 dark:text-green-400'
                        : 'text-red-600 dark:text-red-400'
                    }`}>
                      {item.direction === 'up' ? '↗' : '↘'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Stay informed with real-time market sentiment tracking
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
              Analyze Current Sentiment
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
