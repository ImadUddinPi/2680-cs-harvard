"""L3 Transformer lab. Run: uv run pytest labs/L3_transformer -q"""
import torch


def causal_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """Single-head causal self-attention. q, k, v: (T, d). Return (T, d).

    softmax(q k^T / sqrt(d)) v, where position i may only attend to positions <= i.
    Do not call F.scaled_dot_product_attention; the test does that to check you.
    """
    raise NotImplementedError  # TODO


def kv_bytes_per_token(layers: int, kv_heads: int, head_dim: int, dtype_bytes: int) -> int:
    """Bytes of KV cache added per generated token (keys AND values)."""
    raise NotImplementedError  # TODO


def kv_cache_gib(layers: int, kv_heads: int, head_dim: int, dtype_bytes: int, tokens: int, batch: int = 1) -> float:
    """KV cache size in GiB (2**30 bytes) for `batch` sequences of `tokens` tokens."""
    raise NotImplementedError  # TODO
