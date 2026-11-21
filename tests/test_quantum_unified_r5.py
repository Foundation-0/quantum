#!/usr/bin/env python3
"""Clean-room R5 mutation-killing unittest suite for quantum.unified_obstruction (AUDIT-056).

100% pure Python 3 stdlib; zero bare asserts; targets 100.0% kill rate under `aletheia mutate`.
"""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from quantum import unified_obstruction as qu  # noqa: E402


class TestQuantumUnifiedObstructionR5(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cert = qu.build_certificate()

    def test_01_r3_strict_refusal_guards(self) -> None:
        r3 = self.cert["r3_negative_controls"]
        self.assertTrue(r3["all_r3_rejected"])
        self.assertEqual(r3["count"], 10)

        with self.assertRaises(TypeError):
            qu.exact_frac(False)
        with self.assertRaises(TypeError):
            qu.exact_frac("1/2")
        with self.assertRaisesRegex(ZeroDivisionError, r"Q\(i\)"):
            _ = qu.G1 / qu.G0
        with self.assertRaises(ValueError):
            qu.mat_mul_q([], [[Fraction(1)]])
        with self.assertRaises(ValueError):
            qu.mat_mul_q([[Fraction(1)]], [[Fraction(1)], [Fraction(2)]])
        with self.assertRaises(ValueError):
            qu.mat_mul_qi([], [[qu.G1]])
        with self.assertRaises(ValueError):
            qu.mat_mul_qi([[qu.G1]], [[qu.G1], [qu.G1]])
        with self.assertRaises(ValueError):
            qu.invert_q([])
        with self.assertRaises(ValueError):
            qu.invert_q([[Fraction(1), Fraction(2)]])
        with self.assertRaisesRegex(ValueError, "Singular"):
            qu.invert_q([[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]])
        with self.assertRaises(ValueError):
            qu.invert_qi([])
        with self.assertRaises(ValueError):
            qu.invert_qi([[qu.G1, qu.G1]])
        with self.assertRaisesRegex(ValueError, "Singular"):
            qu.invert_qi([[qu.G1, qu.G1], [qu.G1, qu.G1]])

        # Part 1 guards
        with self.assertRaises(ValueError):
            qu.formal_looped_sorkin_series(True, [qu.G1, qu.G1], [qu.G1, qu.G1], [Fraction(1), Fraction(1)], [[Fraction(0)] * 2] * 2, 1)
        with self.assertRaises(ValueError):
            qu.formal_looped_sorkin_series(2, [qu.G1], [qu.G1, qu.G1], [Fraction(1), Fraction(1)], [[Fraction(0)] * 2] * 2, 1)
        with self.assertRaises(ValueError):
            qu.formal_looped_sorkin_series(2, [qu.G1, qu.G1], [qu.G1, qu.G1], [Fraction(1), Fraction(1)], [[Fraction(0)] * 2] * 2, -1)
        with self.assertRaises(ValueError):
            qu.formal_looped_sorkin_series(2, [qu.G1, qu.G1], [qu.G1, qu.G1], [Fraction(1), Fraction(1)], [[Fraction(0)] * 2] * 2, True)
        with self.assertRaisesRegex(ValueError, "nonzero"):
            qu.formal_looped_sorkin_series(2, [qu.G1, qu.G1], [qu.G1, qu.G1], [Fraction(0), Fraction(1)], [[Fraction(0)] * 2] * 2, 1)
        with self.assertRaisesRegex(ValueError, "positive"):
            qu.finite_g_looped_sorkin_m(2, [qu.G0, qu.G0], [qu.G1, qu.G1], [Fraction(1), Fraction(1)], [[Fraction(0)] * 2] * 2, Fraction(0))
        with self.assertRaises(ValueError):
            qu.m_slit_born_and_quartic_sorkin([qu.G1], Fraction(0))
        with self.assertRaisesRegex(ValueError, "nonzero"):
            qu.m_slit_born_and_quartic_sorkin([qu.G0, qu.G0], Fraction(0))
        with self.assertRaises(ValueError):
            qu.m_slit_pure_bath_complementarity([[qu.G1]])
        with self.assertRaises(ValueError):
            qu.m_slit_pure_bath_complementarity([[], []])
        with self.assertRaises(ValueError):
            qu.m_slit_pure_bath_complementarity([[qu.G1], [qu.G1, qu.G0]])
        with self.assertRaisesRegex(ValueError, "unit norm2"):
            qu.m_slit_pure_bath_complementarity([[qu.GaussQ(2, 0)], [qu.G1]])

        # Part 2 guards
        with self.assertRaisesRegex(ValueError, "n_verts"):
            qu.verify_u1_surgical_and_greens_tomography("bad_n", 1, [(0, 0, Fraction(1))], [0], 0)
        with self.assertRaisesRegex(ValueError, "n_verts"):
            qu.verify_u1_surgical_and_greens_tomography("bad_bool", True, [(0, 0, Fraction(1))], [0], 0)
        with self.assertRaisesRegex(ValueError, "Boundary"):
            qu.verify_u1_surgical_and_greens_tomography("empty_b", 2, [(0, 1, Fraction(1))], [], 0)
        with self.assertRaisesRegex(ValueError, "Boundary"):
            qu.verify_u1_surgical_and_greens_tomography("dup_b", 2, [(0, 1, Fraction(1))], [0, 0], 0)
        with self.assertRaisesRegex(ValueError, "twist_idx"):
            qu.verify_u1_surgical_and_greens_tomography("bad_idx", 2, [(0, 1, Fraction(1))], [0], 2)
        with self.assertRaisesRegex(ValueError, "positive"):
            qu.verify_u1_surgical_and_greens_tomography("zero_w", 2, [(0, 1, Fraction(0))], [0], 0)
        with self.assertRaisesRegex(ValueError, "positive"):
            qu.verify_u1_surgical_and_greens_tomography("neg_w", 2, [(0, 1, Fraction(-1))], [0], 0)
        with self.assertRaisesRegex(ValueError, "positive"):
            qu.verify_u1_surgical_and_greens_tomography("bad_other_w", 3, [(0, 1, Fraction(1)), (1, 2, Fraction(0))], [0], 0)
        with self.assertRaisesRegex(ValueError, "positive"):
            qu.verify_u1_surgical_and_greens_tomography("neg_other_w", 3, [(0, 1, Fraction(1)), (1, 2, Fraction(-1))], [0], 0)

        # Part 3 & integrity guards
        with self.assertRaisesRegex(ValueError, r"\[0, 1\)"):
            qu.werner_modular_gksl_eraser_point(Fraction(-1, 4))
        with self.assertRaisesRegex(ValueError, r"\[0, 1\)"):
            qu.werner_modular_gksl_eraser_point(Fraction(1))
        with self.assertRaises(RuntimeError):
            qu.verify_certificate_integrity({})

    def test_02_part1_m_slit_sorkin_and_complementarity(self) -> None:
        p1 = self.cert["part1_m_slit_sorkin_order_law_and_complementarity"]
        self.assertTrue(p1["part1_all_verified"])
        rows = p1["m_slit_sorkin_order_law_rows"]
        self.assertEqual([r["M_slits"] for r in rows], [2, 3, 4, 5])
        self.assertEqual(rows[3]["quartic_kerr_I_M"], "0")
        self.assertTrue(rows[3]["five_slit_loop_vs_kerr_separator"])
        self.assertTrue(p1["u1_phase_and_S4_permutation_invariant"])

    def test_03_part2_u1_surgical_greens_tomography_and_z4_eraser(self) -> None:
        p2 = self.cert["part2_u1_surgical_greens_tomography_and_z4_eraser"]
        self.assertTrue(p2["part2_all_verified"])
        self.assertEqual(len(p2["u1_surgical_and_two_phase_greens_tomography_cases"]), 7)
        b5_case = p2["u1_surgical_and_two_phase_greens_tomography_cases"][3]
        self.assertEqual(b5_case["G_cut_interior_exact"], "3/7")
        self.assertEqual(b5_case["w_c_harm_B_exact"], "274/249")
        e3 = [(0, 1, Fraction(2)), (1, 2, Fraction(3)), (2, 0, Fraction(5))]
        res_k3 = qu.verify_u1_surgical_and_greens_tomography("K3_full_bnd", 3, e3, [0, 1, 2], 0)
        self.assertTrue(res_k3["all_4_complex_u1_surgical_severing_exact"])
        self.assertEqual(res_k3["G_cut_interior_exact"], "0")
        self.assertEqual(-qu.G1, qu.GaussQ(-1, 0))
        self.assertFalse(qu.G1 == True)
        self.assertFalse(qu.G1 == "1")
        self.assertTrue(qu.G1 == 1)

    def test_04_part3_modular_gksl_eraser_bridge(self) -> None:
        p3 = self.cert["part3_modular_gksl_eraser_bridge"]
        self.assertTrue(p3["part3_all_verified"])
        self.assertTrue(p3["monotone_modular_zeno_freezing_verified"])
        self.assertTrue(p3["chsh_classicality_threshold_5_7_verified"])

    def test_05_part4_eight_glyph_receipts(self) -> None:
        p4 = self.cert["part4_eight_glyph_calculus_receipts"]
        self.assertTrue(p4["glyph_basis_verified_Sm"])
        self.assertEqual(len(p4["compressed_quantum_laws"]), 4)


if __name__ == "__main__":
    unittest.main()
