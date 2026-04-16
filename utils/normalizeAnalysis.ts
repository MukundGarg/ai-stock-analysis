export function normalizeAnalysis(data: any) {
  return {
    executive_summary: "",
    ai_market_signal: { signal: "Neutral", confidence: 50 },
    company_snapshot: "",
    beginner_walkthrough: "",
    key_insights: [],
    strategic_intent: [],
    key_positives: [],
    risks: [],
    analyst_watchlist: [],
    market_impact_strength: {
      level: "Medium",
      probability_shift: 50,
      reasoning: "Insufficient data"
    },
    directional_bias: {
      bias: "Neutral",
      conviction: "Moderate",
      reasoning: "Insufficient data"
    },
    institutional_interpretation: "",
    hidden_signals: [],
    forward_watch: [],
    analysis_mode: data?.analysis_mode || undefined,
    fallback_reason: data?.fallback_reason || undefined,
    setup_hint: data?.setup_hint || undefined,
    fallback_detail: data?.fallback_detail || undefined,
    ...(data || {})
  };
}
