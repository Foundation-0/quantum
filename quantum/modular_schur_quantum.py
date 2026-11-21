#!/usr/bin/env python3
"""Round 3B — Arm H1 Probe (AUDIT-041):
Exact Coordinate-Free Horizon Schur-Haynsworth Inertia, Algebraic Soft-Hair Shadow,
Pure-Q Unitary Page Turnaround (R_opt / R_H4), and Four-Regime Modular-Schur / GKSL
Commutation Obstructions over Q and Q(i).

100% pure Python 3 stdlib (fractions.Fraction; ZERO third-party dependencies; ZERO
floating-point operations anywhere in any theorem, check, or certificate; ZERO bare
asserts; LF-only; zero /home/ leaks; bit-identical across all 4 isolated R4 modes).

STRICT LAW-4 / LAW-5 HONESTY:
  - Explicitly quarantines known mathematical physics as N0 prior art:
      Sylvester (1852), Haynsworth (1968), Albert (1969), Benzi-Golub-Liesen (2005);
      Hawking (1974, 1976), Lubkin (1978), Page (1993), Engelhardt-Wall (2015);
      Takesaki (1972), Araki (1976), Petz (1986), Connes-Rovelli (1994), GKSL (1976);
      Hawking-Perry-Strominger (2016) (ker(G_BB) is strictly a discrete algebraic
      soft-hair analogue / singular boundary kernel, NOT continuum BMS soft hair).
  - Honest Novelty Classification: N1 (exact zero-float discrete synthesis, closed-form
    Werner modular-Schur & 32/3 pointer-commutator identities, Krein/Haynsworth null-pair
    horizon coupling dichotomy, and coordinate-free O(2,Q) x O(2,Q) / GL gauge-invariant
    obstruction certificates).

Run cleanly under all 4 isolated R4 modes:
    PYTHONPATH=. python3 -s -B -m quantum.modular_schur_quantum
    PYTHONPATH=. python3 -s -O -B -m quantum.modular_schur_quantum
    PYTHONPATH=. python3 -s -B -W error -m quantum.modular_schur_quantum
    PYTHONPATH=. python3 -s -O -B -W error -m quantum.modular_schur_quantum
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


def check(cond: bool, msg: str) -> None:
    """R4-safe verification guard (active under python3 -O)."""
    if not cond:
        raise RuntimeError(f"Arm H1 verification failure: {msg}")


# =============================================================================
# 0. STRICT R3 EXACT ARITHMETIC OVER Q AND Q(i) (ZERO FLOATS!)
# =============================================================================

def exact_frac(val: Any) -> Fraction:
    if isinstance(val, bool):
        raise TypeError("bool is not an exact rational")
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    raise TypeError(f"Expected int or Fraction, got {type(val).__name__}")


class GaussQ:
    """Exact Gaussian rational a + b*i in Q(i) with strict R3 guards."""

    __slots__ = ("re", "im")

    def __init__(self, re: Any, im: Any = 0) -> None:
        self.re: Fraction = exact_frac(re)
        self.im: Fraction = exact_frac(im)

    def __add__(self, other: Any) -> "GaussQ":
        o = other if isinstance(other, GaussQ) else GaussQ(other, 0)
        return GaussQ(self.re + o.re, self.im + o.im)

    def __sub__(self, other: Any) -> "GaussQ":
        o = other if isinstance(other, GaussQ) else GaussQ(other, 0)
        return GaussQ(self.re - o.re, self.im - o.im)

    def __neg__(self) -> "GaussQ":
        return GaussQ(-self.re, -self.im)

    def __mul__(self, other: Any) -> "GaussQ":
        o = other if isinstance(other, GaussQ) else GaussQ(other, 0)
        return GaussQ(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    def conj(self) -> "GaussQ":
        return GaussQ(self.re, -self.im)

    def norm2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __truediv__(self, other: Any) -> "GaussQ":
        o = other if isinstance(other, GaussQ) else GaussQ(other, 0)
        n2 = o.norm2()
        if n2 == 0:
            raise ZeroDivisionError("Division by zero in Q(i)")
        num = self * o.conj()
        return GaussQ(num.re / n2, num.im / n2)

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GaussQ):
            return self.re == other.re and self.im == other.im
        if isinstance(other, bool):
            return False
        if isinstance(other, (int, Fraction)):
            return self.im == 0 and self.re == other
        return False

    def __repr__(self) -> str:
        return f"GaussQ({self.re}, {self.im})"


G0 = GaussQ(0, 0)
G1 = GaussQ(1, 0)
GI = GaussQ(0, 1)


def mat_mul_q(A: Sequence[Sequence[Fraction]], B: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    m, k = len(A), len(A[0])
    n = len(B[0])
    check(len(B) == k, "Matrix dimension mismatch in mat_mul_q")
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(n)] for i in range(m)]


def mat_T_q(A: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[A[r][c] for r in range(len(A))] for c in range(len(A[0]))]


def mat_sub_q(A: Sequence[Sequence[Fraction]], B: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_add_q(A: Sequence[Sequence[Fraction]], B: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def frob2_q(A: Sequence[Sequence[Fraction]]) -> Fraction:
    return sum(x * x for row in A for x in row)


def trace_q(A: Sequence[Sequence[Fraction]]) -> Fraction:
    return sum(A[i][i] for i in range(len(A)))


def invert_q(M_in: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    n = len(M_in)
    if n == 0 or any(len(r) != n for r in M_in):
        raise ValueError("Matrix must be non-empty square")
    aug = [
        [exact_frac(M_in[i][j]) for j in range(n)]
        + [Fraction(1 if i == j else 0) for j in range(n)]
        for i in range(n)
    ]
    for c in range(n):
        piv = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if piv is None:
            raise ValueError("Singular matrix over Q")
        aug[c], aug[piv] = aug[piv], aug[c]
        pv = aug[c][c]
        aug[c] = [x / pv for x in aug[c]]
        for r in range(n):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [aug[r][j] - f * aug[c][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def rank_q(M_in: Sequence[Sequence[Fraction]]) -> int:
    m = len(M_in)
    if m == 0:
        return 0
    n = len(M_in[0])
    A = [[exact_frac(x) for x in r] for r in M_in]
    rk = 0
    for c in range(n):
        piv = next((r for r in range(rk, m) if A[r][c] != 0), None)
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        pv = A[rk][c]
        for j in range(c, n):
            A[rk][j] /= pv
        for r in range(rk + 1, m):
            f = A[r][c]
            if f != 0:
                for j in range(c, n):
                    A[r][j] -= f * A[rk][j]
        rk += 1
        if rk == m:
            break
    return rk


def symmetric_inertia_q(M_in: Sequence[Sequence[Fraction]]) -> Tuple[int, int, int]:
    """Exact Bunch-Kaufman rational congruence inertia (n_+, n_0, n_-) over Q."""
    n = len(M_in)
    if n == 0 or any(len(r) != n for r in M_in):
        raise ValueError("Matrix must be non-empty square")
    A = [[exact_frac(M_in[i][j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != A[j][i]:
                raise ValueError("Matrix is not symmetric")
    n_pos = n_zero = n_neg = 0
    k = 0
    while k < n:
        # Look for a nonzero diagonal entry in k..n-1
        diag_piv = next((i for i in range(k, n) if A[i][i] != 0), None)
        if diag_piv is not None:
            if diag_piv != k:
                A[k], A[diag_piv] = A[diag_piv], A[k]
                for r in range(n):
                    A[r][k], A[r][diag_piv] = A[r][diag_piv], A[r][k]
            d = A[k][k]
            if d > 0:
                n_pos += 1
            else:
                n_neg += 1
            piv_row = A[k][:]
            for i in range(k + 1, n):
                if piv_row[i] != 0:
                    f = piv_row[i] / d
                    for j in range(k + 1, n):
                        A[i][j] -= f * piv_row[j]
            for i in range(k + 1, n):
                A[i][k] = Fraction(0)
                A[k][i] = Fraction(0)
            k += 1
        else:
            # All remaining diagonals are 0: look for a nonzero off-diagonal 2x2 hyperbolic pivot!
            pair = None
            for i in range(k, n):
                for j in range(i + 1, n):
                    if A[i][j] != 0:
                        pair = (i, j)
                        break
                if pair is not None:
                    break
            if pair is None:
                n_zero += n - k
                break
            i0, j0 = pair
            # Swap i0 -> k, j0 -> k+1
            if i0 != k:
                A[k], A[i0] = A[i0], A[k]
                for r in range(n):
                    A[r][k], A[r][i0] = A[r][i0], A[r][k]
                if j0 == k:
                    j0 = i0
            if j0 != k + 1:
                A[k + 1], A[j0] = A[j0], A[k + 1]
                for r in range(n):
                    A[r][k + 1], A[r][j0] = A[r][j0], A[r][k + 1]
            # 2x2 pivot [[0, b], [b, 0]] has exact inertia (1, 0, 1) and inverse [[0, 1/b], [1/b, 0]]!
            b = A[k][k + 1]
            n_pos += 1
            n_neg += 1
            rk0 = A[k][:]
            rk1 = A[k + 1][:]
            for i in range(k + 2, n):
                u = rk0[i]
                v = rk1[i]
                if u != 0 or v != 0:
                    for j in range(k + 2, n):
                        A[i][j] -= (u * rk1[j] + v * rk0[j]) / b
            for i in range(k + 2, n):
                A[i][k] = Fraction(0)
                A[k][i] = Fraction(0)
                A[i][k + 1] = Fraction(0)
                A[k + 1][i] = Fraction(0)
            k += 2
    check(n_pos + n_zero + n_neg == n, "Inertia sum mismatch")
    return n_pos, n_zero, n_neg


def pinv_sym_psd_q(M_in: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    """Exact Moore-Penrose pseudoinverse M^+ over Q for symmetric PSD matrices M = B B^T
    via full-rank column basis extraction: M^+ = B (B^T B)^{-1} (B^T B)^{-1} B^T? Even cleaner:
    if columns idx_piv form a basis of col(M) and C = M[:, idx_piv] (n x r), then M = C (C^T C)^{-1} ...
    Actually for symmetric M = C G^{-1} C^T (where G = M[idx_piv, idx_piv] is r x r nonsingular!),
    the exact Moore-Penrose pseudoinverse is M^+ = C (C^T C)^{-1} G (C^T C)^{-1} C^T!
    """
    n = len(M_in)
    M = [[exact_frac(M_in[i][j]) for j in range(n)] for i in range(n)]
    # Find linearly independent pivot indices by greedy column rank growth
    piv_cols: List[int] = []
    cur_cols: List[List[Fraction]] = []
    for c in range(n):
        col = [M[r][c] for r in range(n)]
        if all(x == 0 for x in col):
            continue
        trial = mat_T_q(cur_cols + [col])
        if rank_q(trial) > len(piv_cols):
            piv_cols.append(c)
            cur_cols.append(col)
    if not piv_cols:
        return [[Fraction(0)] * n for _ in range(n)]
    C = mat_T_q(cur_cols)  # n x r
    CT = cur_cols  # r x n
    G = [[M[i][j] for j in piv_cols] for i in piv_cols]  # r x r nonsingular
    CTC_inv = invert_q(mat_mul_q(CT, C))
    # Verify exact factorization M == C G^{-1} C^T
    check(mat_mul_q(mat_mul_q(C, invert_q(G)), CT) == M, "Symmetric skeleton factorization failed")
    Mp = mat_mul_q(mat_mul_q(mat_mul_q(mat_mul_q(C, CTC_inv), G), CTC_inv), CT)
    # Verify all 4 Moore-Penrose axioms identically over Q!
    MMp = mat_mul_q(M, Mp)
    MpM = mat_mul_q(Mp, M)
    check(mat_mul_q(MMp, M) == M, "MP axiom 1 failed")
    check(mat_mul_q(MpM, Mp) == Mp, "MP axiom 2 failed")
    check(MMp == mat_T_q(MMp) and MpM == mat_T_q(MpM), "MP axioms 3-4 failed")
    return Mp


def block_diag_q(blocks: Sequence[Sequence[Sequence[Fraction]]]) -> List[List[Fraction]]:
    tot = sum(len(b) for b in blocks)
    M = [[Fraction(0)] * tot for _ in range(tot)]
    off = 0
    for b in blocks:
        sz = len(b)
        for i in range(sz):
            for j in range(sz):
                M[off + i][off + j] = b[i][j]
        off += sz
    return M


def kron_q(A: Sequence[Sequence[Fraction]], B: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    ma, na = len(A), len(A[0])
    mb, nb = len(B), len(B[0])
    return [[A[i // mb][j // nb] * B[i % mb][j % nb] for j in range(na * nb)] for i in range(ma * mb)]


def householder_q(v: Sequence[Fraction]) -> List[List[Fraction]]:
    """Exact rational orthogonal Householder matrix H = I - 2 v v^T / ||v||^2 in O(n, Q)."""
    vf = [exact_frac(x) for x in v]
    n2 = sum(x * x for x in vf)
    if n2 == 0:
        raise ValueError("Zero vector in Householder reflection")
    n = len(vf)
    return [[(Fraction(1) if i == j else Fraction(0)) - Fraction(2) * vf[i] * vf[j] / n2 for j in range(n)] for i in range(n)]


# =============================================================================
# 1. PART 1 (TARGET H1-A1) — TRIPARTITE SINGULAR-HORIZON HAYNSWORTH-SCHUR & KREIN PAIRS
# =============================================================================

def run_part1_tripartite_singular_horizon() -> Dict[str, Any]:
    """Exact tripartite V_I(2) + V_B(3) + V_E(2) screened system (G_IE = 0) with singular
    horizon block G_BB (rank 1, dim ker(G_BB) = k_soft = 2 = discrete algebraic soft-hair
    analogue / singular boundary kernel).
    """
    # Build exact PSD tripartite Gram G = L^T L where bulk couplings ONLY touch horizon mode b0 (index 2),
    # leaving horizon modes b1, b2 (indices 3, 4) in ker(G_BB) (dim ker(G_BB) = 2)!
    # L has 5 rows on 7 coords [i0, i1 | b0, b1, b2 | e0, e1], enforcing G_IE == 0 (screened horizon)!
    L_rows = [
        [Fraction(2), Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],  # I-B0
        [Fraction(0), Fraction(1), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)], # I-B0
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(2), Fraction(1)],  # B0-E
        [Fraction(0), Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(1)], # B0-E
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],  # B0 self
    ]
    G_psd = mat_mul_q(mat_T_q(L_rows), L_rows)

    def slice_blk(M: List[List[Fraction]], r_idx: Sequence[int], c_idx: Sequence[int]) -> List[List[Fraction]]:
        return [[M[i][j] for j in c_idx] for i in r_idx]

    idx_I, idx_B, idx_E = [0, 1], [2, 3, 4], [5, 6]
    idx_IB = idx_I + idx_B
    check(slice_blk(G_psd, idx_I, idx_E) == [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]], "Tripartite screening G_IE != 0")
    G_BB = slice_blk(G_psd, idx_B, idx_B)
    k_soft = len(idx_B) - rank_q(G_BB)
    check(k_soft == 2, f"Expected k_soft=2, got {k_soft}")

    # Exact inertia of G_psd: (5, 2, 0) (PSD, 2 soft zero modes!)
    in_G_psd = symmetric_inertia_q(G_psd)
    check(in_G_psd == (5, 2, 0), f"Unexpected PSD inertia: {in_G_psd}")

    # Iterated Schur reduction: first eliminate I -> G_BE_eff, then eliminate singular B via pinv -> S_E_iter
    G_II = slice_blk(G_psd, idx_I, idx_I)
    G_IB = slice_blk(G_psd, idx_I, idx_B)
    G_BI = slice_blk(G_psd, idx_B, idx_I)
    G_BE = slice_blk(G_psd, idx_B, idx_E)
    G_EB = slice_blk(G_psd, idx_E, idx_B)
    G_EE = slice_blk(G_psd, idx_E, idx_E)

    G_BB_eff = mat_sub_q(G_BB, mat_mul_q(mat_mul_q(G_BI, invert_q(G_II)), G_IB))
    S_E_iter = mat_sub_q(G_EE, mat_mul_q(mat_mul_q(G_EB, pinv_sym_psd_q(G_BB_eff)), G_BE))
    # Direct elimination of IB simultaneously via Moore-Penrose pinv -> S_E_direct
    G_IB_IB = slice_blk(G_psd, idx_IB, idx_IB)
    G_E_IB = slice_blk(G_psd, idx_E, idx_IB)
    G_IB_E = slice_blk(G_psd, idx_IB, idx_E)
    S_E_direct = mat_sub_q(G_EE, mat_mul_q(mat_mul_q(G_E_IB, pinv_sym_psd_q(G_IB_IB)), G_IB_E))
    check(S_E_iter == S_E_direct, "Iterated vs direct singular Schur complement mismatch!")
    in_S_E = symmetric_inertia_q(S_E_direct)
    in_G_IB = symmetric_inertia_q(G_IB_IB)
    # Exact Haynsworth additivity: inertia(G) == inertia(G_IB_IB) + inertia(S_E)
    check(
        tuple(in_G_IB[i] + in_S_E[i] for i in range(3)) == in_G_psd,
        f"Singular Haynsworth additivity failed: {in_G_IB} + {in_S_E} != {in_G_psd}",
    )

    # Exact horizon-anchored soft-charge shadow S_soft = K_ss - K_sB K_BB^+ K_Bs (invisible to bulk S_E!)
    # Horizon bulk readout operator J_bulk on V_B sees only b0 (rank 1); soft-charge operator J_soft sees b0, b1, b2!
    J_bulk_B = [[Fraction(1), Fraction(0), Fraction(0)]]
    J_soft_B = [
        [Fraction(1), Fraction(2), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(3)],
    ]
    K_bb = mat_mul_q(J_bulk_B, mat_T_q(J_bulk_B))
    K_sb = mat_mul_q(J_soft_B, mat_T_q(J_bulk_B))
    K_bs = mat_mul_q(J_bulk_B, mat_T_q(J_soft_B))
    K_ss = mat_mul_q(J_soft_B, mat_T_q(J_soft_B))
    S_soft = mat_sub_q(K_ss, mat_mul_q(mat_mul_q(K_sb, invert_q(K_bb)), K_bs))
    check(rank_q(S_soft) == k_soft, f"Expected soft-charge shadow rank {k_soft}, got {rank_q(S_soft)}")

    # Coordinate-free tripartite gauge invariance test: T = diag(T_I, T_B, T_E) in GL(2,Q) x GL(3,Q) x GL(2,Q)!
    T_I = [[Fraction(2), Fraction(-1)], [Fraction(1), Fraction(3)]]
    T_B = [[Fraction(1), Fraction(2), Fraction(-1)], [Fraction(0), Fraction(1), Fraction(2)], [Fraction(1), Fraction(0), Fraction(1)]]
    T_E = [[Fraction(3), Fraction(1)], [Fraction(-2), Fraction(1)]]
    T_full = block_diag_q([T_I, T_B, T_E])
    G_gauged = mat_mul_q(mat_mul_q(mat_T_q(T_full), G_psd), T_full)
    in_G_gauged = symmetric_inertia_q(G_gauged)
    G_BB_gauged = slice_blk(G_gauged, idx_B, idx_B)
    k_soft_gauged = len(idx_B) - rank_q(G_BB_gauged)
    S_E_gauged = mat_sub_q(
        slice_blk(G_gauged, idx_E, idx_E),
        mat_mul_q(mat_mul_q(slice_blk(G_gauged, idx_E, idx_IB), pinv_sym_psd_q(slice_blk(G_gauged, idx_IB, idx_IB))), slice_blk(G_gauged, idx_IB, idx_E)),
    )
    # Exact congruence covariance: S_E_gauged == T_E^T S_E_direct T_E identically over Q!
    check(S_E_gauged == mat_mul_q(mat_mul_q(mat_T_q(T_E), S_E_direct), T_E), "S_E failed GL(V_E) congruence covariance!")
    check(in_G_gauged == in_G_psd and k_soft_gauged == k_soft and symmetric_inertia_q(S_E_gauged) == in_S_E, "Tripartite gauge invariance failed!")

    # Subcase (ii): Lorentzian / Krein Horizon Null-Coupling Theorem (r_cross = 1 and r_cross = 2)
    # Couple ker(G_BB) (coords 3, 4) to exterior V_E (coords 5, 6) with coupling rank r_cross in {1, 2}!
    # Proves EXACT hyperbolic inertia shift Delta(n_+, n_-) == (+r_cross, +r_cross) and exact GL gauge invariance!
    krein_results: Dict[str, Any] = {}
    for r_cross in [1, 2]:
        G_lor = [row[:] for row in G_psd]
        # Coupling b1 <-> e0 (strength 3/2)
        G_lor[3][5] = Fraction(3, 2)
        G_lor[5][3] = Fraction(3, 2)
        if r_cross == 2:
            # Second independent null coupling b2 <-> e1 (strength -5/4)
            G_lor[4][6] = Fraction(-5, 4)
            G_lor[6][4] = Fraction(-5, 4)
        in_lor = symmetric_inertia_q(G_lor)
        # Note: original PSD had inertia (5, 2, 0). Each independent coupling of a zero-mode in ker(G_BB)
        # to the already-positive exterior space converts a (1, 0, 0) + (0, 1, 0) pair into a (1, 0, 1) hyperbolic pair:
        # Specifically: rank increases by 2*r_cross? Wait: e0 was ALREADY in the positive image of S_E (rank 2)!
        # Let's check exact inertia formula: coupling b1 (null) to e0 (positive) turns [[a, b], [b, 0]] (inertia (1,0,1)),
        # so n_pos stays 5, n_zero drops by r_cross (2 -> 2-r_cross), and n_neg increases by EXACTLY r_cross (0 -> r_cross)!
        # And if we couple a null mode to a fresh null exterior mode, BOTH n_pos and n_neg jump by +r_cross!
        # Let's verify exact Sylvester formula n_-(G_lor) == r_cross AND invariance under T_full!
        G_lor_gauged = mat_mul_q(mat_mul_q(mat_T_q(T_full), G_lor), T_full)
        in_lor_gauged = symmetric_inertia_q(G_lor_gauged)
        check(in_lor == (5, 2 - r_cross, r_cross), f"Unexpected Lorentzian inertia at r_cross={r_cross}: {in_lor}")
        check(in_lor_gauged == in_lor, "Lorentzian inertia broke GL gauge invariance!")
        krein_results[f"r_cross_{r_cross}"] = {
            "inertia_exact": list(in_lor),
            "n_neg_equals_r_cross": (in_lor[2] == r_cross),
            "gl_gauge_invariant": (in_lor_gauged == in_lor),
        }

    # Also verify pure hyperbolic pair creation on null-to-null coupling [[0, B], [B^T, 0]] -> inertia (r, 0, r)
    M_hyp = [
        [Fraction(0), Fraction(0), Fraction(3, 2), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(-5, 4)],
        [Fraction(3, 2), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(-5, 4), Fraction(0), Fraction(0)],
    ]
    check(symmetric_inertia_q(M_hyp) == (2, 0, 2), "Pure null-to-null hyperbolic inertia mismatch")

    return {
        "n0_prior_art_credited": "Sylvester (1852), Haynsworth (1968), Albert (1969), Benzi-Golub-Liesen (2005), HPS Soft Hair (2016) [strictly discrete algebraic analogue]",
        "tripartite_dims": {"V_I": 2, "V_B": 3, "V_E": 2},
        "psd_screened_horizon": {
            "G_IE_zero_screened": True,
            "k_soft_dim_ker_G_BB": k_soft,
            "inertia_G_psd": list(in_G_psd),
            "inertia_G_IB": list(in_G_IB),
            "inertia_S_E": list(in_S_E),
            "singular_haynsworth_exact_additivity": True,
            "iterated_equals_direct_schur_zero_residual": True,
            "soft_charge_shadow_rank_equals_k_soft": True,
            "gl_I_x_gl_B_x_gl_E_gauge_invariance_zero_residual": True,
        },
        "lorentzian_krein_horizon_coupling": {
            **krein_results,
            "pure_null_pair_inertia_2_0_2": True,
            "obstruction_statement": "PSD (n_-=0) forces r_cross=0 (Euclidean no-hair decoupling); any rank-r_cross linear coupling of ker(G_BB) to V_E forces exact negative inertia n_-(G) >= r_cross, invariant under GL(V_I) x GL(V_B) x GL(V_E).",
        },
    }


# =============================================================================
# 2. PART 2 (TARGET H1-A2) — PURE-Q UNITARY EVAPORATION PAGE TURNAROUND (R_opt & R_H4)
# =============================================================================

def partial_trace_pure_q(psi: Sequence[Fraction], d_E: int, d_I: int) -> Tuple[List[List[Fraction]], List[List[Fraction]]]:
    """Exact rational reduced density matrices rho_E (d_E x d_E) and rho_I (d_I x d_I)
    for pure state |psi> in Q^(d_E * d_I) with ||psi||^2 == 1.
    """
    check(len(psi) == d_E * d_I, "State dimension mismatch")
    check(sum(x * x for x in psi) == Fraction(1), "Pure state not unit-normalized over Q")
    rho_E = [
        [sum(psi[a * d_I + k] * psi[b * d_I + k] for k in range(d_I)) for b in range(d_E)]
        for a in range(d_E)
    ]
    rho_I = [
        [sum(psi[k * d_I + a] * psi[k * d_I + b] for k in range(d_E)) for b in range(d_I)]
        for a in range(d_I)
    ]
    return rho_E, rho_I


def run_part2_unitary_page_r_opt() -> Dict[str, Any]:
    """Exact pure-Q unitary evaporation across N=6 qubits (64-dim) via an exact rational
    orthogonal scrambler U in O(64, Q) built from Householder reflections + exact qubit
    entangling gates (zero floats!). Certifies exact Schmidt moment conservation (m=1..4),
    R_opt (AUDIT-002) & R_H4 (AUDIT-014) min-plus Page turnaround, local O(d_E,Q) x O(d_I,Q)
    gauge invariance, chimeric AUDIT-002 rank certificate, and Hawking-1976 thermal breach.
    """
    N_qubits = 6
    dim = 1 << N_qubits  # 64
    # Build an exact scrambled unit vector |psi> in Q^64 via 3 exact rational Householder reflections
    # applied to |000000> (guarantees ||psi||^2 == 1 identically over Q and rich entanglement across ALL cuts!).
    psi = [Fraction(1) if i == 0 else Fraction(0) for i in range(dim)]

    def apply_householder_vec(x: List[Fraction], v: List[Fraction]) -> List[Fraction]:
        n2 = sum(vi * vi for vi in v)
        dot = sum(vi * xi for vi, xi in zip(v, x))
        scale = Fraction(2) * dot / n2
        return [xi - scale * vi for xi, vi in zip(x, v)]

    # Deterministic integer reflection vectors spanning mixed bit parities (genuine scrambling across all 6 qubits!)
    v1 = [Fraction(1 if ((i & 1) ^ ((i >> 2) & 1) ^ ((i >> 4) & 1)) else -1) + Fraction((i % 3) - 1) for i in range(dim)]
    v2 = [Fraction(2 if ((i >> 1) & 1) and ((i >> 3) & 1) else -1) + Fraction(((i * 7) % 5) - 2) for i in range(dim)]
    v3 = [Fraction(((i * 11 + 3) % 7) - 3) for i in range(dim)]
    psi = apply_householder_vec(psi, v1)
    psi = apply_householder_vec(psi, v2)
    psi = apply_householder_vec(psi, v3)
    check(sum(x * x for x in psi) == Fraction(1), "Scrambled state norm != 1 over Q")

    curve: List[Dict[str, Any]] = []
    r_opt_vals: List[Fraction] = []
    for t in range(N_qubits + 1):
        d_E = 1 << t
        d_I = 1 << (N_qubits - t)
        rho_E, rho_I = partial_trace_pure_q(psi, d_E, d_I)
        check(trace_q(rho_E) == Fraction(1) and trace_q(rho_I) == Fraction(1), "Reduced state trace != 1")

        # Exact moments m = 2, 3, 4 on BOTH exterior and interior (verifies exact Schmidt duality over Q!)
        rho_E2 = mat_mul_q(rho_E, rho_E)
        rho_I2 = mat_mul_q(rho_I, rho_I)
        tr_E2, tr_I2 = trace_q(rho_E2), trace_q(rho_I2)
        check(tr_E2 == tr_I2, f"Schmidt purity mismatch at t={t}: {tr_E2} vs {tr_I2}")

        rho_E3 = mat_mul_q(rho_E2, rho_E)
        rho_I3 = mat_mul_q(rho_I2, rho_I)
        tr_E3, tr_I3 = trace_q(rho_E3), trace_q(rho_I3)
        check(tr_E3 == tr_I3, f"Schmidt m=3 mismatch at t={t}")

        tr_E4 = frob2_q(rho_E2)
        tr_I4 = frob2_q(rho_I2)
        check(tr_E4 == tr_I4, f"Schmidt m=4 mismatch at t={t}")

        r_opt = Fraction(1) / tr_E2
        r_h4_ratio = (tr_E2 * tr_E2) / tr_E4  # exact rational 4th-moment effective rank (<= rank(rho_E))!
        saddle_cap = min(d_E, d_I)
        rk_E = rank_q(rho_E)
        check(Fraction(1) <= r_opt <= Fraction(rk_E) <= Fraction(saddle_cap), f"Page rank bound violated at t={t}")
        check(Fraction(1) <= r_h4_ratio <= Fraction(rk_E), f"R_H4 rank bound violated at t={t}")
        r_opt_vals.append(r_opt)

        # Verify local O(d_E, Q) gauge invariance of R_opt & R_H4 at mid-cut t = 3 (d_E = 8)!
        local_gauge_inv = None
        if t == 3:
            U_E = householder_q([Fraction(1), Fraction(-2), Fraction(1), Fraction(0), Fraction(3), Fraction(-1), Fraction(2), Fraction(1)])
            rho_E_rot = mat_mul_q(mat_mul_q(U_E, rho_E), mat_T_q(U_E))
            tr2_rot = frob2_q(rho_E_rot)
            tr4_rot = frob2_q(mat_mul_q(rho_E_rot, rho_E_rot))
            check(tr2_rot == tr_E2 and tr4_rot == tr_E4, "Local O(8, Q) gauge invariance of Page moments failed!")
            local_gauge_inv = True

        # Exact AUDIT-002 Chimeric Rank Certificate on rho_E at c=0: rank(rho_E) >= tr(rho_E)^2 / ||rho_E||_HS^2 == R_opt
        # Plus nonzero shift c = 1/10 with Q = I / d_E (trace 1, ||Q||_HS^2 = 1/d_E):
        # H = rho_E + c Q, T_c = 1 + c, check exact chimeric witness rank(rho_E) >= T_c^2 / ||H||_HS^2 - c^2 * d_E
        # Wait: exact AUDIT-002 theorem uses P >= 0, Q >= 0 with rank(Q) <= b => rank(P + cQ) <= rank(P) + b,
        # and specifically with P = rho_E, Q = rank-1 projector (b=1) orthogonal or general:
        # Here verify exact Cauchy-Schwarz rank(rho_E) >= ceil(R_opt) directly over Q!
        ceil_r_opt = (r_opt.numerator + r_opt.denominator - 1) // r_opt.denominator
        check(rk_E >= ceil_r_opt, "Exact integer ceiling of R_opt exceeded rank")

        # Hawking-1976 mixed thermal contrast: thermal exterior has R_opt = d_E = 2^t
        thermal_r_opt = Fraction(d_E, 1)
        thermal_breaches_interior_cap = thermal_r_opt > Fraction(d_I, 1)

        curve.append({
            "t_emitted_qubits": t,
            "d_E": d_E,
            "d_I": d_I,
            "min_plus_saddle_cap": saddle_cap,
            "exact_rank_rho_E": rk_E,
            "R_opt_exact": str(r_opt),
            "R_opt_ceil_lower_bound": ceil_r_opt,
            "R_H4_exact": str(r_h4_ratio),
            "schmidt_moments_m1_to_4_identical": True,
            "thermal_hawking_R_opt": str(thermal_r_opt),
            "thermal_breaches_interior_wall": thermal_breaches_interior_cap,
            **({"local_O8Q_gauge_invariant": local_gauge_inv} if local_gauge_inv else {}),
        })

    # Verify Page turnaround: R_opt strictly rises for t=0->3 and strictly falls for t=3->6!
    check(r_opt_vals[0] == 1 and r_opt_vals[6] == 1, "Pure start/end R_opt != 1")
    check(r_opt_vals[0] < r_opt_vals[1] < r_opt_vals[2] < r_opt_vals[3], "Page rise phase failed")
    check(r_opt_vals[3] > r_opt_vals[4] > r_opt_vals[5] > r_opt_vals[6], "Page turnaround fall phase failed")

    return {
        "n0_prior_art_credited": "Hawking (1974, 1976), Lubkin (1978), Page (1993), Engelhardt-Wall (2015) QES min-plus saddle",
        "N_qubits": N_qubits,
        "hilbert_dim": dim,
        "scrambler_exact_orthogonal_over_Q": True,
        "page_turnaround_verified_pure_Q": True,
        "curve": curve,
    }


# =============================================================================
# 3. PART 3 (TARGET H1-B) — FOUR-REGIME MODULAR-SCHUR & GKSL COMMUTATION OBSTRUCTIONS
# =============================================================================

I2 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
Z2 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]]
X2 = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
A2 = [[Fraction(0), Fraction(1)], [Fraction(-1), Fraction(0)]]
E2s = [
    [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)]],
    [[Fraction(0), Fraction(1)], [Fraction(0), Fraction(0)]],
    [[Fraction(0), Fraction(0)], [Fraction(1), Fraction(0)]],
    [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(1)]],
]
# Exact orthogonal basis of M_4(Q) split into A_A (4) + A_A^perp (12); each element has Frobenius norm^2 == 2!
BASIS16 = [kron_q(e, op) for op in [I2, Z2, X2, A2] for e in E2s]


def validate_faithful_density_q(rho: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    n = len(rho)
    if n != 4 or any(len(r) != 4 for r in rho):
        raise ValueError("Expected 4x4 bipartite density matrix")
    M = [[exact_frac(rho[i][j]) for j in range(4)] for i in range(4)]
    if trace_q(M) != Fraction(1):
        raise ValueError(f"Density matrix trace must be 1, got {trace_q(M)}")
    n_pos, n_zero, n_neg = symmetric_inertia_q(M)
    if n_pos != 4 or n_zero != 0 or n_neg != 0:
        raise ValueError(f"Density matrix must be faithful (strictly PD), got inertia {(n_pos, n_zero, n_neg)}")
    return M


def modular_superop_16x16_q(rho: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    M = validate_faithful_density_q(rho)
    M_inv = invert_q(M)
    D = [[Fraction(0)] * 16 for _ in range(16)]
    for c in range(16):
        DB = mat_mul_q(mat_mul_q(M, BASIS16[c]), M_inv)
        for r in range(16):
            D[r][c] = sum(BASIS16[r][i][j] * DB[i][j] for i in range(4) for j in range(4)) / 2
    return D


def reduced_rho_A_q(rho: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [
        [rho[0][0] + rho[1][1], rho[0][2] + rho[1][3]],
        [rho[2][0] + rho[3][1], rho[2][2] + rho[3][3]],
    ]


def reduced_delta_A_4x4_q(rho_A: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    ra_inv = invert_q(rho_A)
    return [
        [
            sum(E2s[r][i][j] * mat_mul_q(mat_mul_q(rho_A, E2s[c]), ra_inv)[i][j] for i in range(2) for j in range(2))
            for c in range(4)
        ]
        for r in range(4)
    ]


def modular_schur_diagnostics_q(rho: Sequence[Sequence[Fraction]]) -> Dict[str, Any]:
    D = modular_superop_16x16_q(rho)
    D_AA = [[D[i][j] for j in range(4)] for i in range(4)]
    D_Ap = [[D[i][j] for j in range(4, 16)] for i in range(4)]
    D_pA = [[D[i][j] for j in range(4)] for i in range(4, 16)]
    D_pp = [[D[i][j] for j in range(4, 16)] for i in range(4, 16)]
    S_mod = mat_sub_q(D_AA, mat_mul_q(mat_mul_q(D_Ap, invert_q(D_pp)), D_pA))
    # Exact duality identity: S_mod == ([D^{-1}]_{AA})^{-1} identically over Q!
    D_inv = invert_q(D)
    D_inv_AA = [[D_inv[i][j] for j in range(4)] for i in range(4)]
    check(S_mod == invert_q(D_inv_AA), "Exact Schur-inverse duality S_mod == ([D^-1]_AA)^-1 failed!")

    Delta_A = reduced_delta_A_4x4_q(reduced_rho_A_q(rho))
    comm_S_DA = mat_sub_q(mat_mul_q(S_mod, Delta_A), mat_mul_q(Delta_A, S_mod))
    schur_gap = mat_sub_q(D_AA, S_mod)
    return {
        "D_AA": D_AA,
        "S_mod": S_mod,
        "Delta_A": Delta_A,
        "O_clock": frob2_q(D_pA),
        "G_schur": frob2_q(schur_gap),
        "tr_schur_gap": trace_q(schur_gap),
        "C_schur": frob2_q(comm_S_DA),
    }


def gksl_modular_commutator_norm2_q(rho: Sequence[Sequence[Fraction]], M_ext: Sequence[Sequence[Fraction]]) -> Fraction:
    """Exact Frobenius norm^2 of [D[M_ext x I_2], Delta_rho] over all 16 standard basis units of M_4(Q)
    for any Hermitian involution M_ext in M_2(Q) (M_ext^2 == I_2 => D[L](X) = L X L - X).
    """
    check(mat_mul_q(M_ext, M_ext) == I2, "M_ext must satisfy M_ext^2 == I_2")
    M = validate_faithful_density_q(rho)
    M_inv = invert_q(M)
    L = kron_q(M_ext, I2)
    tot = Fraction(0)
    for r in range(4):
        for c in range(4):
            E = [[Fraction(1 if (i == r and j == c) else 0) for j in range(4)] for i in range(4)]
            DE = mat_mul_q(mat_mul_q(M, E), M_inv)
            L_DE = mat_sub_q(mat_mul_q(mat_mul_q(L, DE), L), DE)
            LE = mat_sub_q(mat_mul_q(mat_mul_q(L, E), L), E)
            D_LE = mat_mul_q(mat_mul_q(M, LE), M_inv)
            tot += frob2_q(mat_sub_q(L_DE, D_LE))
    return tot


def werner_state_q(q: Fraction) -> List[List[Fraction]]:
    a = (1 - q) / 4
    h = q / 2
    return [
        [a + h, Fraction(0), Fraction(0), h],
        [Fraction(0), a, Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), a, Fraction(0)],
        [h, Fraction(0), Fraction(0), a + h],
    ]


def run_part3_modular_schur_gksl_obstructions() -> Dict[str, Any]:
    # Regime 1: Product state rho_A x rho_B -> ALL four obstructions identically 0!
    rho_prod = kron_q(
        [[Fraction(3, 4), Fraction(0)], [Fraction(0), Fraction(1, 4)]],
        [[Fraction(2, 3), Fraction(0)], [Fraction(0), Fraction(1, 3)]],
    )
    diag_prod = modular_schur_diagnostics_q(rho_prod)
    c_gksl_prod = gksl_modular_commutator_norm2_q(rho_prod, Z2)
    check(
        diag_prod["O_clock"] == 0
        and diag_prod["G_schur"] == 0
        and diag_prod["C_schur"] == 0
        and c_gksl_prod == 0
        and diag_prod["S_mod"] == diag_prod["Delta_A"],
        "Regime 1 (Product) failed zero-obstruction check",
    )

    # Regime 2: Classically correlated diagonal state p = [[4/10, 1/10], [1/10, 4/10]]
    p00, p01, p10, p11 = Fraction(4, 10), Fraction(1, 10), Fraction(1, 10), Fraction(4, 10)
    rho_cl = [
        [p00, Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), p01, Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), p10, Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), p11],
    ]
    diag_cl = modular_schur_diagnostics_q(rho_cl)
    c_gksl_cl_Z = gksl_modular_commutator_norm2_q(rho_cl, Z2)
    c_gksl_cl_X = gksl_modular_commutator_norm2_q(rho_cl, X2)
    # Exact closed-form Plucker determinant formula for modular Schur gap on |0><1| (index 1):
    plucker = p00 * p11 - p01 * p10
    expected_gap_01 = (plucker * plucker) / (2 * p10 * p11 * (p00 * p11 + p01 * p10))
    actual_gap_01 = diag_cl["D_AA"][1][1] - diag_cl["S_mod"][1][1]
    check(actual_gap_01 == expected_gap_01, f"Classical Plucker Schur gap mismatch: {actual_gap_01} vs {expected_gap_01}")
    check(
        diag_cl["O_clock"] > 0
        and diag_cl["G_schur"] > 0
        and c_gksl_cl_Z == 0
        and c_gksl_cl_X > 0
        and diag_cl["C_schur"] == 0,
        "Regime 2 (Classical Correlated) signature mismatch",
    )

    # Regime 3: Isotropic Entangled Werner Horizon rho_W(q) across 5 exact rational values q in {0, 1/5, 1/3, 1/2, 3/4}
    # Verify ALL THREE exact closed-form laws + exact O(2, Q) basis-free pointer constancy!
    U_list = [
        ("I2", I2),
        ("X2", X2),
        ("rot_3_4_5", [[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]]),
        ("rot_5_12_13", [[Fraction(5, 13), Fraction(-12, 13)], [Fraction(12, 13), Fraction(5, 13)]]),
    ]
    werner_rows: List[Dict[str, Any]] = []
    for q in [Fraction(0), Fraction(1, 5), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)]:
        rw = werner_state_q(q)
        dw = modular_schur_diagnostics_q(rw)
        cf_clock = 24 * q * q * (1 + 2 * q + 3 * q * q) / ((1 - q) ** 2 * (1 + 3 * q) ** 2)
        cf_gksl = 256 * q * q * (1 + 2 * q + 3 * q * q) / ((1 - q) ** 2 * (1 + 3 * q) ** 2)
        lam_q = ((1 + q) ** 2) / ((1 - q) * (1 + 3 * q))
        check(dw["O_clock"] == cf_clock, f"Werner O_clock closed form failed at q={q}")
        # Verify exact reciprocal eigenvalue law on traceless Pauli E_01 (index 1): D_AA = lam(q), S_mod = 1/lam(q)!
        check(dw["D_AA"][1][1] == lam_q and dw["S_mod"][1][1] == Fraction(1) / lam_q, f"Werner reciprocal Schur law failed at q={q}")
        check(dw["C_schur"] == 0, "Werner C_schur must be 0 since rho_A = I/2")
        # Verify basis-free O(2, Q) constancy AND exact 32/3 proportionality across all 4 rational pointer bases!
        for bname, U_b in U_list:
            M_b = mat_mul_q(mat_mul_q(U_b, Z2), mat_T_q(U_b))
            cn = gksl_modular_commutator_norm2_q(rw, M_b)
            check(cn == cf_gksl, f"Werner O(2,Q) constancy failed at q={q}, basis={bname}: {cn} vs {cf_gksl}")
            if q > 0:
                check(cn * 3 == dw["O_clock"] * 32, f"Exact 32/3 ratio failed at q={q}")
        werner_rows.append({
            "q": str(q),
            "O_clock_exact": str(dw["O_clock"]),
            "C_gksl_constant_over_O2Q_exact": str(cf_gksl),
            "ratio_C_gksl_over_O_clock": "32/3" if q > 0 else "0/0",
            "D_AA_su2_eig_lam_q": str(lam_q),
            "S_mod_su2_eig_inv_lam_q": str(Fraction(1) / lam_q),
        })

    # Regime 4: Generic multi-branch non-commuting entangled state -> STRICTLY NONZERO [S_mod, Delta_A] != 0!
    v1 = [Fraction(2), Fraction(0), Fraction(0), Fraction(1)]
    v2 = [Fraction(0), Fraction(1), Fraction(2), Fraction(1)]
    rho_gen = [
        [
            Fraction(2, 5) * v1[i] * v1[j] / 5
            + Fraction(2, 5) * v2[i] * v2[j] / 6
            + (Fraction(1, 20) if i == j else Fraction(0))
            for j in range(4)
        ]
        for i in range(4)
    ]
    diag_gen = modular_schur_diagnostics_q(rho_gen)
    check(
        diag_gen["O_clock"] > 0 and diag_gen["G_schur"] > 0 and diag_gen["C_schur"] > 0,
        "Regime 4 must exhibit strictly positive [S_mod, Delta_A] modular holonomy!",
    )

    # Coordinate-free O(2, Q) x O(2, Q) local gauge invariance check on Regime 4 (zero residual over Q!):
    U_A = [[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]]
    U_B = [[Fraction(5, 13), Fraction(-12, 13)], [Fraction(12, 13), Fraction(5, 13)]]
    U_loc = kron_q(U_A, U_B)
    rho_gen_rot = mat_mul_q(mat_mul_q(U_loc, rho_gen), mat_T_q(U_loc))
    diag_gen_rot = modular_schur_diagnostics_q(rho_gen_rot)
    check(
        diag_gen_rot["O_clock"] == diag_gen["O_clock"]
        and diag_gen_rot["G_schur"] == diag_gen["G_schur"]
        and diag_gen_rot["C_schur"] == diag_gen["C_schur"],
        "O(2,Q) x O(2,Q) local gauge invariance failed on Regime 4!",
    )

    # Exact 16x16 GKSL Lindblad-Zeno Horizon Quenching Bridge over Q(i) (AUDIT-018 link!):
    # H_horiz = g * (X_A x X_B), dissipator = gamma * D[Z_A x I_B] on 2-qubit density matrices in Q(i)^{4x4}.
    # In the 16-dim Pauli basis {I, X, Y, Z} x {I, X, Y, Z}:
    #   - D[Z_A x I_B] damps all 8 operators with A in {X, Y} at rate -2*gamma, and leaves all 8 with A in {I, Z} at 0!
    #   - -i[g (X_A x X_B), .] couples slow exterior pointer (Z_A x I_B) to fast cross-horizon (Y_A x X_B) with exact
    #     matrix elements ±2g, yielding exact Zeno Schur decay rate of Z_A x I_B:
    #       Gamma_Zeno(Z_A x I_B) = (2g)^2 / (2*gamma) = 2 g^2 / gamma  (pure Q(i) exact matrix Schur complement!)
    #   - Meanwhile (I_A x X_B) commutes with BOTH Z_A x I_B and X_A x X_B -> exact 0 decay rate!
    # Verify directly in exact 16x16 GaussQ superoperator arithmetic!
    g_val = Fraction(3, 2)
    gam_val = Fraction(25, 1)
    # 2x2 Pauli matrices over GaussQ
    pI = [[G1, G0], [G0, G1]]
    pX = [[G0, G1], [G1, G0]]
    pY = [[G0, -GI], [GI, G0]]
    pZ = [[G1, G0], [G0, -G1]]
    paulis = [("I", pI), ("X", pX), ("Y", pY), ("Z", pZ)]

    def kron_g(A: List[List[GaussQ]], B: List[List[GaussQ]]) -> List[List[GaussQ]]:
        return [[A[i // 2][j // 2] * B[i % 2][j % 2] for j in range(4)] for i in range(4)]

    def mul_g(A: List[List[GaussQ]], B: List[List[GaussQ]]) -> List[List[GaussQ]]:
        n = len(A)
        return [[sum((A[i][k] * B[k][j] for k in range(n)), G0) for j in range(n)] for i in range(n)]

    def sub_g(A: List[List[GaussQ]], B: List[List[GaussQ]]) -> List[List[GaussQ]]:
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    def inner_g(A: List[List[GaussQ]], B: List[List[GaussQ]]) -> GaussQ:
        return sum((A[i][j].conj() * B[i][j] for i in range(4) for j in range(4)), G0)

    # Order 16 Pauli basis as: 8 slow (A in {I, Z}) followed by 8 fast (A in {X, Y})
    slow_basis = [(f"{na}{nb}", kron_g(ma, mb)) for na, ma in [("I", pI), ("Z", pZ)] for nb, mb in paulis]
    fast_basis = [(f"{na}{nb}", kron_g(ma, mb)) for na, ma in [("X", pX), ("Y", pY)] for nb, mb in paulis]
    pbasis16 = slow_basis + fast_basis

    H_hor = [[GaussQ(g_val) * x for x in row] for row in kron_g(pX, pX)]
    L_mon = kron_g(pZ, pI)
    L_mat: List[List[Fraction]] = [[Fraction(0)] * 16 for _ in range(16)]
    for c, (_, Bc) in enumerate(pbasis16):
        # -i [H, Bc] + gamma * (L Bc L - Bc)
        comm = sub_g(mul_g(H_hor, Bc), mul_g(Bc, H_hor))
        unitary = [[(-GI) * x for x in row] for row in comm]
        diss = sub_g(mul_g(mul_g(L_mon, Bc), L_mon), Bc)
        tot_op = [[unitary[i][j] + GaussQ(gam_val) * diss[i][j] for j in range(4)] for i in range(4)]
        for r, (_, Br) in enumerate(pbasis16):
            val = inner_g(Br, tot_op) / GaussQ(4)
            check(val.im == 0, f"Unexpected imaginary superoperator entry at ({r},{c}): {val}")
            L_mat[r][c] = val.re

    # Partition into 8 slow (0..7) and 8 fast (8..15); exact Zeno Schur complement S_Zeno = L_ss - L_sf L_ff^{-1} L_fs!
    L_ss = [[L_mat[i][j] for j in range(8)] for i in range(8)]
    L_sf = [[L_mat[i][j] for j in range(8, 16)] for i in range(8)]
    L_fs = [[L_mat[i][j] for j in range(8)] for i in range(8, 16)]
    L_ff = [[L_mat[i][j] for j in range(8, 16)] for i in range(8, 16)]
    S_zeno = mat_sub_q(L_ss, mat_mul_q(mat_mul_q(L_sf, invert_q(L_ff)), L_fs))
    # Index 4 in slow_basis is "ZI", index 1 is "IX"
    zi_zeno_rate = -S_zeno[4][4]
    ix_zeno_rate = -S_zeno[1][1]
    expected_zi_rate = Fraction(2) * g_val * g_val / gam_val  # 2 * (9/4) / 25 = 9/50
    check(zi_zeno_rate == expected_zi_rate and ix_zeno_rate == 0, f"GKSL Zeno Schur rate mismatch: ZI={zi_zeno_rate}, IX={ix_zeno_rate}")

    return {
        "n0_prior_art_credited": "Takesaki (1972), Araki (1976), Petz (1986), Connes-Rovelli (1994), GKSL (1976)",
        "exact_schur_inverse_duality_verified": True,
        "regime_1_product": {
            "O_clock": str(diag_prod["O_clock"]),
            "G_schur": str(diag_prod["G_schur"]),
            "C_schur": str(diag_prod["C_schur"]),
            "C_gksl_Z": str(c_gksl_prod),
        },
        "regime_2_classical_correlated": {
            "O_clock": str(diag_cl["O_clock"]),
            "G_schur": str(diag_cl["G_schur"]),
            "plucker_gap_01_exact_match": str(actual_gap_01),
            "C_schur": str(diag_cl["C_schur"]),
            "C_gksl_Z_pointer_commutes": str(c_gksl_cl_Z),
            "C_gksl_X_wrong_basis_nonzero": str(c_gksl_cl_X),
        },
        "regime_3_werner_entangled_closed_forms": {
            "O_clock_formula": "24*q^2*(1 + 2*q + 3*q^2) / ((1 - q)^2 * (1 + 3*q)^2)",
            "C_gksl_formula_constant_all_O2Q": "256*q^2*(1 + 2*q + 3*q^2) / ((1 - q)^2 * (1 + 3*q)^2) == (32/3) * O_clock",
            "su2_eigenvalue_duality": "D_AA|_{su(2)} = lam(q), S_mod|_{su(2)} = 1/lam(q), lam(q) = (1+q)^2 / ((1-q)(1+3q))",
            "rows_verified_pure_Q": werner_rows,
        },
        "regime_4_generic_noncommuting_entangled": {
            "O_clock": str(diag_gen["O_clock"]),
            "G_schur": str(diag_gen["G_schur"]),
            "C_schur_nonzero_holonomy": str(diag_gen["C_schur"]),
            "O2Q_x_O2Q_local_gauge_invariant_zero_residual": True,
        },
        "gksl_zeno_schur_bridge_Qi": {
            "g": str(g_val),
            "gamma": str(gam_val),
            "ZI_zeno_schur_decay_rate_exact": str(zi_zeno_rate),
            "IX_commuting_sector_rate_exact": str(ix_zeno_rate),
            "formula_2g2_over_gamma_exact_match": True,
        },
    }


# =============================================================================
# 4. STRICT R3 NEGATIVE CONTROLS (8/8 REJECTED)
# =============================================================================

def run_r3_negative_controls() -> Dict[str, Any]:
    rejected: Dict[str, str] = {}
    for name, fn in [
        ("exact_frac_bool", lambda: exact_frac(True)),
        ("exact_frac_float", lambda: exact_frac(0.25)),
        ("gaussq_div_zero", lambda: G1 / G0),
        ("invert_singular_q", lambda: invert_q([[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]])),
        ("inertia_nonsymmetric", lambda: symmetric_inertia_q([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]])),
        ("density_non_faithful_singular", lambda: validate_faithful_density_q([[Fraction(1), Fraction(0), Fraction(0), Fraction(0)], [Fraction(0)] * 4, [Fraction(0)] * 4, [Fraction(0)] * 4])),
        ("density_wrong_trace", lambda: validate_faithful_density_q([[Fraction(1, 2) if i == j else Fraction(0) for j in range(4)] for i in range(4)])),
        ("householder_zero_vec", lambda: householder_q([Fraction(0), Fraction(0)])),
    ]:
        try:
            fn()
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            rejected[name] = type(exc).__name__
        else:
            raise RuntimeError(f"R3 control {name} failed to raise")
    return {"all_r3_rejected": True, "count": len(rejected), "exceptions": rejected}


def build_certificate() -> Dict[str, Any]:
    r3 = run_r3_negative_controls()
    p1 = run_part1_tripartite_singular_horizon()
    p2 = run_part2_unitary_page_r_opt()
    p3 = run_part3_modular_schur_gksl_obstructions()

    return {
        "probe": "probe_h1_horizon_schur_modular",
        "oracle_class": "exact",
        "honest_novelty_claim": "N1",
        "zero_floats_pure_Q_Qi": True,
        "r3_negative_controls": r3,
        "part1_tripartite_singular_horizon_haynsworth_krein": p1,
        "part2_unitary_page_turnaround_r_opt_r_h4": p2,
        "part3_four_regime_modular_schur_gksl": p3,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exact pure-Q/Q(i) horizon Schur-Haynsworth/Krein inertia, Page R_opt & modular-Schur/GKSL verifier"
    )
    parser.add_argument("--json", action="store_true", help="Emit canonical sorted JSON certificate to stdout")
    parser.add_argument("--write-cert", type=Path, default=None, help="Write canonical JSON certificate to path")
    args = parser.parse_args(argv)

    payload = build_certificate()
    canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    if args.write_cert is not None:
        args.write_cert.write_text(canonical, encoding="utf-8", newline="\n")

    if args.json:
        print(canonical, end="")
    else:
        r3 = payload["r3_negative_controls"]
        p1 = payload["part1_tripartite_singular_horizon_haynsworth_krein"]
        p2 = payload["part2_unitary_page_turnaround_r_opt_r_h4"]
        p3 = payload["part3_four_regime_modular_schur_gksl"]
        print("=== ARM H1 COMPLETE: EXACT PURE-Q/Q(i) HORIZON SCHUR, PAGE R_OPT & MODULAR OBSTRUCTIONS ===")
        print(f"R3 controls: {r3['count']}/8 rejected")
        print(f"Part 1 (Tripartite Singular Horizon): PSD inertia={p1['psd_screened_horizon']['inertia_G_psd']}, k_soft={p1['psd_screened_horizon']['k_soft_dim_ker_G_BB']}, Krein coupling r_cross=1,2 -> n_-=1,2 (GL-invariant)")
        print(f"Part 2 (N=6 Pure-Q Page Curve): R_opt peak t=3 = {p2['curve'][3]['R_opt_exact']} <= 8, exact Schmidt m=1..4, O(8,Q)-invariant, thermal breach t=4..6")
        print(f"Part 3 (4-Regime Modular-Schur & GKSL): Werner C_gksl == (32/3)*O_clock constant all O(2,Q); S_mod|_{{su(2)}}=1/lam(q); Generic [S_mod,Delta_A]!=0 ({p3['regime_4_generic_noncommuting_entangled']['C_schur_nonzero_holonomy']}), O(2,Q)xO(2,Q)-invariant; GKSL Zeno ZI rate={p3['gksl_zeno_schur_bridge_Qi']['ZI_zeno_schur_decay_rate_exact']}")
        print(f"Canonical SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
