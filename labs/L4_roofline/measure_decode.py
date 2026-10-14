"""Measure prefill vs decode on CPU with a tiny open model (complete; do not edit).

Run: uv run python labs/L4_roofline/measure_decode.py
First run downloads Qwen2.5-0.5B-Instruct (~1 GB). Predict BEFORE running:
  1. Is time-per-output-token roughly constant as the prompt gets longer? (decode)
  2. Does time-to-first-token grow roughly linearly with prompt length? (prefill)
  3. What tokens/s would bandwidth_GBps*1e9 / model_bytes predict for your RAM?
"""
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

NAME = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(NAME)
model = AutoModelForCausalLM.from_pretrained(NAME, torch_dtype=torch.float32).eval()
param_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
print(f"weights: {param_bytes/1e9:.2f} GB")

base = "The quick brown fox jumps over the lazy dog. " * 4
for reps in [1, 4, 16, 64]:
    ids = tok(base * reps, return_tensors="pt").input_ids
    with torch.no_grad():
        t0 = time.perf_counter()
        out = model(ids, use_cache=True)
        ttft = time.perf_counter() - t0  # prefill: whole prompt in one pass
        past, nxt = out.past_key_values, out.logits[:, -1:].argmax(-1)
        t0 = time.perf_counter()
        n = 16
        for _ in range(n):  # decode: one token at a time, reading weights + growing KV cache
            out = model(nxt, past_key_values=past, use_cache=True)
            past, nxt = out.past_key_values, out.logits[:, -1:].argmax(-1)
        tpot = (time.perf_counter() - t0) / n
    print(f"prompt {ids.shape[1]:5d} tok | TTFT {ttft*1e3:8.1f} ms | TPOT {tpot*1e3:7.1f} ms | implied weight BW {param_bytes/tpot/1e9:6.1f} GB/s")
