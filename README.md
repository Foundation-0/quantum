# `Foundation-0/quantum`

Exact, **zero-float, zero-dependency** pure Python 3 standard-library (`fractions.Fraction`, exact integers, and $\mathbb{Q}[i]$) verification instruments for **multi-slit Sorkin tomography, complex $U(1)$ surgical edge-severing, $\mathbb{Z}_4$-cover Fourier quantum erasers, GKSL Lindblad–Zeno Schur complements, and Tomita–Takesaki modular obstructions**, expressed in the 8-glyph Aletheia operator calculus (`⧄ ⧅ ⦷ ⟠ ⧇ ⦺ ⩩ ⫩`).

- **Zero third-party dependencies** (pure Python 3 stdlib only, `>=3.10`)
- **Zero floating-point numbers** in any theorem, verification check, or JSON receipt
- **Zero bare `assert`s** (all verification guards remain active under `python3 -O`)
- **Bit-identical deterministic receipts** across isolated interpreter modes (`-I -B`, `-I -O -B`, `-I -B -W error`, `-I -O -B -W error`)
- **Strict Epistemic Honesty (Law 4 & Law 5):** Every classical and modern foundation is explicitly quarantined as `N0` prior art (`R5-N0-01`..`R5-N0-04`), and the exact mathematical barriers separating these finite discrete theorems from continuum quantum field theory are disclosed up front.

---

## Quickstart

```bash
# List all 4 exact verification modules (runs cleanly from a fresh clone; or `pip install -e .` first)
PYTHONPATH=. python3 -s -B -m quantum list

# Run the entire zero-float verification suite and print canonical SHA-256 receipts
PYTHONPATH=. python3 -s -B -m quantum verify

# Emit canonical JSON receipt bundle
PYTHONPATH=. python3 -s -B -m quantum verify --json

# Run the full isolated (-I) test suite (all 4 modules + R5 mutation-killing suites + CLI checks)
python3 -I -B tests/run_all.py
```

---

## Modules & Verified Audit Receipts

| Module | Audit | Scope | Exact Core Result (Zero Floats) | Report |
|---|---|---|---|---|
| `quantum.double_slit_continuum` | `AUDIT-054` (`VERIFIED`, `N1`) | 4-regime double-slit & Sorkin triple-slit continuum-observer obstruction suite | Exact pure-bath $V^2 + D^2 \equiv 1$ & mixed-bath strict drop; 16-vertex Fine/Farkas CHSH no-go (`S = 14/5 > 2` with `0` signaling); `16x16` GKSL Schur dephasing `9/50`; Sorkin triple-slit separation (linear bath $I_{ABC} \equiv 0$, looped-Schur degree-0 invariant, quartic Kerr $\lambda^2$-scaling); parallel-sum continuum-observer screening & Rayleigh shunt ceiling. | [DOUBLE_SLIT_CONTINUUM_REPORT.md](reports/DOUBLE_SLIT_CONTINUUM_REPORT.md) |
| `quantum.gksl_lindblad_zeno` | `AUDIT-018` (`VERIFIED`, `N2`) | Exact multipole $N^3$ law & `16x16` GKSL Tomita–Takesaki / Zeno Schur / EP2 Jordan / Riccati bridge | Exact `N=2..10` CM $N^3$ scaling & $O(k^2)$ dipole cancellation to $O(k^4)$ quadrupole; Huygens–Steiner cross-term nullity; exact $[D_{\mathrm{CM}}, \Delta_\rho] \equiv 0$ on $V_{\mathrm{inv}}$ & KMS detailed balance; `16x16` Schur sweep `-(2\gamma_t + 2g^2/N^2\gamma_1)`; exact degenerate (`12 -> 8`) & split (`14 -> 12`) EP2 Jordan blocks; Riccati slow-manifold convergence & $O(16,\mathbb{Q})$ invariance. | [QUANTUM_UNIFICATION_REPORT.md](docs/QUANTUM_UNIFICATION_REPORT.md) |
| `quantum.modular_schur_quantum` | `AUDIT-041` (`VERIFIED`, `N1`) | Singular-boundary Schur/Krein inertia, pure-$\mathbb{Q}$ Page turnaround & 4-regime modular-Schur/GKSL obstructions | Tripartite Krein null-coupling $n_- = r_{\mathrm{cross}}$ (`GL`-invariant); `N=6` pure-$\mathbb{Q}$ Schmidt-dual Page turnaround; Werner $\mathcal{C}_{\mathrm{GKSL}} \equiv \frac{32}{3}\mathcal{O}_{\mathrm{clock}}$ constant across $O(2,\mathbb{Q})$ & reciprocal $\mathfrak{su}(2)$ freezing $S_{\mathrm{mod}}|_{\mathfrak{su}(2)} = \lambda(q)^{-1}$; generic non-commuting $[S_{\mathrm{mod}}, \Delta_A] \neq 0$ (`O(2,Q) x O(2,Q)`-invariant). | [HORIZON_SCHUR_MODULAR_REPORT.md](reports/HORIZON_SCHUR_MODULAR_REPORT.md) |
| `quantum.unified_obstruction` | `AUDIT-056` (`VERIFIED`, `N2` on Q2 / `N1` on Q1,Q3) | Unified Round-5 quantum operator theorems in the 8-glyph Aletheia calculus | **(Q1)** Universal $M$-slit looped-Schur Sorkin order law $I_M^{\mathrm{loop}}(g) = O(g^{M-2})$ ($M=2..5$, degree-0 intensity invariant) separating linear loops from quartic Kerr ($I_5^{\mathrm{quartic}} \equiv 0 \neq I_5^{\mathrm{loop}}$) + $M$-slit pure-bath $\mathcal{V}_M^2 + \mathcal{D}_M^2 \equiv 1$; **(Q2)** Universal complex $U(1)$ surgical edge-severing + exact two-phase ($\mathbb{Z}_4/\mathbb{Z}_2$) holographic interior Green's-function tomography down to $|B|=1$ (`G_cut(0,1) = 3/7`) + $\mathbb{Z}_4$-cover 4-slit Fourier deck-splitting eraser; **(Q3)** Unified Werner eraser / CHSH (`V > 5/7`) / modular-Schur freezing / $O(2,\mathbb{Q})$ GKSL equalizer bridge. | [QUANTUM_UNIFICATION_REPORT.md](docs/QUANTUM_UNIFICATION_REPORT.md) |

---

## 8-Glyph Aletheia Calculus Laws (Verified `Sm` Unicode Basis)

| Law | 8-Glyph Statement | ASCII Fallback |
|---|---|---|
| **Q1 ($M$-Slit Sorkin Order Law)** | `I_M(G ⧄ S) ⩩ O(g^(M-2)), ⧇_M(λ·α) ⩩ ⧇_M(α), I_5^quartic ⩩ 0 != I_5^loop` | `I_M(G \|/\| S) =#= O(g^(M-2)), [o]_M(lam*alpha) =#= [o]_M(alpha), I_5^quartic =#= 0 != I_5^loop` |
| **Q2a ($U(1)$ Surgical Severing & Tomography)** | `(L ⦷ u_e*) ⧄ 1_B ⩩ Λ^(G\e*) - Λ^(G); G_cut(u,v) ⩩ 2/Φ(-1) - 1/Φ(i)` | `(L (\|\|) u_e*) \|/\| 1_B =#= Lam^(G\e*) - Lam^(G); G_cut(u,v) =#= 2/Phi(-1) - 1/Phi(i)` |
| **Q2b ($\mathbb{Z}_4$-Cover 4-Slit Eraser)** | `(F_4 ⊗ I_B)† (L_tilde ⧄ B_tilde) (F_4 ⊗ I_B) ⩩ 4 ⊕_{r=0..3} (L^(χ^r) ⧄ B)` | `(F_4 x I_B)^dag (L_tilde \|/\| B_tilde) (F_4 x I_B) =#= 4 (+)_(r=0..3) (L^(chi^r) \|/\| B)` |
| **Q3 (Modular–GKSL–Eraser Equalizer)** | `(Δ_ρ ⧄ B)|_{su(2)} ⩩ λ(V)^(-1) I_3; C_GKSL(U) ⟠_{O(2,Q)} (32/3) O_clock(V)` | `(Delta_rho \|/\| B)\|_{su(2)} =#= lam(V)^(-1) I_3; C_GKSL(U) <=>_{O(2,Q)} (32/3) O_clock(V)` |

---

## Strict Law-4 `N0` Prior-Art Quarantine

All classical and modern physics/mathematics roots are explicitly credited in [DOUBLE_SLIT_PRIOR_ART.md](docs/DOUBLE_SLIT_PRIOR_ART.md) and [QUANTUM_UNIFICATION_REPORT.md](docs/QUANTUM_UNIFICATION_REPORT.md) and are **never** claimed as new:
- **`R5-N0-01` (Complementarity & Eraser):** Bohr–Einstein (1927), Wootters–Zurek (1979), Scully–Englert–Walther (1991), Jaeger–Shimony–Vaidman (1995), Englert (1996).
- **`R5-N0-02` (Sorkin Hierarchy & Multi-Slit Loops):** Sorkin (1994), Sinha et al. (2010), Sawant et al. (2014), Magaña-Loaiza et al. (2016).
- **`R5-N0-03` (Open Quantum Systems & Modular Theory):** Tomita–Takesaki (1970/1972), Gorini–Kossakowski–Sudarshan–Lindblad (1976), Misra–Sudarshan (1977), Facchi–Pascazio (2002).
- **`R5-N0-04` (Schur, Effective Resistance & Magnetic Graphs):** Huygens–Steiner (1673/1840), Kirchhoff (1847), Sylvester (1852), Schur (1917), Foster (1948), Kato (1966), Haynsworth (1968), Fenichel (1979), Bilu–Linial (2006), Kenyon (2011).

---

## Honest Scope & 3 Mathematical Gaps to Continuum Quantum Field Theory

1. **Finite-Dimensional Algebraic Scope:** All Hilbert spaces, GKSL superoperators, and weighted graphs are finite-dimensional over $\mathbb{Q}$ and $\mathbb{Q}[i]$; continuum QFT requires Type III$_1$ von Neumann algebra renormalization and Haag–Kastler local nets.
2. **Exact Near-Field Geometry vs. Discrete Slit Matrix:** The $M$-slit looped-Schur order law $I_M^{\mathrm{loop}}(g) = O(g^{M-2})$ is exact for finite slit-to-slit coupling operators $M_S(g) = (D_0 - g K_{\mathrm{near}})_{S,S}$; computing physical coupling constants $g$ for metallic/plasmonic apertures requires solving 3D vector Maxwell boundary-value problems.
3. **Abelian $U(1)$ Flat Holonomy vs. Non-Abelian Gauge Fields:** The complex $U(1)$ surgical severing and two-phase Green's-function tomography identities hold universally for Abelian $U(1)$ magnetic Laplacians on any finite connected weighted graph; non-Abelian gauge fields ($SU(N)$) introduce non-commuting path-ordered holonomies.

---

## License

[MIT](LICENSE)
