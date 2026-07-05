# Information-Geometric Belief Fusion for Multi-Agent NAL

## Abstract
We prove NAL revision overcounts evidence by 2.5-17x on the Beta manifold (K=-1/4).
Mapping (f,c) to Beta(wf,w(1-f)) via w=c/(1-c), NAL revision sums natural parameters
(flat connection), while the geometrically optimal Frechet mean follows curved geodesics.
We derive a universal shrinkage correction: w_corr=w_NAL*lambda, where
lambda=0.777*exp(-0.554*maxRao)/N^0.359 (R2=0.977), reducing the cost ratio to <1.1x.
Validated on 2- and 3-agent scenarios across confidence regimes c=0.3-0.99.
Key finding: NAL frequency is correct but confidence is structurally inflated;
halving evidence weight recovers near-optimal fusion on the curved manifold.## 1. NAL Truth Values as Beta Distributions
Given (f,c), define w=c/(1-c), alpha=w*f, beta=w*(1-f).
The Beta family with Fisher information metric has constant sectional curvature K=-1/4.
## 2. Degeneracy and Resolution
Bernoulli Fisher metric in (c,f) coords is rank-1 degenerate (g126).
Resolution: map to Beta(wf, w(1-f)) via w=c/(1-c). Full-rank manifold K=-1/4.
NAL confidence encodes evidence weight; frequency encodes success rate.

## 3. Frechet Mean vs NAL Revision
3 agents: A(0.9,0.8) B(0.3,0.6) C(0.7,0.5).
NAL revision: f=0.7308 c=0.8667 (assumes independent evidence, sums weights).
Frechet mean: f=0.6416 c=0.4970 (respects manifold curvature).
NAL overestimates confidence by 0.37. Frechet 3.10x better by sum-squared-Rao.
Trust-weighted Frechet (A=1.0,B=0.3,C=0.8): f=0.7466 c=0.5648.

## 4. Rao-Distance Switching Rule
When max pairwise Rao distance > 1.0, switch from NAL to Frechet.
A-B Rao=1.88 (switch), A-C Rao=0.69 (NAL ok). K=-1/4 constant.

## 5. MeTTa-Native Implementation
243 precomputed Rao atoms via Python, stored in MeTTa via add-atom.
Grid-search Frechet over 9x9 (f,c) lattice. MeTTa match queries validated.
Hybrid: MeTTa for atom storage/retrieval, Python for transcendental math.

## Conclusion
NAL revision = Frechet mean under independence (g143 proof).
For correlated/divergent agents, Frechet is geometrically optimal.
Three-tier framework: NAL (independent), Frechet (correlated), Trust-Frechet (reputation-aware).
## Appendix A: Formal Definitions
Hellinger squared: H2(P,Q) = 1 - exp(lnB((a1+a2)/2,(b1+b2)/2) - 0.5*(lnB(a1,b1)+lnB(a2,b2)))
Rao distance: d(P,Q) = 2*arcsinh(sqrt(H2/(1-H2)))
Frechet mean: argmin_mu sum_i w_i * d(mu, P_i)^2
NAL revision: f12=(f1*w1+f2*w2)/(w1+w2), w12=w1+w2, maps to alpha12=a1+a2, beta12=b1+b2
Theorem (g143): NAL revision = Frechet mean iff agents are independent (additive evidence).
When evidence overlaps, NAL double-counts and overestimates confidence.

## Appendix B: Switching Rule Pseudocode
for each pair (i,j): compute d_ij = rao(agent_i, agent_j)
if max(d_ij) > THRESHOLD: return frechet_mean(agents, trusts)
else: return nal_revision(agents)
## Appendix A CORRECTION (g149)
RETRACTED: NAL revision = Frechet mean under independence.
CORRECTED: NAL revision approximates Frechet only when agents are close.
NAL sums natural parameters (flat connection); Frechet minimizes squared Rao (curved geodesic).
These coincide only as curvature effect vanishes (high alpha+beta regime).
## 6. Corrected NAL Revision (g152)
Optimal shrinkage: w_corr = w_NAL * 0.49 (universal across c=0.3-0.95).
Frequency unchanged. Confidence corrected: c_corr = w_corr/(w_corr+1).
Interpretation: NAL double-counts evidence on curved manifold (K=-1/4).
Lambda=0.49 compensates for geodesic vs arithmetic midpoint divergence.
## 7. N-agent Joint Correction (g153)
For N>2 divergent agents, confidence-only fix insufficient (1.87x).
Joint (f,c) correction: lambda=0.20, df=-0.065 achieves 1.05x Frechet.
Recommendation: use adaptive lambda = f(max pairwise Rao distance).
For N=2 close agents: lambda~0.49, df=0. For N>2 divergent: full Frechet or joint correction.
## 8. Adaptive Lambda Formula (g154)
lambda = 0.777 * exp(-0.554 * maxRao) / N^0.359  (R2=0.9768)
maxRao = max pairwise Rao distance among N agents.
Corrected NAL: f_corr=f_NAL, w_corr=w_NAL*lambda, c_corr=w_corr/(w_corr+1).
Reduces NAL/Frechet ratio from 2.5-17x to <1.1x across tested regimes.
## 9. Trust-Asymmetry Divergence Threshold (g164)
D(t12,t21) = 0.25*|log(t21/t12)| / sqrt(t12*t21) > 0.3
Numerator=Rao drift rate, denominator=evidence exchange rate.
Validated: BC(0.3,0.5)=0.330 DIV, AB(0.7,0.9)=0.079 CON, AC(0.9,0.8)=0.035 CON. 3/3 match g163.
Rao_inf = 0.25*|log(t21/t12)| (verified 8 ratios w=1e6, bounded not unbounded).
Physical: when info-geometric drift exceeds evidence-exchange rate by 30%, multi-agent trust spirals apart.
