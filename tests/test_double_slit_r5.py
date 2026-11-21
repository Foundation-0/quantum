#!/usr/bin/env python3
"""Clean-room R5 mutation-killing unittest suite for quantum.double_slit_continuum (AUDIT-054).

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

from quantum import double_slit_continuum as ds  # noqa: E402


class TestDoubleSlitContinuumObserverR5(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cert = ds.build_certificate()

    def test_01_r3_strict_refusal_guards(self) -> None:
        r3 = self.cert["r3_negative_controls"]
        self.assertTrue(r3["all_r3_rejected"])
        self.assertEqual(r3["count"], 10)

        with self.assertRaises(TypeError):
            ds.exact_frac(False)
        with self.assertRaises(TypeError):
            ds.exact_frac("1/2")
        with self.assertRaisesRegex(ZeroDivisionError, r"Q\(i\)"):
            _ = ds.G1 / ds.G0
        with self.assertRaises(ValueError):
            ds.mat_mul_q([], [[Fraction(1)]])
        with self.assertRaises(ValueError):
            ds.mat_mul_q([[Fraction(1)]], [[Fraction(1)], [Fraction(2)]])
        with self.assertRaises(ValueError):
            ds.mat_mul_qi([], [[ds.G1]])
        with self.assertRaises(ValueError):
            ds.mat_mul_qi([[ds.G1]], [[ds.G1], [ds.G1]])
        with self.assertRaises(ValueError):
            ds.invert_q([])
        with self.assertRaises(ValueError):
            ds.invert_q([[Fraction(1), Fraction(2)]])
        with self.assertRaisesRegex(ValueError, "Singular"):
            ds.invert_q([[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]])
        with self.assertRaises(ValueError):
            ds.invert_qi([])
        with self.assertRaises(ValueError):
            ds.invert_qi([[ds.G1, ds.G1]])
        with self.assertRaisesRegex(ValueError, "Singular"):
            ds.invert_qi([[ds.G1, ds.G1], [ds.G1, ds.G1]])

        with self.assertRaises(ValueError):
            ds.signed_dtn_q(1, [], [0], [])
        with self.assertRaises(ValueError):
            ds.signed_dtn_q(True, [], [0], [])
        with self.assertRaises(ValueError):
            ds.signed_dtn_q(2, [(0, 1, Fraction(1))], [], [1])
        with self.assertRaises(ValueError):
            ds.signed_dtn_q(2, [(0, 1, Fraction(1))], [0, 0], [1])
        with self.assertRaisesRegex(ValueError, "length"):
            ds.signed_dtn_q(2, [(0, 1, Fraction(1))], [0], [1, 1])
        with self.assertRaisesRegex(ValueError, "positive"):
            ds.signed_dtn_q(2, [(0, 1, Fraction(0))], [0], [1])
        with self.assertRaisesRegex(ValueError, "positive"):
            ds.signed_dtn_q(2, [(0, 1, Fraction(-1))], [0], [1])
        with self.assertRaises(ValueError):
            ds.signed_dtn_q(2, [(0, 1, Fraction(1))], [0], [True])
        with self.assertRaises(ValueError):
            ds.signed_dtn_q(2, [(0, 1, Fraction(1))], [0], [2])

        with self.assertRaises(ValueError):
            ds.pure_and_mixed_bath_complementarity(Fraction(-1, 4), Fraction(1))
        with self.assertRaises(ValueError):
            ds.pure_and_mixed_bath_complementarity(Fraction(5, 4), Fraction(1))
        with self.assertRaises(ValueError):
            ds.pure_and_mixed_bath_complementarity(Fraction(1, 2), Fraction(3, 2))
        with self.assertRaisesRegex(ValueError, "gamma_damp"):
            ds.verify_gksl_16x16_schur_dephasing(Fraction(1), Fraction(0))
        with self.assertRaisesRegex(ValueError, "gamma_damp"):
            ds.verify_gksl_16x16_schur_dephasing(Fraction(1), Fraction(-1))
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([], [], [])
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([Fraction(1)], [Fraction(1), Fraction(0)], [Fraction(0)])
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([Fraction(-1), Fraction(2)], [Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)])
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([Fraction(1, 2)], [Fraction(1)], [Fraction(0)])
        with self.assertRaisesRegex(ValueError, "Slit probability"):
            ds.verify_classical_ensemble_bound([Fraction(1)], [Fraction(2)], [Fraction(0)])
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([Fraction(1)], [Fraction(1, 2)], [Fraction(-1, 2)])
        with self.assertRaises(ValueError):
            ds.verify_classical_ensemble_bound([Fraction(1)], [Fraction(1, 2)], [Fraction(2)])

        zero_probs = {m: Fraction(0) for m in [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]}
        with self.assertRaisesRegex(ValueError, "positive"):
            ds.sorkin_invariant_from_probs(zero_probs)
        with self.assertRaises(ValueError):
            ds.linear_bath_3slit_probs([ds.G1], [[ds.G1]])
        bad_gram = [[ds.G1, ds.GI, ds.G0], [ds.GI, ds.G1, ds.G0], [ds.G0, ds.G0, ds.G1]]
        with self.assertRaisesRegex(ValueError, "Non-Hermitian"):
            ds.linear_bath_3slit_probs([ds.G1, ds.G1, ds.G1], bad_gram)
        with self.assertRaises(ValueError):
            ds.linear_looped_schur_3slit_probs([ds.G1], [ds.G1], [Fraction(1)], [[Fraction(0)]], Fraction(0))
        with self.assertRaises(ValueError):
            ds.cayley_kerr_cross_phase_3slit_probs([ds.G1], [[Fraction(0)]], Fraction(0))
        with self.assertRaises(ValueError):
            ds.quartic_kerr_born_3slit_probs([ds.G1], Fraction(0))
        with self.assertRaisesRegex(ValueError, "length"):
            ds.finite_t_magnetic_energy_q(2, [(0, 1, Fraction(1))], [0], [Fraction(1), Fraction(2)], Fraction(1))
        with self.assertRaises(RuntimeError):
            ds.verify_certificate_integrity({})

    def test_02_regime_I_and_edge_branches(self) -> None:
        p1 = self.cert["part1_regime_I_linear_continuum_bath"]
        self.assertTrue(p1["regime_I_all_verified"])
        self.assertEqual(p1["gksl_16x16_schur_dephasing"]["slit_coherence_dephasing_rates_XI_YI"], ["9/50", "9/50"])
        self.assertTrue(p1["surgical_coherence_severing_AUDIT047R_part3"]["Lam_red_equals_Lam_severed_slit_A_exact"])
        self.assertTrue(p1["quantum_eraser_deck_splitting_AUDIT047R_part4"]["M_deck_T_Lam_tilde_M_deck_eq_2_LamPlus_oplus_LamChi"])
        lam_p = ds.signed_dtn_q(2, [(0, 1, Fraction(3))], [0, 1], [1])
        red, phi = ds.monopole_reduced_dtn_q(lam_p)
        self.assertEqual(phi, Fraction(0))
        self.assertEqual(red, lam_p)
        self.assertEqual(ds.finite_t_magnetic_energy_q(2, [(0, 1, Fraction(1))], [0, 1], [Fraction(1)], Fraction(1)), Fraction(2))
        self.assertEqual(-ds.G1, ds.GaussQ(-1, 0))
        self.assertFalse(ds.G1 == True)
        self.assertFalse(ds.G1 == "1")
        self.assertTrue(ds.G1 == 1)

    def test_03_regime_II_classical_farkas_nogo(self) -> None:
        p2 = self.cert["part2_regime_II_classical_falsification"]
        self.assertTrue(p2["regime_II_falsification_verified"])
        chsh = p2["fine_farkas_16vertex_chsh_delayed_choice_nogo"]
        self.assertEqual(chsh["S_CHSH_quantum_345_exact"], "14/5")
        self.assertEqual(chsh["all_16_classical_vertices_range"], [-2, 2])
        self.assertTrue(chsh["no_signaling_marginals_exact_zero"])

    def test_04_regime_III_sorkin_separation_and_scaling(self) -> None:
        p3 = self.cert["part3_sorkin_triple_slit_tomography"]
        self.assertTrue(p3["part3_all_verified"])
        self.assertTrue(p3["regime_I_linear_born_and_arbitrary_bath_I_ABC_zero"])
        self.assertTrue(p3["regime_III_A_linear_looped_schur"]["all_nonzero_and_degree0_intensity_invariant"])
        self.assertTrue(p3["regime_III_B1_norm_conserving_cayley_kerr"]["all_nonzero_and_scale_breaking"])
        self.assertTrue(p3["regime_III_B2_quartic_kerr_born"]["exact_quadratic_intensity_scaling_lam2"])
        self.assertTrue(p3["u1_phase_and_S3_slit_permutation_invariance_exact"])

    def test_05_part4_parallel_sum_screening(self) -> None:
        p4 = self.cert["part4_parallel_sum_continuum_observer_screening"]
        self.assertTrue(p4["part4_all_verified"])
        self.assertEqual(len(p4["symmetric_2slit_parallel_sum_rows"]), 9)
        self.assertEqual(len(p4["rayleigh_shunt_ceiling_rows"]), 4)
        self.assertEqual(len(p4["observer_decoherence_competition_rows"]), 4)


if __name__ == "__main__":
    unittest.main()
