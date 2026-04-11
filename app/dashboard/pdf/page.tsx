'use client';

import Link from 'next/link';
import { useState, useRef } from 'react';

interface AnalysisResult {
  company_summary: string;
  key_positives: string[];
  risks: string[];
  future_outlook: string;
}

interface ErrorState {
  message: string;
  details?: string;
}

export default function PDFToolPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<ErrorState | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    // Reset states
    setError(null);
    setAnalysis(null);
    setFileName(null);

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError({
        message: 'Invalid file type',
        details: 'Please upload a PDF file only.',
      });
      return;
    }

    // Validate file size (max 25MB)
    const maxSize = 25 * 1024 * 1024;
    if (file.size > maxSize) {
      setError({
        message: 'File too large',
        details: 'Please upload a PDF smaller than 25MB.',
      });
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

      const response = await fetch('http://localhost:8000/analyze-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `Server error: ${response.status}`
        );
      }

      const result: AnalysisResult = await response.json();
      setAnalysis(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError({
        message: 'Failed to analyze PDF',
        details:
          errorMessage === 'Failed to fetch'
            ? 'Backend server not running. Please start it on http://localhost:8000'
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

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

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
            {/* Upload Area or Results */}
            <div className="lg:col-span-2">
              {!analysis && !isLoading && (
                <>
                  {/* Upload Area */}
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`bg-gray-50 dark:bg-gray-900 border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                      isDragging
                        ? 'border-blue-400 dark:border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                        : 'border-gray-300 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-600'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf"
                      onChange={handleInputChange}
                      className="hidden"
                    />
                    <div className="text-5xl mb-4">📄</div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      Upload Your Financial Report
                    </h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      Drag and drop your PDF or click to browse
                    </p>
                    <button
                      onClick={handleButtonClick}
                      className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                    >
                      Choose File
                    </button>
                    <p className="text-sm text-gray-500 dark:text-gray-500 mt-4">
                      Supported formats: PDF (up to 25MB)
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
                          Future Outlook
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Understand growth potential and trajectory
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
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                  <p className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
                    Analyzing your PDF...
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    This may take a moment
                  </p>
                </div>
              )}

              {/* Analysis Results */}
              {analysis && !isLoading && (
                <div className="space-y-8">
                  {/* File Name */}
                  <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                    <p className="text-sm text-green-900 dark:text-green-100">
                      ✓ Successfully analyzed: <span className="font-medium">{fileName}</span>
                    </p>
                  </div>

                  {/* Company Summary */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                      📋 Company Summary
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                      {analysis.company_summary}
                    </p>
                  </div>

                  {/* Key Positives */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-green-600 dark:text-green-400 mb-4">
                      ✓ Key Positives
                    </h3>
                    <ul className="space-y-3">
                      {analysis.key_positives.map((positive, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-3 text-gray-700 dark:text-gray-300"
                        >
                          <span className="mt-1 text-green-600 dark:text-green-400 font-bold">
                            •
                          </span>
                          <span>{positive}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Risks */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
                      ⚠️ Risks
                    </h3>
                    <ul className="space-y-3">
                      {analysis.risks.map((risk, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-3 text-gray-700 dark:text-gray-300"
                        >
                          <span className="mt-1 text-red-600 dark:text-red-400 font-bold">
                            •
                          </span>
                          <span>{risk}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Future Outlook */}
                  <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-3">
                      🔮 Future Outlook
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                      {analysis.future_outlook}
                    </p>
                  </div>

                  {/* Upload Another */}
                  <button
                    onClick={() => {
                      setAnalysis(null);
                      setFileName(null);
                      setError(null);
                      fileInputRef.current?.click();
                    }}
                    className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                  >
                    Analyze Another Report
                  </button>
                </div>
              )}
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
    </div>
  );
}
