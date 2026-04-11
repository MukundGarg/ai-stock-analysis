'use client';

import Link from 'next/link';

export default function PDFToolPage() {
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
            📄 PDF Financial Report Explainer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Upload financial reports and get AI-powered explanations
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload Area */}
            <div className="lg:col-span-2">
              <div className="bg-gray-50 dark:bg-gray-900 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-12 text-center hover:border-blue-400 dark:hover:border-blue-600 transition-colors cursor-pointer">
                <div className="text-5xl mb-4">📄</div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Upload Your Financial Report
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Drag and drop your PDF or click to browse
                </p>
                <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
                  Choose File
                </button>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-4">
                  Supported formats: PDF (up to 50MB)
                </p>
              </div>

              {/* Features */}
              <div className="mt-12">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  What You Can Do
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <div className="text-3xl mb-3">🔍</div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Analyze Metrics
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      Get detailed explanations of all key financial metrics
                    </p>
                  </div>

                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <div className="text-3xl mb-3">💡</div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Get Insights
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      Understand what the numbers mean for the company
                    </p>
                  </div>

                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <div className="text-3xl mb-3">⚠️</div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Risk Assessment
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      Identify potential risks and concerns
                    </p>
                  </div>

                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <div className="text-3xl mb-3">📊</div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Visual Reports
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      Get charts and visualizations of trends
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-20 space-y-6">
                {/* Info Box */}
                <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-3">
                    💡 Pro Tips
                  </h4>
                  <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Start with quarterly reports</li>
                    <li>• Compare year-over-year data</li>
                    <li>• Look for trends in margins</li>
                    <li>• Check balance sheet strength</li>
                  </ul>
                </div>

                {/* Supported Documents */}
                <div className="p-6 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Supported Documents
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• 10-K Annual Reports</li>
                    <li>• 10-Q Quarterly Reports</li>
                    <li>• 8-K Current Reports</li>
                    <li>• Earnings Call Transcripts</li>
                    <li>• Investor Presentations</li>
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
              Start analyzing financial reports powered by AI
            </p>
            <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium">
              Upload Report
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
