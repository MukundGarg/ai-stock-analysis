export function normalizeAnalysis(data: any) {
  return {
    market_reaction: "",
    catalyst_type: "unknown",
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
