"""Memory locality experiment (complete; do not edit). Write your prediction first.

Predict: summing a C-order 8192x8192 float32 array by rows vs by columns. Ratio of times?
Run: uv run python labs/L1_systems/stride_bench.py
"""
import time

import numpy as np

n = 8192
a = np.random.rand(n, n).astype(np.float32)


def timeit(f, reps=3):
    best = 1e9
    for _ in range(reps):
        t = time.perf_counter()
        f()
        best = min(best, time.perf_counter() - t)
    return best


def by_rows():
    return sum(a[i, :].sum() for i in range(n))


def by_cols():
    return sum(a[:, j].sum() for j in range(n))


r, c = timeit(by_rows), timeit(by_cols)
print(f"rows: {r*1e3:8.1f} ms   cols: {c*1e3:8.1f} ms   cols/rows = {c/r:.1f}x")
print("Why? Row slice touches consecutive 64B cache lines; column slice touches one float per line.")
