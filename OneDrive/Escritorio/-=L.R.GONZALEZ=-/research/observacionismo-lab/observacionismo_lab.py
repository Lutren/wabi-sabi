#!/usr/bin/env python3
"""
Observacionismo Lab: observer/proxy audit for local PSI Chi experiments.

This local harness fixes the early prototype pitfalls:
- clone RCPoint values before mutating;
- use deterministic per-profile seeds;
- probabilistic completion factors such as 0.8 work as intended;
- high signal attention changes uncertainty instead of duplicating evidence;
- observer names are low-claim proxy descriptions.
- negative controls can deliberately break the data/model link.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import random
import statistics
import sys
from collections import Counter
from dataclasses import replace
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


DEFAULT_ENGINE = Path(r"C:\Users\L-Tyr\psi_chi_lab_v9.py")


def load_engine(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"PSI Chi engine not found: {path}")
    spec = importlib.util.spec_from_file_location("psi_chi_lab_v9_local", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import engine: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def clone_points(points: Iterable[object]) -> List[object]:
    return [replace(p) for p in points]


def stable_seed(seed: int, label: str) -> int:
    digest = hashlib.blake2b(label.encode("utf-8"), digest_size=4).hexdigest()
    return (seed + int(digest, 16)) % (2**32)


def maybe_add_completion_points(points: List[object], extra: List[object], factor: float, rng: random.Random) -> List[object]:
    whole = int(math.floor(max(0.0, factor)))
    frac = max(0.0, factor - whole)
    out = list(points)
    for _ in range(whole):
        out.extend(clone_points(extra))
    for item in extra:
        if rng.random() < frac:
            out.append(replace(item))
    return out


OBSERVER_PROFILES: Dict[str, Dict[str, object]] = {
    "visual_proxy": {
        "description": "Visual-style data mask: radial inversion, mild imputation, coarse velocity bins and outer-radius uncertainty.",
        "invert_radial": True,
        "completion_factor": 0.8,
        "remove_low_contrast": 0.05,
        "weight_by_sn": True,
        "discretize_velocity": 5.0,
        "attenuate_outer": 0.5,
        "separate_components": False,
    },
    "component_split_proxy": {
        "description": "Component-split proxy: gas/disk/bulge are inspected separately; not a direct dark-matter or gravity-only observer.",
        "invert_radial": False,
        "completion_factor": 0.2,
        "remove_low_contrast": 0.12,
        "weight_by_sn": False,
        "discretize_velocity": 0.0,
        "attenuate_outer": 0.0,
        "separate_components": True,
    },
    "phase_proxy": {
        "description": "Curve-shape proxy: preserves component split and uses light velocity quantization; not a real phase instrument.",
        "invert_radial": True,
        "completion_factor": 0.0,
        "remove_low_contrast": 0.15,
        "weight_by_sn": False,
        "discretize_velocity": 2.0,
        "attenuate_outer": 0.0,
        "separate_components": True,
    },
    "instrument_balanced": {
        "description": "Balanced baseline: no deliberate observer distortion.",
        "invert_radial": False,
        "completion_factor": 0.0,
        "remove_low_contrast": 0.0,
        "weight_by_sn": False,
        "discretize_velocity": 0.0,
        "attenuate_outer": 0.0,
        "separate_components": False,
    },
    "scientific_community": {
        "description": "Peer-review proxy: conservative uncertainty inflation and no imputed evidence.",
        "invert_radial": False,
        "completion_factor": 0.0,
        "remove_low_contrast": 0.0,
        "weight_by_sn": False,
        "discretize_velocity": 0.0,
        "attenuate_outer": 0.15,
        "separate_components": False,
        "error_scale": 1.15,
    },
    "adversarial_observer": {
        "description": "Stress-test proxy: drops some outer-radius evidence, perturbs radii and adds measurement noise.",
        "invert_radial": False,
        "completion_factor": 0.0,
        "remove_low_contrast": 0.08,
        "weight_by_sn": False,
        "discretize_velocity": 4.0,
        "attenuate_outer": 1.0,
        "separate_components": False,
        "drop_outer_quantile": 0.25,
        "radius_scale_sigma": 0.08,
        "velocity_noise_sigma": 0.75,
        "error_scale": 1.25,
    },
}


CONTROL_MODES = ("none", "shuffled_baryons", "shuffled_velocities")


def apply_negative_control(points: List[object], mode: str, seed: int) -> List[object]:
    if mode not in CONTROL_MODES:
        raise ValueError(f"Unknown control mode: {mode}")
    pts = clone_points(points)
    if mode == "none":
        return pts

    rng = random.Random(seed)
    if mode == "shuffled_baryons":
        components = [(p.vgas_kms, p.vdisk_kms, p.vbul_kms, p.sb_disk, p.sb_bul) for p in pts]
        rng.shuffle(components)
        for point, values in zip(pts, components):
            point.vgas_kms, point.vdisk_kms, point.vbul_kms, point.sb_disk, point.sb_bul = values
        return pts

    observed = [(p.vobs_kms, p.evobs_kms) for p in pts]
    rng.shuffle(observed)
    for point, values in zip(pts, observed):
        point.vobs_kms, point.evobs_kms = values
    return pts


def apply_observer_proxy(points: List[object], profile: Dict[str, object], engine, seed: int) -> List[object]:
    rng = random.Random(seed)
    pts = clone_points(points)
    RCPoint = engine.RCPoint

    radius_sigma = float(profile.get("radius_scale_sigma", 0.0))
    if radius_sigma > 0:
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            scale = rng.lognormvariate(0.0, radius_sigma)
            for point in gpts:
                point.r_kpc *= scale

    if profile.get("separate_components", False):
        split = []
        for pt in pts:
            if pt.vgas_kms > 0:
                split.append(RCPoint(pt.galaxy, pt.r_kpc, pt.vobs_kms, pt.evobs_kms, pt.vgas_kms, 0.0, 0.0, pt.sb_disk, pt.sb_bul))
            if pt.vdisk_kms > 0:
                split.append(RCPoint(pt.galaxy, pt.r_kpc, pt.vobs_kms, pt.evobs_kms, 0.0, pt.vdisk_kms, 0.0, pt.sb_disk, pt.sb_bul))
            if pt.vbul_kms > 0:
                split.append(RCPoint(pt.galaxy, pt.r_kpc, pt.vobs_kms, pt.evobs_kms, 0.0, 0.0, pt.vbul_kms, pt.sb_disk, pt.sb_bul))
        if split:
            pts = split

    drop_outer = float(profile.get("drop_outer_quantile", 0.0))
    if drop_outer > 0:
        filtered = []
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            ordered = sorted(gpts, key=lambda x: x.r_kpc)
            keep_count = max(4, int(math.ceil(len(ordered) * (1.0 - min(drop_outer, 0.9)))))
            filtered.extend(ordered[:keep_count])
        pts = filtered

    if profile.get("invert_radial", False):
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            radii = [p.r_kpc for p in gpts]
            rmin, rmax = min(radii), max(radii)
            for p in gpts:
                p.r_kpc = rmin + (rmax - p.r_kpc)

    factor = float(profile.get("completion_factor", 0.0))
    if factor > 0:
        extra = []
        for gal, gpts in engine.group_by_galaxy(pts).items():
            ordered = sorted(gpts, key=lambda x: x.r_kpc)
            for left, right in zip(ordered, ordered[1:]):
                extra.append(RCPoint(
                    gal,
                    (left.r_kpc + right.r_kpc) / 2.0,
                    (left.vobs_kms + right.vobs_kms) / 2.0,
                    max(left.evobs_kms, right.evobs_kms) * 1.5,
                    (left.vgas_kms + right.vgas_kms) / 2.0,
                    (left.vdisk_kms + right.vdisk_kms) / 2.0,
                    (left.vbul_kms + right.vbul_kms) / 2.0,
                    (left.sb_disk + right.sb_disk) / 2.0,
                    (left.sb_bul + right.sb_bul) / 2.0,
                ))
        pts = maybe_add_completion_points(pts, extra, factor, rng)

    low = float(profile.get("remove_low_contrast", 0.0))
    if low > 0:
        filtered = []
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            ordered = sorted(gpts, key=lambda x: x.r_kpc)
            if len(ordered) <= 1:
                filtered.extend(ordered)
                continue
            keep = [True] * len(ordered)
            for idx in range(1, len(ordered)):
                delta = abs(ordered[idx].vobs_kms - ordered[idx - 1].vobs_kms) / max(abs(ordered[idx].vobs_kms), 1.0)
                if delta < low:
                    drop = idx if ordered[idx].evobs_kms >= ordered[idx - 1].evobs_kms else idx - 1
                    keep[drop] = False
            filtered.extend(point for idx, point in enumerate(ordered) if keep[idx])
        pts = filtered

    if profile.get("weight_by_sn", False):
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            values = [abs(p.vobs_kms) / max(p.evobs_kms, 1e-6) for p in gpts]
            median = statistics.median(values) if values else 0.0
            for point, sn in zip(gpts, values):
                if median > 0 and sn > 2 * median:
                    point.evobs_kms = max(point.evobs_kms * 0.75, 1e-6)

    velocity_noise = float(profile.get("velocity_noise_sigma", 0.0))
    if velocity_noise > 0:
        for point in pts:
            point.vobs_kms += rng.gauss(0.0, velocity_noise * max(point.evobs_kms, 1e-6))

    step = float(profile.get("discretize_velocity", 0.0))
    if step > 0:
        for point in pts:
            point.vobs_kms = round(point.vobs_kms / step) * step

    error_scale = float(profile.get("error_scale", 1.0))
    if error_scale != 1.0:
        for point in pts:
            point.evobs_kms *= max(error_scale, 1e-6)

    attenuation = float(profile.get("attenuate_outer", 0.0))
    if attenuation > 0:
        for _gal, gpts in engine.group_by_galaxy(pts).items():
            rmax = max(p.r_kpc for p in gpts)
            for point in gpts:
                if point.r_kpc > 0.7 * rmax:
                    point.evobs_kms *= 1.0 + attenuation

    return pts


def rows_from_leaderboard(results, engine) -> List[Dict[str, object]]:
    rows = engine.delta_table(results)
    rows.sort(key=lambda row: row["bic"])
    return rows


def params_by_model(results) -> Dict[str, Dict[str, float]]:
    return {result.model: dict(result.best.params) for result in results}


def margin_to_second(rows: List[Dict[str, object]]) -> float:
    if len(rows) < 2:
        return 0.0
    return float(rows[1]["delta_bic"])


def theory_from_params(engine, params: Dict[str, float]):
    p = engine.TheoryParams(
        upsilon_disk=float(params.get("upsilon_disk", 0.5)),
        upsilon_bulge=float(params.get("upsilon_bulge", 0.7)),
    )
    for name in ("L", "alpha", "a_screen", "n_screen", "rho_screen", "n_rho"):
        if name in params:
            setattr(p, name, float(params[name]))
    for name in ("nfw_A", "nfw_b", "nfw_c", "hier_A", "hier_beta", "hier_c0", "hier_gamma"):
        if name in params:
            setattr(p, name, float(params[name]))
    return p


def residual_signature(points: List[object], model: str, params: Dict[str, float], engine) -> Dict[str, object]:
    if not points:
        return {"ok": False, "reason": "no_points"}
    if model == "nfw_local":
        return {"ok": False, "reason": "nfw_local_is_descriptive_and_has_no_holdout_halos"}

    p = theory_from_params(engine, params)
    a0 = float(params.get("a0", engine.A0_RAR))
    cache = engine.gal_cache_for_model(points, p)
    rows: List[Tuple[float, float, float, float]] = []
    for point in points:
        pred = engine.predict_velocity_kms(point, model, p, cache, a0)
        sigma = engine.sigma_v(point)
        norm = (pred - point.vobs_kms) / max(sigma, 1e-9)
        frac = (pred - point.vobs_kms) / max(abs(point.vobs_kms), 1e-9)
        vbar2 = engine.baryonic_v2_kms2(point, p)
        gbar = (vbar2 * 1e6) / max(point.r_kpc * engine.KPC, 1e-9)
        rows.append((point.r_kpc, gbar, norm, frac))

    rows.sort(key=lambda row: row[0])
    mid = len(rows) // 2
    inner = rows[:mid] or rows
    outer = rows[mid:] or rows
    by_accel = sorted(rows, key=lambda row: row[1])
    low_accel = by_accel[:mid] or by_accel
    high_accel = by_accel[mid:] or by_accel

    def mean(values: List[float]) -> float:
        return sum(values) / max(1, len(values))

    norm_values = [row[2] for row in rows]
    frac_values = [row[3] for row in rows]
    inner_frac = mean([row[3] for row in inner])
    outer_frac = mean([row[3] for row in outer])
    low_frac = mean([row[3] for row in low_accel])
    high_frac = mean([row[3] for row in high_accel])
    return {
        "ok": True,
        "model": model,
        "points": len(rows),
        "rms_norm_residual": round(math.sqrt(mean([value * value for value in norm_values])), 6),
        "mean_abs_norm_residual": round(mean([abs(value) for value in norm_values]), 6),
        "mean_frac_residual": round(mean(frac_values), 6),
        "max_abs_norm_residual": round(max(abs(value) for value in norm_values), 6),
        "outer_minus_inner_frac_residual": round(outer_frac - inner_frac, 6),
        "low_minus_high_accel_frac_residual": round(low_frac - high_frac, 6),
    }


def split_heldout_by_galaxy(points: List[object], frac: float, seed: int, engine) -> Tuple[List[object], List[object], List[str]]:
    by_gal = engine.group_by_galaxy(points)
    names = sorted(by_gal)
    if len(names) < 3 or frac <= 0:
        return list(points), [], []
    rng = random.Random(seed)
    rng.shuffle(names)
    holdout_count = max(1, min(len(names) - 1, int(round(len(names) * min(frac, 0.8)))))
    holdout_names = set(names[:holdout_count])
    train: List[object] = []
    holdout: List[object] = []
    for name, gpts in by_gal.items():
        (holdout if name in holdout_names else train).extend(clone_points(gpts))
    return train, holdout, sorted(holdout_names)


def heldout_report(points: List[object], leaderboard_fn, samples: int, seed: int, engine, frac: float) -> Dict[str, object]:
    train, holdout, names = split_heldout_by_galaxy(points, frac, seed, engine)
    if not holdout:
        return {"ok": False, "reason": "heldout_disabled_or_too_few_galaxies"}
    tuned = leaderboard_fn(train, samples=samples, seed=seed)
    rows = rows_from_leaderboard(tuned, engine)
    model_params = params_by_model(tuned)
    top_model = rows[0]["model"]
    return {
        "ok": True,
        "heldout_fraction": frac,
        "heldout_galaxies": names,
        "train_points": len(train),
        "heldout_points": len(holdout),
        "train_winner": top_model,
        "train_margin_to_second_delta_bic": margin_to_second(rows),
        "heldout_residual_signature": residual_signature(holdout, top_model, model_params.get(top_model, {}), engine),
    }


def run_audit(args) -> Dict[str, object]:
    engine = load_engine(Path(args.engine))
    profiles = [p.strip() for p in args.profiles.split(",") if p.strip()]
    unknown = [p for p in profiles if p not in OBSERVER_PROFILES]
    if unknown:
        raise ValueError(f"Unknown observer profile(s): {', '.join(unknown)}")

    base_raw = engine.synth_points(truth=args.truth, n_galaxies=args.galaxies, seed=args.seed, noise=True)
    base = apply_negative_control(base_raw, args.control, stable_seed(args.seed, f"control:{args.control}"))
    leaderboard_fn = engine.leaderboard_extended if args.extended else engine.leaderboard
    results = {}

    for profile_name in profiles:
        profile = OBSERVER_PROFILES[profile_name]
        proxy_seed = stable_seed(args.seed, profile_name)
        distorted = apply_observer_proxy(base, profile, engine, proxy_seed)
        leaderboard = leaderboard_fn(distorted, samples=args.samples, seed=proxy_seed)
        model_params = params_by_model(leaderboard)
        rows = rows_from_leaderboard(leaderboard, engine)
        top_model = rows[0]["model"]
        results[profile_name] = {
            "description": profile["description"],
            "winner": top_model,
            "margin_to_second_delta_bic": margin_to_second(rows),
            "points": len(distorted),
            "galaxies": len(engine.group_by_galaxy(distorted)),
            "ranking": [row["model"] for row in rows],
            "residual_signature": residual_signature(distorted, top_model, model_params.get(top_model, {}), engine),
            "heldout_report": heldout_report(
                distorted,
                leaderboard_fn,
                samples=max(10, int(args.samples)),
                seed=stable_seed(proxy_seed, "heldout"),
                engine=engine,
                frac=float(args.heldout_frac),
            ),
            "leaderboard": rows,
        }

    winners = [entry["winner"] for entry in results.values()]
    counts = Counter(winners)
    top_model, top_count = counts.most_common(1)[0]
    margins = [float(entry["margin_to_second_delta_bic"]) for entry in results.values()]
    rankings = [tuple(entry["ranking"]) for entry in results.values()]
    ranking_counts = Counter(rankings)
    _top_ranking, top_ranking_count = ranking_counts.most_common(1)[0]
    return {
        "status": "LOCAL_RESEARCH_EVIDENCE",
        "truth": args.truth,
        "control": args.control,
        "engine": str(Path(args.engine).resolve()),
        "galaxies": args.galaxies,
        "samples": args.samples,
        "extended": bool(args.extended),
        "profiles": profiles,
        "results": results,
        "stability": {
            "winner_counts": dict(counts),
            "most_invariant": top_model,
            "winner_rate": top_count / max(1, len(profiles)),
            "mean_margin_to_second_delta_bic": sum(margins) / max(1, len(margins)),
            "rank_stability": top_ranking_count / max(1, len(rankings)),
        },
        "claim_boundary": [
            "Synthetic observer/proxy audit only.",
            "Not proof of physics, cosmology, consciousness or real-world prediction.",
            "Proxy transformations are masks over data, not new instrument measurements.",
            "Negative controls are expected to break claims; survival under a broken control is a bias warning.",
        ],
    }


def run_selftest(args) -> Dict[str, object]:
    base_args = argparse.Namespace(
        engine=args.engine,
        truth="rar",
        galaxies=args.galaxies,
        samples=args.samples,
        seed=args.seed,
        profiles="instrument_balanced,scientific_community,adversarial_observer",
        extended=False,
        control="none",
        heldout_frac=args.heldout_frac,
    )
    control_args = argparse.Namespace(
        engine=args.engine,
        truth="rar",
        galaxies=args.galaxies,
        samples=args.samples,
        seed=args.seed,
        profiles="instrument_balanced,scientific_community,adversarial_observer",
        extended=False,
        control="shuffled_baryons",
        heldout_frac=args.heldout_frac,
    )
    normal = run_audit(base_args)
    shuffled = run_audit(control_args)
    checks = {
        "normal_has_winner": bool(normal["stability"]["most_invariant"]),
        "normal_has_margins": "mean_margin_to_second_delta_bic" in normal["stability"],
        "shuffled_has_winner": bool(shuffled["stability"]["most_invariant"]),
        "control_changed_or_reported": shuffled["control"] == "shuffled_baryons",
    }
    return {
        "status": "LOCAL_SELFTEST",
        "ok": all(checks.values()),
        "checks": checks,
        "normal": normal["stability"],
        "shuffled_baryons": shuffled["stability"],
        "claim_boundary": [
            "Selftest validates code paths only.",
            "It is not physics evidence and not a publication gate.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Observacionismo Lab observer/proxy audit")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo")
    demo.add_argument("--engine", default=str(DEFAULT_ENGINE))
    demo.add_argument("--truth", default="rar", choices=["rar", "psichi", "psichi_weak", "pop_nfw", "mixed"])
    demo.add_argument("--galaxies", type=int, default=6)
    demo.add_argument("--samples", type=int, default=80)
    demo.add_argument("--seed", type=int, default=42)
    demo.add_argument("--profiles", default="visual_proxy,component_split_proxy,instrument_balanced")
    demo.add_argument("--control", default="none", choices=CONTROL_MODES)
    demo.add_argument("--heldout-frac", type=float, default=0.0)
    demo.add_argument("--extended", action="store_true")
    demo.add_argument("--out", default="")

    selftest = sub.add_parser("selftest")
    selftest.add_argument("--engine", default=str(DEFAULT_ENGINE))
    selftest.add_argument("--galaxies", type=int, default=5)
    selftest.add_argument("--samples", type=int, default=40)
    selftest.add_argument("--seed", type=int, default=42)
    selftest.add_argument("--heldout-frac", type=float, default=0.2)
    selftest.add_argument("--out", default="")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    payload = run_selftest(args) if args.command == "selftest" else run_audit(args)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
