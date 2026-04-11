'use client';

import Link from 'next/link';

export default function ChartToolPage() {
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
            📊 Chart Pattern Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Master technical analysis with AI-powered chart pattern recognition
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Chart Input */}
            <div className="lg:col-span-2">
              <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Enter Stock Symbol or Upload Chart
                </h2>

                <div className="space-y-6">
                  {/* Search Input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                      Stock Symbol
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., AAPL, TSLA, MSFT"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  {/* Chart Preview */}
                  <div className="bg-white dark:bg-black rounded-lg border border-gray-300 dark:border-gray-700 p-8 h-80 flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-5xl mb-4">📈</div>
                      <p className="text-gray-500 dark:text-gray-400">
                        Chart will appear here after entering a symbol
                      </p>
                    </div>
                  </div>

                  {/* Analyze Button */}
                  <button className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
                    Analyze Chart
                  </button>
                </div>
              </div>

              {/* Pattern Explanations */}
              <div className="mt-12">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Common Patterns
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { name: 'Head & Shoulders', signal: 'Bearish', confidence: '85%' },
                    { name: 'Double Top', signal: 'Bearish', confidence: '78%' },
                    { name: 'Triangle', signal: 'Neutral', confidence: '72%' },
                    { name: 'Cup & Handle', signal: 'Bullish', confidence: '88%' },
                  ].map((pattern, idx) => (
                    <div
                      key={idx}
                      className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:border-blue-400 dark:hover:border-blue-600 transition-all cursor-pointer"
                    >
                      <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                        {pattern.name}
                      </h4>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">
                          Signal: <span className="font-medium text-gray-900 dark:text-white">{pattern.signal}</span>
                        </span>
                        <span className="text-gray-600 dark:text-gray-400">
                          Confidence: <span className="font-medium text-gray-900 dark:text-white">{pattern.confidence}</span>
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-20 space-y-6">
                {/* Info Box */}
                <div className="p-6 rounded-xl bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800">
                  <h4 className="font-semibold text-purple-900 dark:text-purple-100 mb-3">
                    📚 Learn Patterns
                  </h4>
                  <ul className="space-y-2 text-sm text-purple-800 dark:text-purple-200">
                    <li>• Understand trend reversals</li>
                    <li>• Identify support & resistance</li>
                    <li>• Recognize continuation patterns</li>
                    <li>• Learn volume analysis</li>
                  </ul>
                </div>

                {/* Timeframes */}
                <div className="p-6 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Timeframes
                  </h4>
                  <div className="space-y-2">
                    <button className="w-full px-3 py-2 text-left text-sm rounded bg-blue-600 text-white font-medium">
                      1D
                    </button>
                    <button className="w-full px-3 py-2 text-left text-sm rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors">
                      1W
                    </button>
                    <button className="w-full px-3 py-2 text-left text-sm rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors">
                      1M
                    </button>
                    <button className="w-full px-3 py-2 text-left text-sm rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors">
                      3M
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Analyze any stock with AI-powered pattern recognition
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
              Start Analyzing
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
