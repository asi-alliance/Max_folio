BENCHMARK V2: SOURCE-ANCHORED VS BASELINE
================================
Baseline (no source tags):
  Exact cues: source recall 0.50
  Paraphrase cues: source recall 0.33

Source-anchored (with source prefixes):
  Exact cues: source recall 1.0
  Paraphrase cues: source recall 1.0

Conclusion: Source prefix in queries eliminates provenance degradation.
Content recall unchanged at 0.92-1.0 across all conditions.
Recommendation: adopt [source=X date=Y conf=Z] prefix standard.