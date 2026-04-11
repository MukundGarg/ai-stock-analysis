'use client';

import Link from 'next/link';

export default function MovementToolPage() {
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
            🔍 Why is This Stock Moving?
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Get instant explanations for stock price movements with AI-powered analysis
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Search */}
          <div className="mb-12">
            <div className="flex gap-4">
              <input
                type="text"
                placeholder="Enter stock symbol (e.g., AAPL, TSLA)"
                className="flex-1 px-6 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
                Analyze
              </button>
            </div>
          </div>

          {/* Analysis Results */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Analysis */}
            <div className="lg:col-span-2">
              {/* Stock Info */}
              <div className="p-8 rounded-xl bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 border border-gray-200 dark:border-gray-800 mb-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                      AAPL (Apple Inc.)
                    </h2>
                    <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">
                      Current Price: $185.42 • Change: +2.45% ↗
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Today's Movement
                    </div>
                    <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                      +$4.40
                    </div>
                  </div>
                </div>

                {/* Chart Placeholder */}
                <div className="bg-white dark:bg-black rounded-lg h-48 flex items-center justify-center">
                  <p className="text-gray-500 dark:text-gray-400">
                    Price chart visualization
                  </p>
                </div>
              </div>

              {/* Key Catalysts */}
              <div className="mb-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Key Catalysts Driving Movement
                </h3>

                <div className="space-y-4">
                  {[
                    {
                      icon: '📰',
                      title: 'Q4 Earnings Beat',
                      impact: 'Major Positive',
                      details: 'Apple reported better-than-expected earnings with strong iPhone sales',
                      time: '2 hours ago',
                    },
                    {
                      icon: '🏢',
                      title: 'Apple AI Announcement',
                      impact: 'Positive',
                      details: 'Company announced major AI features coming to next generation iPhones',
                      time: '4 hours ago',
                    },
                    {
                      icon: '📊',
                      title: 'Analyst Upgrade',
                      impact: 'Positive',
                      details: 'Morgan Stanley upgraded AAPL to overweight with $200 price target',
                      time: '6 hours ago',
                    },
                    {
                      icon: '🌍',
                      title: 'Better Than Expected China Sales',
                      impact: 'Positive',
                      details: 'Sales in Greater China exceeded analyst expectations despite market slowdown',
                      time: '8 hours ago',
                    },
                  ].map((catalyst, idx) => (
                    <div
                      key={idx}
                      className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:border-blue-400 dark:hover:border-blue-600 transition-all cursor-pointer"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div className="flex items-start gap-4">
                          <span className="text-3xl">{catalyst.icon}</span>
                          <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                              {catalyst.title}
                            </h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                              {catalyst.details}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                            catalyst.impact.includes('Major Positive')
                              ? 'bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100'
                              : catalyst.impact.includes('Positive')
                              ? 'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100'
                              : 'bg-yellow-100 dark:bg-yellow-900 text-yellow-900 dark:text-yellow-100'
                          }`}>
                            {catalyst.impact}
                          </span>
                          <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                            {catalyst.time}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Historical Context */}
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Historical Context
                </h3>

                <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        52-Week High
                      </p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        $199.62
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        52-Week Low
                      </p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        $143.30
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Market Cap
                      </p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        $2.8T
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-20 space-y-6">
                {/* Movement Summary */}
                <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
                    📈 Movement Summary
                  </h4>
                  <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Strong positive catalysts</li>
                    <li>• Above 50-day average</li>
                    <li>• High trading volume</li>
                    <li>• Bullish momentum</li>
                  </ul>
                </div>

                {/* Impact Assessment */}
                <div className="p-6 rounded-xl bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800">
                  <h4 className="font-semibold text-purple-900 dark:text-purple-100 mb-3">
                    Impact Assessment
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span>Earnings Impact</span>
                        <span className="font-bold">75%</span>
                      </div>
                      <div className="w-full bg-purple-200 dark:bg-purple-800 rounded-full h-2">
                        <div className="bg-purple-600 dark:bg-purple-400 h-2 rounded-full" style={{ width: '75%' }}></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span>Analyst Rating</span>
                        <span className="font-bold">60%</span>
                      </div>
                      <div className="w-full bg-purple-200 dark:bg-purple-800 rounded-full h-2">
                        <div className="bg-purple-600 dark:bg-purple-400 h-2 rounded-full" style={{ width: '60%' }}></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span>Market Sentiment</span>
                        <span className="font-bold">45%</span>
                      </div>
                      <div className="w-full bg-purple-200 dark:bg-purple-800 rounded-full h-2">
                        <div className="bg-purple-600 dark:bg-purple-400 h-2 rounded-full" style={{ width: '45%' }}></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Forecast */}
                <div className="p-6 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <h4 className="font-semibold text-green-900 dark:text-green-100 mb-3">
                    🎯 AI Forecast
                  </h4>
                  <p className="text-sm text-green-800 dark:text-green-200 mb-4">
                    Potential for further upside in near term based on positive catalysts.
                  </p>
                  <div className="flex gap-2">
                    <div className="flex-1 text-center p-2 rounded bg-white dark:bg-green-900">
                      <p className="text-xs text-green-900 dark:text-green-100">48H</p>
                      <p className="text-lg font-bold text-green-600 dark:text-green-400">+1.2%</p>
                    </div>
                    <div className="flex-1 text-center p-2 rounded bg-white dark:bg-green-900">
                      <p className="text-xs text-green-900 dark:text-green-100">1W</p>
                      <p className="text-lg font-bold text-green-600 dark:text-green-400">+2.8%</p>
                    </div>
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
              Understand market movements with AI-powered analysis
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
              Analyze Any Stock
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
