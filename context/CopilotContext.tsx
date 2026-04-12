'use client';

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { getApiUrl } from '@/lib/api';

const SESSION_KEY = 'stocksense_copilot_session_v2';

export type WorkspaceContext = {
  sourcePage?: string;
  lastPdfAnalysis?: unknown;
  lastChartAnalysis?: unknown;
  lastSentiment?: unknown;
  updatedAt?: string;
};

type CopilotContextValue = {
  sessionId: string | null;
  workspace: WorkspaceContext;
  setLastPdfAnalysis: (data: unknown, page?: string) => void;
  setLastChartAnalysis: (data: unknown, page?: string) => void;
  setLastSentiment: (data: unknown, page?: string) => void;
  clearWorkspace: () => void;
  sendCopilotMessage: (text: string) => Promise<{ reply: string; sessionId: string }>;
};

const CopilotContext = createContext<CopilotContextValue | null>(null);

export function CopilotProvider({ children }: { children: React.ReactNode }) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [workspace, setWorkspace] = useState<WorkspaceContext>({});

  useEffect(() => {
    try {
      let s = localStorage.getItem(SESSION_KEY);
      if (!s) {
        s = crypto.randomUUID();
        localStorage.setItem(SESSION_KEY, s);
      }
      setSessionId(s);
    } catch {
      setSessionId(crypto.randomUUID());
    }
  }, []);

  const persistSession = useCallback((sid: string) => {
    setSessionId(sid);
    try {
      localStorage.setItem(SESSION_KEY, sid);
    } catch {
      /* ignore */
    }
  }, []);

  const setLastPdfAnalysis = useCallback((data: unknown, page = '/dashboard/pdf') => {
    setWorkspace((w) => ({
      ...w,
      lastPdfAnalysis: data,
      sourcePage: page,
      updatedAt: new Date().toISOString(),
    }));
  }, []);

  const setLastChartAnalysis = useCallback((data: unknown, page = '/dashboard/chart') => {
    setWorkspace((w) => ({
      ...w,
      lastChartAnalysis: data,
      sourcePage: page,
      updatedAt: new Date().toISOString(),
    }));
  }, []);

  const setLastSentiment = useCallback((data: unknown, page = '/dashboard/sentiment') => {
    setWorkspace((w) => ({
      ...w,
      lastSentiment: data,
      sourcePage: page,
      updatedAt: new Date().toISOString(),
    }));
  }, []);

  const clearWorkspace = useCallback(() => setWorkspace({}), []);

  const sendCopilotMessage = useCallback(
    async (text: string) => {
      const api = getApiUrl();
      const res = await fetch(`${api}/copilot/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          workspace_context: Object.keys(workspace).length ? workspace : undefined,
        }),
      });
      const raw = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error((raw as { error?: string }).error || `Copilot error (${res.status})`);
      }
      const data = raw as { reply: string; session_id: string };
      persistSession(data.session_id);
      return { reply: data.reply, sessionId: data.session_id };
    },
    [sessionId, workspace, persistSession]
  );

  const value = useMemo(
    () => ({
      sessionId,
      workspace,
      setLastPdfAnalysis,
      setLastChartAnalysis,
      setLastSentiment,
      clearWorkspace,
      sendCopilotMessage,
    }),
    [
      sessionId,
      workspace,
      setLastPdfAnalysis,
      setLastChartAnalysis,
      setLastSentiment,
      clearWorkspace,
      sendCopilotMessage,
    ]
  );

  return <CopilotContext.Provider value={value}>{children}</CopilotContext.Provider>;
}

export function useCopilot() {
  const ctx = useContext(CopilotContext);
  if (!ctx) {
    throw new Error('useCopilot must be used within CopilotProvider');
  }
  return ctx;
}
