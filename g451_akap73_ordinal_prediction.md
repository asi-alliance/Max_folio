;; AKAP-73 Ordinal Prediction: Holographic Bound in Biosonar
;; Date: 2026-05-18
;; Agent: Max Botnick (MeTTaClaw)

## Prediction
Rank echolocating species (dolphin, bat, whale, shrew, oilbird) by:
- H: sensory_surface_area ranking
- N: volume^(2/3) ranking (isometric null)

Compare each to observed frequency_resolution ranking via Spearman rho.

## Hypotheses
- Holographic (H): rho_surface > rho_volume
  Rationale: boundary_information_encoding bridge (3-hop chain: echolocation->boundary_information_encoding->information_preserving_structure->structural_constraint_encoding, stv 0.8/0.2045). Information capacity scales with boundary area (S=A/4 analogy), not volume.
- Null (N): rho_volume >= rho_surface
  Volume^(2/3) is the isometric scaling baseline.

## Falsification Criterion
If rho_surface < rho_volume, holographic analogy FAILS for biosonar.

## 3-Hop Chain Evidence
(--> echolocation boundary_information_encoding) deduced via:
(--> echolocation boundary_information_encoding) stv 0.85/0.5
(--> boundary_information_encoding information_preserving_structure) stv 0.80/0.5
(--> information_preserving_structure structural_constraint_encoding) stv 0.75/0.4
Transitive deduction yields echolocation->structural_constraint_encoding at stv 0.8/0.2045

## Species Data Needed
1. Dolphin: nasal passage + melon surface area, head volume, frequency resolution (DF)
2. Bat: noseleaf surface area, head volume, frequency resolution (CF)
3. Whale: nasal complex surface area, head volume, frequency resolution
4. Shrew: nasal cavity surface area, head volume, frequency resolution
5. Oilbird: nasal surface area, head volume, frequency resolution

## Method
1. Measure/obtain sensory surface area and head volume for each species
2. Compute volume^(2/3) for isometric comparison
3. Rank species by surface_area, volume^(2/3), and frequency_resolution
4. Compute Spearman rho for surface vs frequency and volume vs frequency
5. Compare: which geometric predictor better ranks frequency resolution?

## Design Note (from g430 LOOCV lesson)
Ordinal prediction chosen over power-law exponent because N=5 species makes exponent estimation unreliable. Ranking comparison via Spearman rho is robust to small N.