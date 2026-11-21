# Round 3B — Arm H1: Exact Horizon Schur–Haynsworth Inertia, Pure-$\mathbb{Q}$ Page Turnaround & Four-Regime Modular-Schur Obstructions (`AUDIT-041`)

- **Owner:** `gravity-probe` (Arm H1, `#243` + `HAWKING_PORTALS_AND_PRIOR_ART.md`)
- **Workspace:** `symbiosis/round3/hawking-bridge/horizon_schur_modular/`
- **Executable Artifact:** `probe_h1_horizon_schur_modular.py` (`SHA-256: fc5bb6d6...`) $\to$ `probe_h1_horizon_schur_modular_results.json` (`SHA-256: a0ec4426...`) — **`AUDIT-041` `VERIFIED` (`#258`, `check_034_audit041_horizon_schur_modular.py`: full symbolic SymPy proofs + `4/4` isolated `-I` R4 bit-identical + `aletheia audit-check PASS`)**
- **Oracle Class & Honest Novelty Claim:** `exact` (**100% pure `fractions.Fraction` & $\mathbb{Q}[i]$, ZERO floats anywhere**) | **`N1`** (exact zero-float discrete synthesis, closed-form coordinate-free modular-Schur & pointer-commutator laws, and Krein/Haynsworth null-coupling obstructions — explicitly NOT claiming to solve continuum quantum gravity or the black-hole information paradox).

---

## 1. Strict Law-4 `N0` Prior-Art Quarantine

Every known pillar of mathematical physics referenced below is explicitly quarantined as **`N0`** prior art:
- **Sylvester (1852), Haynsworth (1968), Albert (1969), Benzi–Golub–Liesen (2005):** Congruence inertia, generalized Schur complement additivity, PSD range conditions, and saddle-point matrix inertia.
- **Hawking (1974, 1976), Lubkin (1978), Page (1993), Engelhardt–Wall (2015):** Thermal radiation, Haar purity average, Page min-plus entanglement turnaround, and QES islands.
- **Takesaki (1972), Araki (1976), Petz (1986), Connes–Rovelli (1994), GKSL (1976):** Conditional expectation criterion $\Delta_\rho(\mathcal{A}_A) \subseteq \mathcal{A}_A$, relative-entropy monotonicity, Thermal Time Hypothesis, and Lindblad generators.
- **Hawking–Perry–Strominger (2016):** BMS soft-hair motivation; in this discrete finite-dimensional model, $\ker(G_{BB})$ is strictly an **algebraic soft-hair analogue / singular boundary kernel**, never continuum gravitational BMS soft hair.

---

## 2. Verified Exact Zero-Float Results (Pure $\mathbb{Q}$ and $\mathbb{Q}[i]$)

### Part 1 (Target H1-A1) — Tripartite Singular-Horizon Haynsworth–Schur & Krein Null-Coupling Obstruction
On a screened tripartite space $V_I(2) \oplus V_B(3) \oplus V_E(2)$ ($G_{IE} \equiv 0$, singular horizon block $\dim \ker(G_{BB}) = k_{\mathrm{soft}} = 2$):
1. **Euclidean PSD Screening ($G \succeq 0$, exact Bunch–Kaufman inertia `(5, 2, 0)`):** Iterated fiber elimination (`I` then singular `B` via exact Moore–Penrose $G_{BB}^+$ verified against all 4 MP axioms over $\mathbb{Q}$) matches direct block elimination with `0` residual; singular Haynsworth additivity `(3, 2, 0) + (2, 0, 0) = (5, 2, 0)` holds identically; a horizon-anchored soft-charge readout preserves exact rank `2 = k_soft` invisible to bulk exterior Schur $S_{E|IB}$; all invariants and $S_E$ congruence covariance hold with **`0` residual** under $GL(2,\mathbb{Q}) \times GL(3,\mathbb{Q}) \times GL(2,\mathbb{Q})$.
2. **Lorentzian / Krein Horizon Null-Coupling Obstruction:** Turning on linear coupling of rank $r_{\mathrm{cross}} \in \{1, 2\}$ between $\ker(G_{BB})$ and $V_E$ shifts exact inertia to `(5, 2 - r_cross, r_cross)` (exact $n_-(G) = r_{\mathrm{cross}}$, invariant under $GL(V_I)\times GL(V_B)\times GL(V_E)$), while null-to-null coupling yields exact hyperbolic inertia `(2, 0, 2)` — proving over $\mathbb{Q}$ why Euclidean PSD quadratic forms forbid linear zero-mode coupling (`r_cross = 0`) whereas indefinite/Lorentzian signatures permit it at the exact algebraic cost of one negative inertia index per coupled soft mode.

### Part 2 (Target H1-A2) — Pure-$\mathbb{Q}$ Unitary Evaporation Page Turnaround (`N = 6` Qubits, `64`-Dim Exact $O(64,\mathbb{Q})$ Scrambler)
- Applying 3 exact rational Householder reflections (`||psi||^2 == 1` identically over $\mathbb{Q}$, zero floats) across all bipartitions $t = 0..6$ ($d_E = 2^t$, $d_I = 2^{6-t}$):
  - **Exact Schmidt Moment Conservation:** $\operatorname{tr}(\rho_E(t)^m) \equiv \operatorname{tr}(\rho_I(t)^m)$ for $m = 1, 2, 3, 4$ at every $t = 0..6$.
  - **Exact Zero-Log `R_opt` (`AUDIT-002`) & Fourth-Moment `R_{H4}` (`AUDIT-014`) Turnaround:** $R_{\mathrm{opt}}(\rho_E(t)) = 1/\operatorname{tr}(\rho_E^2)$ rises strictly for $t = 0 \to 3$, peaks strictly below the min-plus tropical saddle $\min(2^t, 2^{6-t}) = 8$, falls strictly for $t = 3 \to 6$, certifies exact integer rank lower bounds $\lceil R_{\mathrm{opt}} \rceil \le \operatorname{rank}(\rho_E)$ without computing a single eigenvalue, and is **`0`-residual invariant** under local $O(8, \mathbb{Q})$ gauge rotation at $t = 3$.
  - **Hawking-1976 Thermal Negative Control:** Mixed thermal emission $R_{\mathrm{opt}} = 2^t$ strictly violates the interior wall $2^{6-t}$ at $t = 4, 5, 6$ (`16 > 4, 32 > 2, 64 > 1`).

### Part 3 (Target H1-B) — Four-Regime Exact Modular-Schur & GKSL Commutation Obstructions over $\mathbb{Q}$ and $\mathbb{Q}[i]$
For a faithful bipartite state $\omega_{AB} \in M_4(\mathbb{Q})$, block-partitioning the exact $16 \times 16$ modular operator $\Delta_{\omega_{AB}}(X) = \omega_{AB} X \omega_{AB}^{-1}$ along $\mathcal{A}_A \oplus \mathcal{A}_A^\perp$ defines the **Modular Schur Reduction** $S_{\mathrm{mod}}(\omega_{AB}) := D_{AA} - D_{A\perp} D_{\perp\perp}^{-1} D_{\perp A} \equiv ([\Delta_{\omega_{AB}}^{-1}]_{AA})^{-1}$ (verified identically over $\mathbb{Q}$), yielding four strictly separated, coordinate-free regimes:

| Regime | $\mathcal{O}_{\mathrm{clock}} = \|D_{\perp A}\|_F^2$ | $\mathcal{G}_{\mathrm{Schur}} = \|D_{AA} - S_{\mathrm{mod}}\|_F^2$ | $\min_{U_A \in O(2,\mathbb{Q})} \|[\mathcal{D}[U_A Z_A U_A^\top \otimes I_B], \Delta_\omega]\|_F^2$ | $\mathcal{C}_{\mathrm{Schur}} = \|[S_{\mathrm{mod}}, \Delta_{\omega_A}]\|_F^2$ |
|---|---|---|---|---|
| **1. Product ($\omega_A \otimes \omega_B$)** | `0` | `0` | `0` | `0` |
| **2. Classical Correlated ($p_{ab} \neq p_a q_b$)** | `225/32` | `50625/9248` (exact Plücker $(p_{00}p_{11}-p_{01}p_{10})^2$ gap!) | `0` at pointer $Z_A$ (`> 0` at $X_A$) | `0` |
| **3. Isotropic Entangled Werner ($\rho_W(q)$, $q \in (0,1)$)** | $\frac{24 q^2(1+2q+3q^2)}{(1-q)^2(1+3q)^2}$ | Exact reciprocal $D_{AA}\big|_{\mathfrak{su}(2)} = \lambda(q)$, $S_{\mathrm{mod}}\big|_{\mathfrak{su}(2)} = \lambda(q)^{-1}$, $\lambda(q)=\frac{(1+q)^2}{(1-q)(1+3q)}$ | **Constant $\forall U_A \in O(2,\mathbb{Q})$:** $\frac{256 q^2(1+2q+3q^2)}{(1-q)^2(1+3q)^2} \equiv \frac{32}{3}\,\mathcal{O}_{\mathrm{clock}}$ | `0` ($\rho_A = I_2/2$) |
| **4. Generic Multi-Branch Entangled** | `> 0` | `> 0` | `> 0` | **`> 0` (exact non-commuting modular holonomy, `0`-residual $O(2,\mathbb{Q})\times O(2,\mathbb{Q})$ invariant!)** |

- **Exact Closed-Form Werner Horizon Freezing ($q \to 1^-$):** On $\mathfrak{su}(2)$ exterior observables, $S_{\mathrm{mod}}(\rho_W(q)) = \frac{(1-q)(1+3q)}{(1+q)^2}\,\mathrm{Id} \to 0$ (complete Schur freezing at maximal horizon entanglement) while $D_{AA}(\rho_W(q)) = \lambda(q)\,\mathrm{Id} \to \infty$, and NO local exterior pointer basis $U_A Z_A U_A^\top$ commutes with $\Delta_{\rho_W(q)}$ (constant $\frac{32}{3}\,\mathcal{O}_{\mathrm{clock}}$ across all $U_A \in O(2, \mathbb{Q})$).
- **Exact $16 \times 16$ GKSL Lindblad–Zeno Bridge over $\mathbb{Q}[i]$ (`AUDIT-018`):** Strong exterior monitoring $\gamma \mathcal{D}[Z_A \otimes I_B]$ ($\gamma = 25$) against horizon coupling $g(X_A \otimes X_B)$ ($g = 3/2$) Zeno-quenches `ZI` at exact rational Schur rate $2 g^2 / \gamma = 9/50$ while holding the commuting sector `IX` at exact `0` drift.

---

## 3. Reproducibility (4-Mode Isolated R4 Parity)

From `symbiosis/round3/hawking-bridge/horizon_schur_modular/`:

```bash
for f in "-I -B" "-I -O -B" "-I -B -W error" "-I -O -B -W error"; do
  python3 $f probe_h1_horizon_schur_modular.py
done
```
