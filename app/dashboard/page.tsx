import ToolCard from '@/components/ToolCard';

export default function DashboardPage() {
  const tools = [
    {
      icon: '📄',
      title: 'Upload Financial Report',
      description:
        'Structured PDF summary: insights, risks, opportunities, extracted figures, and beginner walkthrough (INR-aware).',
      href: '/dashboard/pdf',
    },
    {
      icon: '📊',
      title: 'Chart Pattern Analyzer',
      description:
        'AI vision + geometry fallback for patterns, support/resistance, trendlines, breakouts — with confidence and reasoning.',
      href: '/dashboard/chart',
    },
    {
      icon: '📈',
      title: 'Market Sentiment',
      description:
        'News-driven sentiment tuned for India (Nifty, RBI, flows, INR…): drivers, reasoning, and headlines.',
      href: '/dashboard/sentiment',
    },
    {
      icon: '🎮',
      title: 'Trade Simulator',
      description: 'Practice trading with virtual capital in a risk-free environment with AI guidance.',
      href: '/dashboard/simulator',
    },
    {
      icon: '🔍',
      title: 'Stock Movement Analysis',
      description: 'Understand why stocks are moving with AI-powered news and catalyst analysis.',
      href: '/dashboard/movement',
    },
  ];

  return (
    <div className="w-full">
      {/* Header Section */}
      <section className="py-16 bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-black dark:via-gray-950 dark:to-black border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4">
              Dashboard
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
              Indian-market-focused tools plus one <span className="font-medium text-gray-800 dark:text-gray-200">BharatTrade Copilot</span> — use the floating chat for follow-ups; it remembers your latest PDF, chart, and sentiment results.
            </p>
          </div>

          <div className="mb-10 rounded-xl border border-indigo-200 bg-indigo-50/80 p-5 dark:border-indigo-900 dark:bg-indigo-950/40">
            <p className="text-sm text-indigo-950 dark:text-indigo-100">
              New to NSE/BSE? Read{' '}
              <a href="/learn/india" className="font-medium underline">
                India markets 101
              </a>{' '}
              then ask the Copilot anything (F&amp;O vs equity, timings, SEBI basics, or “what does my chart mean?”).
            </p>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
              <p className="text-sm text-gray-600 dark:text-gray-400">Available Tools</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">5</p>
            </div>
            <div className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
              <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
              <p className="text-3xl font-bold text-green-600 dark:text-green-400">Active</p>
            </div>
            <div className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
              <p className="text-sm text-gray-600 dark:text-gray-400">Learning Path</p>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">Beginner</p>
            </div>
          </div>
        </div>
      </section>

      {/* Tools Grid */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-12">
            Choose a Tool to Get Started
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {tools.map((tool, index) => (
              <ToolCard key={index} {...tool} />
            ))}
          </div>
        </div>
      </section>

      {/* Getting Started Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-12">
            Getting Started
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {[
              {
                number: '1',
                title: 'Choose Your Tool',
                description: 'Select from our 5 AI-powered tools based on what you want to learn.',
              },
              {
                number: '2',
                title: 'Follow the Guide',
                description: 'Each tool comes with on-screen guidance to help you get the most out of it.',
              },
              {
                number: '3',
                title: 'Learn & Practice',
                description: 'Use the insights to deepen your stock market knowledge and practice trading.',
              },
            ].map((step, index) => (
              <div
                key={index}
                className="p-8 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-600 transition-all"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg mb-4">
                  {step.number}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {step.description}
                </p>
              </div>
            ))}
          </div>

          {/* Tips Section */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-8">
            <h3 className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-4">
              💡 Tips for Success
            </h3>
            <ul className="space-y-3 text-blue-800 dark:text-blue-200">
              <li className="flex items-start">
                <span className="mr-3">→</span>
                <span>Start with the PDF Report Explainer to understand company fundamentals</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">→</span>
                <span>Move to Chart Patterns to learn technical analysis</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">→</span>
                <span>Practice with the Trade Simulator before making real trades</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">→</span>
                <span>Use Stock Movement Analysis to understand market catalysts</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Learning Resources Section */}
      <section className="py-20 bg-white dark:bg-black border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Learning Resources
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 mb-12">
            Supplement your learning with these helpful resources:
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <a
              href="#"
              className="p-8 rounded-xl bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all hover:shadow-lg group"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                📚 Stock Market Glossary
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Learn common stock market terms and concepts with simple explanations.
              </p>
            </a>

            <a
              href="#"
              className="p-8 rounded-xl bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all hover:shadow-lg group"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                🎓 Educational Articles
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Deep-dive articles on various stock market topics and strategies.
              </p>
            </a>

            <a
              href="#"
              className="p-8 rounded-xl bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all hover:shadow-lg group"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                🎬 Video Tutorials
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Watch step-by-step video guides for each tool and feature.
              </p>
            </a>

            <a
              href="#"
              className="p-8 rounded-xl bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all hover:shadow-lg group"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                💬 Community Forum
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Ask questions and share insights with our learning community.
              </p>
            </a>
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="py-12 bg-yellow-50 dark:bg-yellow-900/10 border-t border-yellow-200 dark:border-yellow-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="p-6 bg-white dark:bg-gray-900 rounded-lg border border-yellow-200 dark:border-yellow-800">
            <p className="text-yellow-900 dark:text-yellow-100">
              <strong>⚠️ Disclaimer:</strong> StockSense AI provides educational content only. This is not financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
