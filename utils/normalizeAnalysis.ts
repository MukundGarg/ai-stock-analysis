export function normalizeAnalysis(data: any) {
  return {
    executive_summary: "",
    ai_market_signal: { signal: "Neutral", confidence: 50 },
    company_snapshot: "",
    beginner_walkthrough: "",
    strategic_intent: [],
    key_insights: [],
    key_positives: [],
    risks: [],
    analyst_watchlist: [],
    analysis_mode: data?.analysis_mode || undefined,
    fallback_reason: data?.fallback_reason || undefined,
    setup_hint: data?.setup_hint || undefined,
    fallback_detail: data?.fallback_detail || undefined,
    ...(data || {})
  };
}
