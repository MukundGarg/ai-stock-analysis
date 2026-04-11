'use client';

import Link from 'next/link';

export default function SimulatorToolPage() {
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
            🎮 AI Trade Simulator
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Practice trading with virtual capital and learn without risk
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Chart and Trading Area */}
            <div className="lg:col-span-2">
              {/* Portfolio Summary */}
              <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="p-6 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 border border-blue-200 dark:border-blue-800">
                  <p className="text-sm text-blue-900 dark:text-blue-300 mb-2">
                    Total Balance
                  </p>
                  <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                    $100,000
                  </p>
                </div>
                <div className="p-6 rounded-lg bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30 border border-green-200 dark:border-green-800">
                  <p className="text-sm text-green-900 dark:text-green-300 mb-2">
                    Portfolio Value
                  </p>
                  <p className="text-3xl font-bold text-green-600 dark:text-green-400">
                    $105,432
                  </p>
                </div>
                <div className="p-6 rounded-lg bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/30 dark:to-purple-800/30 border border-purple-200 dark:border-purple-800">
                  <p className="text-sm text-purple-900 dark:text-purple-300 mb-2">
                    Today's Return
                  </p>
                  <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                    +5.4%
                  </p>
                </div>
              </div>

              {/* Trading Area */}
              <div className="bg-gray-50 dark:bg-gray-900 p-8 rounded-xl border border-gray-200 dark:border-gray-800">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Execute a Trade
                </h2>

                <div className="space-y-6">
                  {/* Symbol Input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                      Stock Symbol
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., AAPL"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Quantity */}
                    <div>
                      <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                        Quantity (Shares)
                      </label>
                      <input
                        type="number"
                        placeholder="100"
                        className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>

                    {/* Order Type */}
                    <div>
                      <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                        Order Type
                      </label>
                      <select className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option>Market Order</option>
                        <option>Limit Order</option>
                        <option>Stop Loss</option>
                      </select>
                    </div>
                  </div>

                  {/* Trade Buttons */}
                  <div className="grid grid-cols-2 gap-4">
                    <button className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors">
                      Buy
                    </button>
                    <button className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors">
                      Sell
                    </button>
                  </div>
                </div>
              </div>

              {/* Holdings */}
              <div className="mt-12">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Your Holdings
                </h3>
                <div className="space-y-4">
                  {[
                    { symbol: 'AAPL', shares: 50, avgPrice: 150.25, current: 165.50, gain: '+10.2%' },
                    { symbol: 'MSFT', shares: 30, avgPrice: 320.00, current: 335.75, gain: '+4.9%' },
                    { symbol: 'TSLA', shares: 20, avgPrice: 230.00, current: 215.30, gain: '-6.4%' },
                  ].map((holding, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white">
                            {holding.symbol}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {holding.shares} shares @ ${holding.avgPrice}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold text-gray-900 dark:text-white">
                            ${holding.current}
                          </p>
                          <p className={`text-sm font-medium ${
                            holding.gain.startsWith('+')
                              ? 'text-green-600 dark:text-green-400'
                              : 'text-red-600 dark:text-red-400'
                          }`}>
                            {holding.gain}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-20 space-y-6">
                {/* AI Recommendations */}
                <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
                    🤖 AI Recommendations
                  </h4>
                  <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                    <li>• BUY: NVDA (Strong momentum)</li>
                    <li>• HOLD: AAPL (Stable)</li>
                    <li>• SELL: AMD (Resistance)</li>
                  </ul>
                </div>

                {/* Trading Rules */}
                <div className="p-6 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Trading Rules
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Risk max 2% per trade</li>
                    <li>• Set stop losses</li>
                    <li>• Take profits at 2:1 ratio</li>
                    <li>• Journal every trade</li>
                  </ul>
                </div>

                {/* Performance */}
                <div className="p-6 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <h4 className="font-semibold text-green-900 dark:text-green-100 mb-3">
                    📊 Performance
                  </h4>
                  <ul className="space-y-2 text-sm text-green-800 dark:text-green-200">
                    <li>• Win Rate: 72%</li>
                    <li>• Avg Gain: +2.3%</li>
                    <li>• Avg Loss: -1.1%</li>
                  </ul>
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
              Start practicing with zero risk - learn by doing
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
              Start Trading
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
