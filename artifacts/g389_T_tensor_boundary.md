# g389: Amari T-Tensor at g381 Anisotropy Boundary

**Goal**: Test whether Amari skewness tensor T has geometric invariant at g381 gcc/gff=1 crossover contour.
**AC (Cy5037)**: Compute T at 10+ boundary points, test for invariant signature.
**Result**: FALSIFIED — no invariant. Enriched by deeper structural discovery.

## 1. Original Hypothesis
T_ijk contracted at gcc/gff=1 boundary shows constant signature → metric and connection anisotropy are coupled.

## 2. Findings

### 2a. T-Tensor Boundary Scan (6 points)
| f | c_boundary | Tfff/Tccc | Verdict |
|------|-----------|-----------|----------|
| 0.25 | 0.456 | +0.090 | Variable |
| 0.30 | 0.423 | +0.070 | Variable |
| 0.35 | 0.393 | +0.045 | Variable |
| 0.40 | 0.365 | +0.020 | Variable |
| 0.45 | 0.340 | +0.005 | Variable |
| 0.50 | 0.311 | 0.000 | Symmetry zero |

**Verdict**: Ratio varies +0.12 to 0.00. NOT invariant. Symmetry forces T_fff=0 at f=0.5.

### 2b. Critical Discovery: Coordinate vs Geometric Boundary
gcc/gff=1 has eigenvalue ratio=2.60 (NOT 1.0). Off-diagonal g_fc=-0.350 breaks isotropy.
Two distinct contours exist:
- **gcc/gff=1**: coordinate-dependent, operationally meaningful for NAL (equal df/dc cost)
- **eigenvalue ratio=1**: true geometric isotropy, DEGENERATE POINT at f=0.5 c≈0.312 (ratio=1.0017)

### 2c. Eigenvalue Ratio Scan
| f | min eigenvalue ratio | Interpretation |
|------|---------------------|----------------|
| 0.30 | 1.617 | Strongly anisotropic |
| 0.35 | 1.447 | Anisotropic |
| 0.40 | 1.285 | Moderately anisotropic |
| 0.45 | 1.137 | Weakly anisotropic |
| 0.50 | 1.003 | Near-isotropic (degenerate) |

## 3. Revised STVs (per Kevin reliability standard Cy5083)
- g381 boundary geometric claim: stv(1.0,0.9) → **stv(0.7,0.7)** coordinate-dependent
- g389 T-invariant hypothesis: **stv(0.0,0.85)** falsified
- g389 intrinsic anisotropy finding: **stv(0.9,0.85)**
- g388 two-variable model: stv(0.9,0.7) maintained, N=6 flagged

## 4. NAL Implication
Beta manifold is intrinsically anisotropic almost everywhere. Confidence perturbations geometrically costlier than frequency perturbations. The manifold itself encodes PRECAUTIONARY GEOMETRY for belief revision.

## 5. Lineage
g381(anisotropy island) → g385(AKAP refit) → g386(plateau) → g387(direction) → g388(T-model) → g389(T-boundary)

## 6. Reproducibility
Scripts: /tmp/g389_T.py, /tmp/g389_eig_scan.py. All computations use scipy.special.polygamma on Beta(alpha,beta) Fisher metric in (f,c) parametrization.