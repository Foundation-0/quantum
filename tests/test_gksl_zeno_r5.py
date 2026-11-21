#!/usr/bin/env python3
"""Clean-room R5 mutation-killing unittest suite for quantum.gksl_lindblad_zeno (AUDIT-018).

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

from quantum import gksl_lindblad_zeno as gz  # noqa: E402


class TestGkslLindbladZenoR5(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cert = gz.build_certificate()

    def test_01_r3_strict_refusal_guards(self) -> None:
        r3 = self.cert["r3_tcb_negative_controls"]
        self.assertTrue(r3["all_r3_controls_rejected"])
        self.assertEqual(r3["count"], 12)

        with self.assertRaises(TypeError):
            gz.exact_frac(False)
        with self.assertRaises(TypeError):
            gz.exact_frac(0.5)
        with self.assertRaises(TypeError):
            gz.exact_frac("1/2")
        with self.assertRaisesRegex(ZeroDivisionError, r"Q\(i\)"):
            _ = gz.G1 / gz.G0
        with self.assertRaisesRegex(ValueError, "Negative"):
            gz.isqrt_bracket(Fraction(-1, 9))
        with self.assertRaisesRegex(ValueError, "prec_bits"):
            gz.isqrt_bracket(Fraction(2), prec_bits=0)
        with self.assertRaisesRegex(ValueError, "prec_bits"):
            gz.isqrt_bracket(Fraction(2), prec_bits=True)
        self.assertEqual(gz.isqrt_bracket(Fraction(0)), (Fraction(0), Fraction(0)))
        self.assertEqual(gz.isqrt_bracket(Fraction(9, 16)), (Fraction(3, 4), Fraction(3, 4)))

        with self.assertRaisesRegex(ValueError, "Empty"):
            gz.matinv_q([])
        with self.assertRaisesRegex(ValueError, "square"):
            gz.matinv_q([[1, 2]])
        with self.assertRaisesRegex(ValueError, "singular"):
            gz.matinv_q([[1, 2], [2, 4]])
        with self.assertRaisesRegex(ValueError, "Empty"):
            gz.matinv_g([])
        with self.assertRaisesRegex(ValueError, "square"):
            gz.matinv_g([[gz.G1, gz.G1]])
        with self.assertRaisesRegex(ValueError, "singular"):
            gz.matinv_g([[gz.G1, gz.G1], [gz.G1, gz.G1]])
        with self.assertRaisesRegex(ValueError, "nonzero"):
            gz.householder_q([Fraction(0), Fraction(0)])
        with self.assertRaises(RuntimeError):
            gz.check(False, "forced_fail")
        with self.assertRaises(RuntimeError):
            gz.verify_certificate_integrity({})
        bad_cert = dict(self.cert)
        bad_cert["oracle_class"] = "approx"
        with self.assertRaises(RuntimeError):
            gz.verify_certificate_integrity(bad_cert)

        # Exercise GaussQ equality/negation branches
        self.assertEqual(-gz.G1, gz.GaussQ(-1, 0))
        self.assertFalse(gz.G1 == True)
        self.assertFalse(gz.G1 == "1")
        self.assertTrue(gz.G1 == 1)
        self.assertEqual(1 + gz.G1, gz.GaussQ(2, 0))
        self.assertEqual(2 - gz.G1, gz.G1)
        self.assertEqual(3 * gz.G1, gz.GaussQ(3, 0))

    def test_02_part_a_exact_multipoles(self) -> None:
        pa = self.cert["part_a_exact_multipoles"]
        self.assertEqual(len(pa["configs_verified"]), 6)
        self.assertEqual(pa["configs_verified"][-1]["W_CM_over_W_single_exact"], "1000")
        self.assertTrue(pa["observer_invariant_Finv"]["permutation_zero_through_k10"])
        self.assertTrue(pa["negative_control_broken_CM"]["dipole_protection_broken"])

    def test_03_part_b_lindblad_zeno_and_ep2(self) -> None:
        pb = self.cert["part_b_exact_16x16_lindblad_zeno"]
        self.assertTrue(pb["modular_flow_tomita_takesaki"]["commutator_D_CM_Delta_rho_V_inv_zero"])
        self.assertTrue(pb["modular_flow_tomita_takesaki"]["kms_quantum_detailed_balance_zero"])
        self.assertEqual(pb["exceptional_point_EP2"]["degenerate_gt0_gamma_CM_eq_2g"]["full_16x16_rank_1_and_2"], [12, 8])
        self.assertEqual(pb["exceptional_point_EP2"]["split_gt1_isolates_IX_IY_EP2"]["full_16x16_rank_1_and_2"], [14, 12])
        self.assertTrue(pb["basis_invariance_and_witness_negative_controls"]["full_O16Q_trace_invariance_k1_to_4"])
        self.assertTrue(pb["basis_invariance_and_witness_negative_controls"]["block_O8Q_schur_exact_covariance"])
        self.assertEqual(pb["basis_invariance_and_witness_negative_controls"]["neg_ctrl_local_IZ_destroys_zeno"]["good_CM_witness_IX_rate"], "1/5")


if __name__ == "__main__":
    unittest.main()
