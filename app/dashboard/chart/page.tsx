'use client';

import Link from 'next/link';
import { useState, useRef } from 'react';
import Image from 'next/image';

interface ChartAnalysisResult {
  pattern: string;
  signal: string;
  confidence: string;
  description: string;
}

interface ErrorState {
  message: string;
  details?: string;
}

export default function ChartToolPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<ChartAnalysisResult | null>(null);
  const [error, setError] = useState<ErrorState | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    // Reset states
    setError(null);
    setAnalysis(null);
    setFileName(null);
    setPreviewUrl(null);

    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      setError({
        message: 'Invalid file type',
        details: 'Please upload a PNG or JPG image only.',
      });
      return;
    }

    // Validate file size (max 5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setError({
        message: 'File too large',
        details: 'Please upload an image smaller than 5MB.',
      });
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setPreviewUrl(e.target.result as string);
      }
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

      const response = await fetch('http://localhost:8000/analyze-chart', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `Server error: ${response.status}`
        );
      }

      const result: ChartAnalysisResult = await response.json();
      setAnalysis(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError({
        message: 'Failed to analyze chart',
        details:
          errorMessage === 'Failed to fetch'
            ? 'Backend server not running. Please start it on http://localhost:8000'
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

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'Bullish':
        return 'bg-green-100 dark:bg-green-900/30 text-green-900 dark:text-green-100 border-green-300 dark:border-green-700';
      case 'Bearish':
        return 'bg-red-100 dark:bg-red-900/30 text-red-900 dark:text-red-100 border-red-300 dark:border-red-700';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-700';
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'High':
        return 'text-green-600 dark:text-green-400';
      case 'Medium':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'Low':
        return 'text-gray-600 dark:text-gray-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
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
            📊 Chart Pattern Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl">
            Upload stock chart images and get AI-powered pattern detection
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload or Results */}
            <div className="lg:col-span-2">
              {!analysis && !isLoading && !previewUrl && (
                <>
                  {/* Upload Area */}
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                      isDragging
                        ? 'border-blue-400 dark:border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                        : 'border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 hover:border-blue-400 dark:hover:border-blue-600'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".png,.jpg,.jpeg"
                      onChange={handleInputChange}
                      className="hidden"
                    />
                    <div className="text-5xl mb-4">📈</div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      Upload Your Chart Image
                    </h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      Drag and drop a chart image or click to browse
                    </p>
                    <button
                      onClick={handleButtonClick}
                      className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                    >
                      Choose Image
                    </button>
                    <p className="text-sm text-gray-500 dark:text-gray-500 mt-4">
                      Supported formats: PNG, JPG (up to 5MB)
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
                      Pattern Detection Features
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {[
                        { icon: '📈', title: 'Uptrend', desc: 'Identifies rising price trends' },
                        { icon: '📉', title: 'Downtrend', desc: 'Detects falling price trends' },
                        { icon: '⬆️⬆️', title: 'Double Top', desc: 'Recognizes reversal signals' },
                        { icon: '⬇️⬇️', title: 'Double Bottom', desc: 'Finds support potential' },
                      ].map((feature, idx) => (
                        <div
                          key={idx}
                          className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900"
                        >
                          <div className="text-3xl mb-3">{feature.icon}</div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                            {feature.title}
                          </h4>
                          <p className="text-gray-600 dark:text-gray-400 text-sm">
                            {feature.desc}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {/* Preview and Loading */}
              {(previewUrl || isLoading) && !analysis && (
                <div className="space-y-6">
                  {previewUrl && (
                    <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Chart Preview
                      </h3>
                      <div className="relative w-full h-60 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden">
                        <img
                          src={previewUrl}
                          alt="Chart preview"
                          className="w-full h-full object-contain"
                        />
                      </div>
                    </div>
                  )}

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
                        Analyzing chart...
                      </p>
                      <p className="text-gray-600 dark:text-gray-400">
                        Detecting patterns and trends
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Analysis Results */}
              {analysis && !isLoading && (
                <div className="space-y-6">
                  {/* File Name */}
                  <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                    <p className="text-sm text-green-900 dark:text-green-100">
                      ✓ Chart analyzed: <span className="font-medium">{fileName}</span>
                    </p>
                  </div>

                  {/* Pattern Result Card */}
                  <div className="p-8 rounded-lg border-2 border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                    <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                      {analysis.pattern}
                    </h3>

                    {/* Signal Badge */}
                    <div className="mb-6">
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Trading Signal
                      </p>
                      <div
                        className={`inline-block px-4 py-2 rounded-lg border text-lg font-semibold ${getSignalColor(
                          analysis.signal
                        )}`}
                      >
                        {analysis.signal}
                      </div>
                    </div>

                    {/* Confidence */}
                    <div className="mb-6">
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Analysis Confidence
                      </p>
                      <div className="flex items-center gap-2">
                        <div className={`text-2xl font-bold ${getConfidenceColor(analysis.confidence)}`}>
                          {analysis.confidence}
                        </div>
                        <div className="flex gap-1">
                          {[1, 2, 3].map((i) => (
                            <div
                              key={i}
                              className={`h-2 w-2 rounded-full ${
                                i <=
                                (analysis.confidence === 'High'
                                  ? 3
                                  : analysis.confidence === 'Medium'
                                  ? 2
                                  : 1)
                                  ? getConfidenceColor(analysis.confidence).replace('text-', 'bg-')
                                  : 'bg-gray-300 dark:bg-gray-600'
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Description */}
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Pattern Explanation
                      </p>
                      <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                        {analysis.description}
                      </p>
                    </div>
                  </div>

                  {/* Upload Another */}
                  <button
                    onClick={() => {
                      setAnalysis(null);
                      setFileName(null);
                      setPreviewUrl(null);
                      setError(null);
                      fileInputRef.current?.click();
                    }}
                    className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                  >
                    Analyze Another Chart
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
                    💡 Tips for Best Results
                  </h4>
                  <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Use clear, high-contrast charts</li>
                    <li>• Include full price history</li>
                    <li>• Avoid cluttered indicators</li>
                    <li>• Use candlestick or line charts</li>
                  </ul>
                </div>

                {/* Patterns Guide */}
                <div className="p-6 rounded-xl bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800">
                  <h4 className="font-semibold text-purple-900 dark:text-purple-100 mb-3">
                    📚 Pattern Guide
                  </h4>
                  <ul className="space-y-2 text-sm text-purple-800 dark:text-purple-200">
                    <li>
                      <strong>Bullish:</strong> Upward price movement
                    </li>
                    <li>
                      <strong>Bearish:</strong> Downward price movement
                    </li>
                    <li>
                      <strong>Neutral:</strong> Mixed signals
                    </li>
                  </ul>
                </div>

                {/* Limitations */}
                <div className="p-6 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800">
                  <h4 className="font-semibold text-amber-900 dark:text-amber-100 mb-3">
                    ⚠️ Disclaimer
                  </h4>
                  <p className="text-xs text-amber-800 dark:text-amber-200">
                    Pattern analysis is for educational purposes. Always do your own research and consult
                    professionals before trading.
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