"""L4 Roofline lab. Run: uv run pytest labs/L4_roofline -q

Then run measure_decode.py and compare to your own prediction.
"""


def matmul_cost(m: int, n: int, k: int, dtype_bytes: int = 2) -> tuple:
    """(FLOPs, bytes moved) for C[m,n] = A[m,k] @ B[k,n]: read A and B once, write C once."""
    raise NotImplementedError  # TODO


def intensity(flops: float, bytes_moved: float) -> float:
    """FLOPs per byte."""
    raise NotImplementedError  # TODO


def ridge(peak_flops: float, bandwidth: float) -> float:
    """Intensity at which an op switches from memory-bound to compute-bound."""
    raise NotImplementedError  # TODO


def bound(flops: float, bytes_moved: float, peak_flops: float, bandwidth: float) -> str:
    """Return 'compute' or 'memory'."""
    raise NotImplementedError  # TODO


def decode_tps_ceiling(param_bytes: float, bandwidth: float, kv_bytes_per_seq: float = 0.0, batch: int = 1) -> float:
    """Upper bound on total tokens/s for batched decode:
    batch * bandwidth / (batch * kv_bytes_per_seq + param_bytes)   (weights are read once per step, KV once per sequence)."""
    raise NotImplementedError  # TODO


if __name__ == "__main__":
    # Fill in your own table once the functions work: model, dtype, GPU -> tokens/s ceiling.
    H100_BW = 3.35e12
    for name, params in [("7B fp16", 14e9), ("7B int4", 3.5e9), ("70B int4", 35e9)]:
        print(name, round(decode_tps_ceiling(params, H100_BW), 1), "tok/s (batch 1)")
