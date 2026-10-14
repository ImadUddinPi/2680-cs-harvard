import torch
import torch.nn.functional as F

import lab


def test_attention_matches_reference():
    torch.manual_seed(0)
    q, k, v = (torch.randn(7, 16) for _ in range(3))
    ref = F.scaled_dot_product_attention(q[None], k[None], v[None], is_causal=True)[0]
    assert torch.allclose(lab.causal_attention(q, k, v), ref, atol=1e-5)


def test_attention_is_causal():
    torch.manual_seed(1)
    q, k, v = (torch.randn(5, 8) for _ in range(3))
    out1 = lab.causal_attention(q, k, v)
    v2 = v.clone()
    v2[4] += 100.0  # change only the LAST token's value
    out2 = lab.causal_attention(q, k, v2)
    assert torch.allclose(out1[:4], out2[:4], atol=1e-6)  # earlier outputs cannot change


def test_kv_sizes():
    assert lab.kv_bytes_per_token(32, 32, 128, 2) == 524_288
    # Llama-2-13B style: 40 layers, 40 kv heads, 128 dim, bf16, 8192 tokens ~ 6.25 GiB (6.7e9 bytes)
    assert abs(lab.kv_cache_gib(40, 40, 128, 2, 8192) - 6.25) < 0.01
    # GQA with 8 kv heads is 5x smaller
    assert abs(lab.kv_cache_gib(40, 8, 128, 2, 8192) - 1.25) < 0.01
    assert abs(lab.kv_cache_gib(32, 32, 128, 2, 4096, batch=4) - 8.0) < 0.01
