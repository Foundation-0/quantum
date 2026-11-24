#!/usr/bin/env python3
"""Master R4-clean test runner for Foundation-0/quantum.

Executes:
  1. All four exact zero-float verification modules via `quantum.cli.run_verify("all")`
  2. Clean-room R5 unittest suite for `quantum.double_slit_continuum` (AUDIT-054)
  3. Clean-room R5 unittest suite for `quantum.gksl_lindblad_zeno` (AUDIT-018)
  4. Clean-room R5 unittest suite for `quantum.unified_obstruction` (AUDIT-056)
  5. CLI smoke checks (`list`, `verify --module unified --json`)

Zero third-party dependencies; zero bare `assert`s; bit-identical across all 4 isolated
R4 modes (`-I -B`, `-I -O -B`, `-I -B -W error`, `-I -O -B -W error`).
"""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
for p in (str(ROOT), str(TESTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from quantum import cli  # noqa: E402
import test_double_slit_r5  # noqa: E402
import test_gksl_zeno_r5  # noqa: E402
import test_quantum_unified_r5  # noqa: E402


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(f"QUANTUM_TEST_RUNNER_FAILED: {msg}")


def _run_suite(mod: object, label: str) -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(mod)
    sink = io.StringIO()
    result = unittest.TextTestRunner(stream=sink, verbosity=0).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError(f"{label} R5 unittest failed:\n{sink.getvalue()}")
    return result.testsRun


def main() -> int:
    # 1. All 4 exact zero-float verification modules
    bundle = cli.run_verify("all")
    require(bundle["all_verified"] is True, "Not all modules verified")
    require(bundle["modules_verified"] == 4, f"Expected 4 modules, got {bundle['modules_verified']}")
    require(bundle["zero_floats"] is True, "Float detected in verification output")

    # 2-4. Clean-room R5 unittest suites
    n_ds = _run_suite(test_double_slit_r5, "double_slit_continuum")
    n_gz = _run_suite(test_gksl_zeno_r5, "gksl_lindblad_zeno")
    n_qu = _run_suite(test_quantum_unified_r5, "unified_obstruction")

    # 5. CLI smoke checks (no disk side effects!)
    buf_list = io.StringIO()
    with redirect_stdout(buf_list):
        rc_list = cli.main(["list"])
    require(rc_list == 0 and "unified" in buf_list.getvalue(), "CLI list check failed")

    buf_json = io.StringIO()
    with redirect_stdout(buf_json):
        rc_json = cli.main(["verify", "--module", "unified", "--json"])
    require(rc_json == 0, "CLI verify --json failed")
    parsed = json.loads(buf_json.getvalue())
    require(parsed["all_verified"] is True and parsed["modules_verified"] == 1, "CLI JSON output invalid")

    print("=== Foundation-0/quantum FULL VERIFICATION PASS ===")
    for key, info in bundle["receipts"].items():
        print(f"  [PASS] {key:12s}  sha256={info['canonical_sha256']}")
    print(f"  [PASS] double_slit_continuum R5 suite: {n_ds}/{n_ds} tests")
    print(f"  [PASS] gksl_lindblad_zeno R5 suite:    {n_gz}/{n_gz} tests")
    print(f"  [PASS] unified_obstruction R5 suite:   {n_qu}/{n_qu} tests")
    print(f"  Bundle SHA-256: {bundle['bundle_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
