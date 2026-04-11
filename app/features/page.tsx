import FeatureCard from '@/components/FeatureCard';

export default function FeaturesPage() {
  const features = [
    {
      icon: '📄',
      title: 'PDF Financial Report Explainer',
      description: 'Upload and get AI-powered explanations of financial reports. Understand balance sheets, income statements, and cash flow statements like never before.',
    },
    {
      icon: '📊',
      title: 'Chart Pattern Explainer',
      description: 'Learn to recognize and analyze stock chart patterns. Get insights into what patterns mean and how they can guide your trading decisions.',
    },
    {
      icon: '📈',
      title: 'Market Sentiment AI',
      description: 'Track real-time market sentiment and understand what the market is feeling. Get insights into bullish and bearish trends.',
    },
    {
      icon: '🎮',
      title: 'AI Trade Simulator',
      description: 'Practice trading in a risk-free environment. Use AI-powered recommendations to improve your trading strategy without losing real money.',
    },
    {
      icon: '🔍',
      title: 'Why is This Stock Moving?',
      description: 'Get instant explanations for why stocks are moving. Understand the catalysts behind daily price movements with AI analysis.',
    },
  ];

  return (
    <div className="w-full">
      {/* Header Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Features
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              StockSense AI comes with 5 powerful, AI-driven tools designed to accelerate your stock market learning journey.
            </p>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* Feature Details Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-12 text-center">
            How Each Tool Works
          </h2>

          {/* Feature 1 */}
          <div className="mb-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="text-5xl mb-4">📄</div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                PDF Financial Report Explainer
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
                Simply upload any financial report, quarterly earnings document, or SEC filing. Our AI analyzes the document and provides:
              </p>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-start">
                  <span className="text-blue-600 dark:text-blue-400 font-bold mr-3">✓</span>
                  <span>Key metrics explained in simple language</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 dark:text-blue-400 font-bold mr-3">✓</span>
                  <span>What the numbers mean for the company</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 dark:text-blue-400 font-bold mr-3">✓</span>
                  <span>Investment implications and risk analysis</span>
                </li>
              </ul>
            </div>
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="bg-gray-100 dark:bg-gray-900 rounded-lg h-64 flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Feature Preview</p>
              </div>
            </div>
          </div>

          {/* Feature 2 */}
          <div className="mb-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center md:order-last">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="bg-gray-100 dark:bg-gray-900 rounded-lg h-64 flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Feature Preview</p>
              </div>
            </div>
            <div>
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Chart Pattern Explainer
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
                Master the art of reading stock charts. Our AI tool helps you understand:
              </p>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-start">
                  <span className="text-purple-600 dark:text-purple-400 font-bold mr-3">✓</span>
                  <span>Common patterns: Head & Shoulders, Double Tops, Triangles</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-600 dark:text-purple-400 font-bold mr-3">✓</span>
                  <span>Support and resistance levels</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-600 dark:text-purple-400 font-bold mr-3">✓</span>
                  <span>Trading opportunities and risk zones</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="mb-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="text-5xl mb-4">📈</div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Market Sentiment AI
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
                Stay ahead of market trends with real-time sentiment analysis:
              </p>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-start">
                  <span className="text-green-600 dark:text-green-400 font-bold mr-3">✓</span>
                  <span>Overall market sentiment index</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-600 dark:text-green-400 font-bold mr-3">✓</span>
                  <span>Sector-wise sentiment breakdown</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-600 dark:text-green-400 font-bold mr-3">✓</span>
                  <span>Fear and greed indicators</span>
                </li>
              </ul>
            </div>
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="bg-gray-100 dark:bg-gray-900 rounded-lg h-64 flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Feature Preview</p>
              </div>
            </div>
          </div>

          {/* Feature 4 */}
          <div className="mb-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center md:order-last">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="bg-gray-100 dark:bg-gray-900 rounded-lg h-64 flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Feature Preview</p>
              </div>
            </div>
            <div>
              <div className="text-5xl mb-4">🎮</div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                AI Trade Simulator
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
                Practice trading without risking real money:
              </p>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-start">
                  <span className="text-orange-600 dark:text-orange-400 font-bold mr-3">✓</span>
                  <span>Start with virtual capital</span>
                </li>
                <li className="flex items-start">
                  <span className="text-orange-600 dark:text-orange-400 font-bold mr-3">✓</span>
                  <span>Execute real trades in a sandbox</span>
                </li>
                <li className="flex items-start">
                  <span className="text-orange-600 dark:text-orange-400 font-bold mr-3">✓</span>
                  <span>Get AI feedback and recommendations</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Feature 5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Why is This Stock Moving?
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
                Get instant explanations for market movements:
              </p>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-start">
                  <span className="text-red-600 dark:text-red-400 font-bold mr-3">✓</span>
                  <span>News and events analysis</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-600 dark:text-red-400 font-bold mr-3">✓</span>
                  <span>Earnings impact assessment</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-600 dark:text-red-400 font-bold mr-3">✓</span>
                  <span>Market catalyst identification</span>
                </li>
              </ul>
            </div>
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="bg-gray-100 dark:bg-gray-900 rounded-lg h-64 flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Feature Preview</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-900 dark:to-black border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Ready to Learn?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
            Access all features and start your stock market learning journey today.
          </p>
          <a
            href="/dashboard"
            className="inline-flex items-center justify-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl"
          >
            Go to Dashboard
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </a>
        </div>
      </section>
    </div>
  );
}
