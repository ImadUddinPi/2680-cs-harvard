# Lab specifications and review rubric

The student implements TODO functions in `labs/<L>/...`; pytest tests are the spec. The tutor does not write the student's solution. Use this file to review code the student pastes: check each behavior below and ask technical questions about the gaps. Official assignments A1-A5 are the student's own work: explain concepts, review, do not write submissions.

## L1 systems (labs/L1_systems/lab.py)
- `cold_misses(n_elems, elem_bytes, line_bytes=64)` = ceil(n_elems x elem_bytes / line_bytes). Tests: 1,048,576 x 4 -> 65,536; 1000 x 8 -> 125; 65 x 1 -> 2.
- `amdahl(p, cores)` = 1 / ((1-p) + p/cores). Tests: (0.9, 10) -> 5.263; limit 10; p=0 -> 1.
- `racy_total(n_threads, n_incr)`: shared Counter, each increment is read, `time.sleep(0)`, write read+1, no lock; must lose updates (result < n_threads x n_incr).
- `locked_total`: same workload with threading.Lock; must equal n_threads x n_incr. `sharded_total`: per-thread local counts summed at the end.
- Given: stride_bench.py (row vs column sum timing; student predicts the ratio first), cow_demo.py (needs WSL for fork).

## L2 PyTorch (labs/L2_pytorch/lab.py)
- `broadcast_shape(a, b)` without torch; ValueError when incompatible. (8,1,5),(3,1) -> (8,3,5).
- `shares_memory(x, y)`: compare underlying storage (untyped_storage().data_ptr()).
- `flatten_transposed(x)`: x.T flattened in logical order for non-contiguous x.T (use reshape or contiguous().view). arange(6).reshape(2,3) -> [0,3,1,4,2,5].
- `sgd_losses(zero_grad, steps=50, lr=0.2)`: nn.Linear(1,1), manual_seed(0), SGD, MSE on y = 3x+1, x = linspace(-1,1,32).unsqueeze(1). With zero_grad the final loss < 0.01; without it > 0.1.
- `grad_after_two_backwards()` -> 6.0 (retain_graph=True on the first backward).

## L3 transformer (labs/L3_transformer/lab.py)
- `causal_attention(q, k, v)` for (T, d): scores = q k^T / sqrt(d); mask j > i to -inf BEFORE softmax; softmax over last dim; times v. Must match F.scaled_dot_product_attention(is_causal=True) within 1e-5 and be causal (changing the last value row cannot change earlier outputs).
- `kv_bytes_per_token(layers, kv_heads, head_dim, dtype_bytes)` = 2 x product. (32,32,128,2) -> 524,288.
- `kv_cache_gib(..., tokens, batch=1)` = bytes/token x tokens x batch / 2^30. (40,40,128,2, 8192) -> 6.25; GQA 8 heads -> 1.25; (32,32,128,2, 4096, batch 4) -> 8.0.

## L4 roofline (labs/L4_roofline/roofline.py)
- `matmul_cost(m, n, k, dtype_bytes=2)` -> (2mnk, (mk + kn + mn) x dtype_bytes).
- `intensity(flops, bytes)`, `ridge(peak_flops, bandwidth)`, `bound(flops, bytes, peak, bw)` -> 'compute' or 'memory' (intensity >= ridge is compute).
- `decode_tps_ceiling(param_bytes, bandwidth, kv_bytes_per_seq=0, batch=1)` = batch x bandwidth / (batch x kv_bytes_per_seq + param_bytes). Tests: (14e9, 2e12) -> 142.857; batch 16 with kv 2e9 -> 695.65; 4x faster for 4x smaller weights.
- Given: measure_decode.py measures TTFT/TPOT of Qwen2.5-0.5B on CPU at several prompt lengths and reports implied weight bandwidth. The student predicts before running.

## L5 agent loop (labs/L5_agent/agent.py), skeleton of Assignment 2
`run_agent(model, tools, task, max_steps=8)` returns {"final", "steps", "usage": {"in","out"}, "stopped": "final"|"max_steps"}. Model returns {"type": "tool_call", name, args, usage} or {"type": "final", text, usage}.
Behaviors under test: messages start with the user task; tool observation appended as {"role":"tool","name":..., "content": str(result)}; unknown tool, bad arguments and tool exceptions produce an observation beginning "ERROR:" (loop continues); usage summed over every model call; stop at first final; after max_steps model calls with no final return final None and stopped "max_steps"; `cost_usd(usage, price_in_per_m, price_out_per_m)` (10,000 in + 1,000 out at 3 and 15 -> 0.045).
Review questions for a student's solution: Where does the step counter increment? What happens if the tool returns a non-string? Is the assistant call recorded in messages before the observation? Can a malformed `args` crash the loop? Which exceptions are caught and why not a bare except?

## Live run (not required for M00A mastery, needed for A2)
A 40-line `live_run.py` wires a real model API, prints a per-step table of input tokens, output tokens and dollar cost, and shows input tokens growing each turn; then add a cache breakpoint and measure the change.
