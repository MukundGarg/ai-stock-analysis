export function normalizeAnalysis(data: any) {
  return {
    executive_summary: "",
    ai_market_signal: {},
    company_snapshot: "",
    strategic_intent: [],
    key_insights: [],
    key_positives: [],
    risks: [],
    analyst_watchlist: [],
    beginner_walkthrough: "",
    ...(data || {})
  };
}
