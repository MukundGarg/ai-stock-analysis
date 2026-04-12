'use client';

import { useCopilot } from '@/context/CopilotContext';
import { useCallback, useEffect, useRef, useState } from 'react';

type Msg = { role: 'user' | 'assistant'; content: string };

export default function CopilotDock() {
  const { sendCopilotMessage, workspace, clearWorkspace } = useCopilot();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  const onSend = useCallback(async () => {
    const t = input.trim();
    if (!t || loading) return;
    setInput('');
    setErr(null);
    setMessages((m) => [...m, { role: 'user', content: t }]);
    setLoading(true);
    try {
      const { reply } = await sendCopilotMessage(t);
      setMessages((m) => [...m, { role: 'assistant', content: reply }]);
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Something went wrong';
      setErr(msg);
      setMessages((m) => [
        ...m,
        {
          role: 'assistant',
          content:
            'I could not reach the copilot. Is the backend running with AI_PROVIDER and GEMINI_API_KEY or GROQ_API_KEY? ' +
            msg,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, sendCopilotMessage]);

  const hasContext =
    Boolean(workspace.lastPdfAnalysis || workspace.lastChartAnalysis || workspace.lastSentiment);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-[60] flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 transition hover:from-blue-700 hover:to-indigo-700 md:bottom-8 md:right-8"
        aria-label="Open trading copilot"
      >
        <span className="text-lg" aria-hidden>
          💬
        </span>
        Copilot
        {hasContext && (
          <span className="rounded-full bg-white/20 px-2 py-0.5 text-xs">Context on</span>
        )}
      </button>

      {open && (
        <div
          className="fixed inset-0 z-[70] flex justify-end bg-black/40 p-0 sm:p-4 sm:items-end sm:justify-end"
          role="dialog"
          aria-modal="true"
          aria-labelledby="copilot-title"
          onClick={() => setOpen(false)}
        >
          <div
            className="flex h-full w-full max-w-md flex-col bg-white shadow-2xl dark:bg-gray-950 sm:h-[min(640px,85vh)] sm:rounded-2xl sm:border sm:border-gray-200 sm:dark:border-gray-800"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3 dark:border-gray-800">
              <div>
                <h2 id="copilot-title" className="font-semibold text-gray-900 dark:text-white">
                  BharatTrade Copilot
                </h2>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  NSE/BSE-aware assistant · not financial advice
                </p>
              </div>
              <div className="flex gap-2">
                {hasContext && (
                  <button
                    type="button"
                    onClick={clearWorkspace}
                    className="rounded-lg px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-900"
                  >
                    Clear context
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-900"
                  aria-label="Close copilot"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="flex-1 space-y-3 overflow-y-auto px-4 py-3">
              {messages.length === 0 && (
                <div className="rounded-xl bg-gray-50 p-4 text-sm text-gray-600 dark:bg-gray-900 dark:text-gray-300">
                  <p className="mb-2 font-medium text-gray-900 dark:text-white">
                    Ask anything about Indian markets
                  </p>
                  <ul className="list-inside list-disc space-y-1 text-xs">
                    <li>“What is the difference between NSE and BSE?”</li>
                    <li>“Explain F&amp;O vs equity in simple terms.”</li>
                    <li>“What does my PDF or chart result mean?”</li>
                  </ul>
                  {hasContext && (
                    <p className="mt-3 text-xs text-blue-700 dark:text-blue-300">
                      Tool results from this session are attached — ask follow-ups.
                    </p>
                  )}
                </div>
              )}
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`max-w-[95%] rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                    m.role === 'user'
                      ? 'ml-auto bg-blue-600 text-white'
                      : 'mr-auto border border-gray-200 bg-gray-50 text-gray-800 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100'
                  }`}
                >
                  {m.content}
                </div>
              ))}
              {loading && (
                <div className="text-xs text-gray-500 dark:text-gray-400">Thinking…</div>
              )}
              {err && <div className="text-xs text-red-600 dark:text-red-400">{err}</div>}
              <div ref={endRef} />
            </div>

            <div className="border-t border-gray-200 p-3 dark:border-gray-800">
              <div className="flex gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), onSend())}
                  placeholder="Ask about markets, patterns, or your results…"
                  className="flex-1 rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:outline-none dark:border-gray-700 dark:bg-gray-900 dark:text-white"
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={onSend}
                  disabled={loading || !input.trim()}
                  className="rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
