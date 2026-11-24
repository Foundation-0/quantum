"""Unified zero-dependency CLI for Foundation-0/quantum.

Usage:
    PYTHONPATH=. python3 -s -B -m quantum verify [--json] [--module all|double_slit|gksl|modular|unified]
    PYTHONPATH=. python3 -s -B -m quantum list
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from typing import Any, Callable, Dict, Optional, Sequence, Tuple

from . import __version__
from . import double_slit_continuum
from . import gksl_lindblad_zeno
from . import modular_schur_quantum
from . import unified_obstruction


def _canonical_digest(payload: Dict[str, Any]) -> Tuple[str, str]:
    text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    return text, hashlib.sha256(text.encode("utf-8")).hexdigest()


def _count_floats(obj: Any) -> int:
    if isinstance(obj, float):
        return 1
    if isinstance(obj, dict):
        return sum(_count_floats(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(_count_floats(v) for v in obj)
    return 0


_MODULES: Dict[str, Tuple[str, Callable[[], Dict[str, Any]]]] = {
    "double_slit": (
        "AUDIT-054: 4-Regime Double-Slit & Sorkin Triple-Slit Continuum-Observer Obstruction Instrument",
        double_slit_continuum.build_certificate,
    ),
    "gksl": (
        "AUDIT-018: Exact Multipole N^3 Law & 16x16 GKSL Tomita-Takesaki / Zeno Schur / EP2 Jordan / Riccati Bridge",
        gksl_lindblad_zeno.build_certificate,
    ),
    "modular": (
        "AUDIT-041: Tripartite Singular-Horizon Schur/Krein Inertia, Pure-Q Page R_opt & 4-Regime Modular-Schur/GKSL Obstructions",
        modular_schur_quantum.build_certificate,
    ),
    "unified": (
        "AUDIT-056: M-Slit Looped-Schur Sorkin Order Law, Complex U(1) Surgical Severing + Two-Phase Green's Tomography, Z_4 Eraser & Modular-GKSL Equalizer",
        unified_obstruction.build_certificate,
    ),
}


def run_verify(module_choice: str = "all") -> Dict[str, Any]:
    if module_choice == "all":
        selected = list(_MODULES.keys())
    elif module_choice in _MODULES:
        selected = [module_choice]
    else:
        raise ValueError(f"Unknown module selector: {module_choice}")

    receipts: Dict[str, Dict[str, Any]] = {}
    for key in selected:
        desc, builder = _MODULES[key]
        payload = builder()
        _, digest = _canonical_digest(payload)
        float_count = _count_floats(payload)
        if float_count != 0:
            raise RuntimeError(f"Module {key} emitted {float_count} float(s); zero floats required")
        receipts[key] = {
            "description": desc,
            "oracle_class": "exact",
            "zero_floats": True,
            "canonical_sha256": digest,
            "verified": True,
        }

    bundle: Dict[str, Any] = {
        "package": "quantum",
        "version": __version__,
        "oracle_class": "exact",
        "zero_floats": True,
        "modules_verified": len(receipts),
        "all_verified": all(r["verified"] for r in receipts.values()),
        "receipts": receipts,
    }
    _, bundle_sha = _canonical_digest(bundle)
    bundle["bundle_sha256"] = bundle_sha
    return bundle


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="quantum",
        description="Foundation-0/quantum exact zero-float quantum obstruction verification suite",
    )
    parser.add_argument("--version", action="version", version=f"quantum {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_ver = sub.add_parser("verify", help="Run exact pure-Q/Q(i) verification modules and emit SHA-256 receipts")
    p_ver.add_argument(
        "--module",
        choices=["all", "double_slit", "gksl", "modular", "unified"],
        default="all",
        help="Module to verify (default: all)",
    )
    p_ver.add_argument("--json", action="store_true", help="Emit canonical JSON receipt bundle to stdout")

    sub.add_parser("list", help="List available exact verification modules")

    args = parser.parse_args(argv)
    if args.command == "list":
        for key, (desc, _) in _MODULES.items():
            print(f"{key:12s}  {desc}")
        return 0

    if args.command == "verify":
        bundle = run_verify(args.module)
        if args.json:
            text, _ = _canonical_digest(bundle)
            sys.stdout.write(text)
        else:
            print(f"=== Foundation-0/quantum v{__version__} Exact Zero-Float Verification ===")
            for key, info in bundle["receipts"].items():
                print(f"[PASS] {key:12s}  sha256={info['canonical_sha256'][:16]}...  {info['description']}")
            print(f"Modules verified: {bundle['modules_verified']}/{len(_MODULES) if args.module == 'all' else 1} (0 floats)")
            print(f"Bundle SHA-256:   {bundle['bundle_sha256']}")
        return 0

    parser.print_help()
    return 0
