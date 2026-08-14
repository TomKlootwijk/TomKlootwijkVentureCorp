#!/usr/bin/env python3
"""Monte Carlo illustration of AA+BB step-growth polymerization.

The model is deliberately idealized: bifunctional units, no rings, no branching, and
random reaction of complementary chain ends. It demonstrates how a small stoichiometric
imbalance caps the number-average chain length. It is not a molecular simulation of
SE301717B.
"""
from __future__ import annotations
import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def theoretical_xn(r: float, p: float) -> float:
    return (1 + r) / (1 + r - 2 * r * p)


def simulate(n_limiting: int, r: float, conversion: float, seed: int = 7):
    """Graph-free chain-merging model using counts of A- and B-terminated chains."""
    rng = random.Random(seed)
    n_a = n_limiting
    n_b = max(1, round(n_limiting / r)) if r < 1 else n_limiting
    chains = [[1, "A", "A"] for _ in range(n_a)] + [[1, "B", "B"] for _ in range(n_b)]
    target = int(round(2 * n_a * conversion))
    reactions = 0
    while reactions < target:
        a_idx = [i for i, c in enumerate(chains) if c[1] == "A" or c[2] == "A"]
        b_idx = [i for i, c in enumerate(chains) if c[1] == "B" or c[2] == "B"]
        if not a_idx or not b_idx:
            break
        i = rng.choice(a_idx)
        j = rng.choice(b_idx)
        if i == j:
            continue
        c1, c2 = chains[i], chains[j]
        # consume one complementary end and join chains; retain the two unconsumed ends
        ends1 = [c1[1], c1[2]]
        ends2 = [c2[1], c2[2]]
        try:
            ends1.remove("A")
            ends2.remove("B")
        except ValueError:
            continue
        new = [c1[0] + c2[0], ends1[0], ends2[0]]
        for k in sorted((i, j), reverse=True):
            chains.pop(k)
        chains.append(new)
        reactions += 1
    lengths = [c[0] for c in chains]
    return lengths, reactions


def main():
    rows = []
    ratios = [1.0, 0.99, 0.98, 0.97]
    conversions = [0.95, 0.98, 0.99, 0.995]
    for r in ratios:
        for p in conversions:
            lengths, rx = simulate(2500, r, p, seed=int(r*10000+p*1000))
            xn_sim = sum(lengths) / len(lengths)
            rows.append({"r": r, "conversion": p, "theoretical_Xn": theoretical_xn(r, p), "simulated_mean_chain_units": xn_sim, "reactions": rx})
    with (OUT / "polymer_step_growth_results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for r in ratios:
        xs = [p for p in conversions]
        ys = [next(z["theoretical_Xn"] for z in rows if z["r"] == r and z["conversion"] == p) for p in xs]
        ax.plot(xs, ys, marker="o", label=f"r={r:.2f}")
    ax.set_xlabel("Limiting-function conversion p")
    ax.set_ylabel("Ideal number-average degree Xn")
    ax.set_title("Conversion and stoichiometric balance jointly control chain length")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "polymer_step_growth_results.png", dpi=200)

if __name__ == "__main__":
    main()
