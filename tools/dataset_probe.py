#!/usr/bin/env python3
"""Probe the G1 "lite" Humanoid Everyday episodes.

Measures what the diagnostic design depends on: the layout of `action`, how
much the legs move, how far the arms lag their commands, and how large the
nominal tracking residual is. The numbers quoted in the documentation
(docs/overview/dataset.md) come from this script.

Usage:
    pip install numpy pyarrow
    python tools/dataset_probe.py --episodes 40 --seed 7 --cache .cache/he
"""
from __future__ import annotations

import argparse
import json
import random
import urllib.request
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

BASE = "https://huggingface.co/datasets/USC-GVL/Humanoid-Everyday-G1/resolve/main"
ARM = ["L_ShoulderPitch", "L_ShoulderRoll", "L_ShoulderYaw", "L_Elbow", "L_WristRoll",
       "L_WristPitch", "L_WristYaw", "R_ShoulderPitch", "R_ShoulderRoll", "R_ShoulderYaw",
       "R_Elbow", "R_WristRoll", "R_WristPitch", "R_WristYaw"]
MAX_LAG = 30  # frames, i.e. 1 s at 30 Hz


def fetch(url: str, dest: Path) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
    return dest


def best_lag(cmd: np.ndarray, meas: np.ndarray) -> int:
    """Lag, in frames, that minimises the mean absolute residual over all arm joints."""
    costs = [np.abs(cmd[: len(cmd) - k] - meas[k:]).mean() for k in range(MAX_LAG + 1)]
    return int(np.argmin(costs))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=40)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--cache", type=Path, default=Path(".cache/he"))
    args = ap.parse_args()

    info = json.loads(fetch(f"{BASE}/meta/info.json", args.cache / "info.json").read_text())
    print(f"dataset: {info['total_episodes']} episodes, {info['total_frames']} frames, "
          f"{info['total_tasks']} tasks, {info['fps']} fps")
    print("features:", ", ".join(info["features"]))

    ids = random.Random(args.seed).sample(range(info["total_episodes"]), args.episodes)
    lags, raw_p95, comp_p95, leg_ranges, arm_ranges, tasks, durations = [], [], [], [], [], set(), []
    residuals, head_vs_arm, tail_vs_arm, nans, jitter = [], [], [], 0, []

    for ep in ids:
        chunk = ep // info["chunks_size"]
        path = fetch(f"{BASE}/data/chunk-{chunk:03d}/episode_{ep:06d}.parquet",
                     args.cache / f"episode_{ep:06d}.parquet")
        t = pq.read_table(path)
        arm = np.array(t["observation.arm_joints"].to_pylist())
        leg = np.array(t["observation.leg_joints"].to_pylist())
        act = np.array(t["action"].to_pylist())
        ts = np.array(t["timestamp"].to_pylist())
        assert arm.shape[1] == 14 and leg.shape[1] == 15 and act.shape[1] == 28, (arm.shape, leg.shape, act.shape)

        head_vs_arm.append(np.abs(act[:, :14] - arm).mean())
        tail_vs_arm.append(np.abs(act[:, 14:] - arm).mean())
        cmd = act[:, 14:]  # layout confirmed by the two lines above
        lag = best_lag(cmd, arm)
        comp = np.abs(cmd[: len(cmd) - lag] - arm[lag:])
        raw_p95.append(np.percentile(np.abs(cmd - arm), 95))
        comp_p95.append(np.percentile(comp, 95))
        residuals.append(comp)
        lags.append(lag)
        leg_ranges.append(np.ptp(leg, axis=0).max())
        arm_ranges.append(np.ptp(arm, axis=0).max())
        tasks.add(t["task_index"][0].as_py())
        durations.append(float(ts[-1]))
        jitter.append(float(np.diff(ts).std()))
        nans += int(np.isnan(arm).sum() + np.isnan(leg).sum() + np.isnan(act).sum())

    def q(values, name, unit=""):
        v = np.array(values)
        print(f"{name:42s} min {v.min():.3f}  p50 {np.median(v):.3f}  p90 {np.percentile(v, 90):.3f}  max {v.max():.3f} {unit}")

    print(f"\nsample: {len(ids)} episodes from {len(tasks)} tasks, seed {args.seed}, {sum(durations) / 60:.1f} min")
    print(f"action layout: |a[:14]-arm| = {np.mean(head_vs_arm):.3f} rad, |a[14:]-arm| = {np.mean(tail_vs_arm):.3f} rad "
          "(so action = hand[14] + arm[14])")
    print(f"NaN values: {nans};  timestamp jitter max: {max(jitter):.6f} s (LeRobot timestamps are synthetic)\n")
    q(lags, "arm command-to-measure lag per episode", "frames")
    q(raw_p95, "arm residual p95, no lag compensation", "rad")
    q(comp_p95, "arm residual p95, lag compensated", "rad")
    q(arm_ranges, "largest arm joint range per episode", "rad")
    q(leg_ranges, "largest leg/waist joint range per episode", "rad")
    print(f"episodes with a leg/waist joint range above 0.2 rad: {sum(r > 0.2 for r in leg_ranges)}/{len(ids)}")

    pooled = np.concatenate(residuals)
    print("\nper-joint lag-compensated residual p95 / p99 (rad):")
    for j, name in enumerate(ARM):
        print(f"  {name:18s} {np.percentile(pooled[:, j], 95):.3f} / {np.percentile(pooled[:, j], 99):.3f}")


if __name__ == "__main__":
    main()
