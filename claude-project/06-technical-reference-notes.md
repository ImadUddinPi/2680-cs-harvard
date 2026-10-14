# Technical reference notes (lesson content, precise, no analogies)

Use these as the ground truth when explaining or assessing. Teach from these; do not add metaphors.

## 1. Systems (lesson L1)
**Process vs thread.** A process has its own virtual address space. Threads in one process share the address space (heap, globals, code, open files) and each has its own stack, registers and program counter.
**fork().** Creates a child with a copy of the parent's virtual address space. Physical pages are shared read-only (copy-on-write). A write to a shared page triggers a page fault; the kernel allocates a new page, copies the data, maps it writable for the writer. Cost of fork is proportional to page-table size, not memory size.
**Virtual memory.** Per-process page table maps virtual pages to physical frames. The TLB caches translations. TLB miss: translation not cached, hardware or kernel walks the page table (page may be resident). Page fault: page not mapped or not resident; kernel handles it (allocate, load from disk, copy-on-write, or signal SIGSEGV).
**Caches.** Lines are 64 bytes. Sequential access touches each line once. Compulsory misses = ceil(bytes / 64). Row-major array: row traversal is stride-1 (cache-friendly); column traversal strides by row length (one useful element per line, poor locality).
**Concurrency.** Race condition: result depends on interleaving of unsynchronized accesses with at least one write. `counter += 1` is load, add, store, so updates can be lost; final value of two threads x n increments lies between 2 and 2n in the worst case. Fixes: mutex around the critical section; atomic fetch-add; per-thread local counters combined at the end. Deadlock needs: mutual exclusion, hold-and-wait, no preemption, circular wait; prevent by a global lock order. Starvation: a task is indefinitely denied a resource. False sharing: independent variables on one cache line cause coherence traffic.
**Amdahl.** speedup(N) = 1 / ((1 - p) + p / N), limit 1 / (1 - p).
**Python GIL.** One thread executes Python bytecode at a time in standard CPython. CPU-bound threads do not speed up; I/O-bound threads do. Use multiprocessing or native code releasing the GIL.

## 2. PyTorch (lesson L2)
**Tensor = storage + (shape, strides, offset).** view/transpose/slicing change metadata only and share storage. `contiguous()` copies into row-major. `view` requires compatible strides (fails on non-contiguous tensors); `reshape` returns a view if possible, otherwise copies.
**Broadcasting.** Align shapes from the right; pad with 1s on the left; each dimension must be equal or one of them 1. (8,1,5) + (3,1) -> (8,3,5).
**Autograd.** `loss.backward()` runs reverse-mode autodiff and accumulates dLoss/dParam into `.grad` (adds to existing values). `optimizer.zero_grad()` clears them. Calling backward twice on `(3*w).sum()` with w=2 gives grad 6 (3 + 3). Gradient accumulation: divide loss by k, step every k micro-batches.
**eval vs no_grad.** `model.eval()` changes layer behavior (dropout off, batch norm uses running stats). `torch.no_grad()` stops graph recording, so activations are not stored (lower memory).
**Training loop.** forward, loss, backward, step, zero_grad. A learning rate that is too high with accumulated gradients diverges.

## 3. Transformers and KV cache (lesson L3)
**Attention.** For tokens x (T x d_model): Q = x Wq, K = x Wk, V = x Wv. out = softmax(Q K^T / sqrt(d_k) + mask) V. Causal mask sets scores for j > i to -inf before softmax. Division by sqrt(d_k) keeps score variance near 1.
**Cost.** The score matrix is T x T, so attention compute and (without fused kernels) memory are O(T^2). FFN cost is O(T).
**KV cache.** Store K and V of all previous tokens per layer. bytes per token = 2 x layers x kv_heads x head_dim x dtype_bytes. Example 32 layers, 32 heads, 128 dim, fp16: 524,288 B/token; 4,096 tokens = 2 GiB per sequence. Llama-2-13B style (40 layers, 40 heads, 128, bf16): 819,200 B/token; 8,192 tokens = 6.25 GiB. GQA with 8 KV heads divides this by 5 (40/8).
**Prefill vs decode.** Prefill processes all prompt tokens in parallel (matrix-matrix, compute-bound) and fills the cache; TTFT depends on it. Decode generates one token per step (matrix-vector, reads all weights and the KV cache per token, memory-bound); time per output token (TPOT) depends on bytes read. Without a cache, each step recomputes K,V for all earlier tokens.
**Sampling.** Temperature T divides logits before softmax; T -> 0 approaches greedy argmax.

## 4. Roofline and performance arithmetic (lesson L4)
**Definitions.** Arithmetic intensity I = FLOPs / bytes moved. Ridge point = peak FLOP/s / memory bandwidth. If I < ridge the op is memory-bound; otherwise compute-bound.
**Matmul C[m,n] = A[m,k] B[k,n].** FLOPs = 2mnk. Bytes (dtype b) = (mk + kn + mn) b. For n x n x n fp16: intensity = n/3 FLOP/byte (4096 -> 1365).
**Example ridge.** 1,000 TFLOP/s and 3 TB/s -> ridge 333 FLOP/byte. H100-class compute-bound batch is roughly 280 tokens (JAX Scaling Book).
**Decode ceiling.** tokens/s (batch B) <= B x BW / (B x KV_bytes_per_seq + weight_bytes). Batch 1, 7B fp16 (14 GB) at 2 TB/s: 143 tok/s; 4-bit weights (3.5 GB) -> 571 tok/s. Batching raises throughput because weights are read once per step for all sequences; KV traffic grows per sequence.
**Latency stats.** Report p50 and p99. Probability that at least one of n independent calls falls in the slowest 1%: 1 - 0.99^n (n=50 -> 0.395, n=30 -> 0.260).
**Goodput.** Requests per second that meet the TTFT and TPOT SLOs, not raw throughput.

## 5. Agent loop, tokens and cost (lessons L5, M00A)
**Model call.** Stateless: (messages, tool definitions) -> one assistant message (text, or tool call with name and JSON input). The API does not execute tools.
**Loop.** messages = [user task]; repeat: call model; append reply; if no tool call return text; else run each tool in the harness, append tool_result; stop at a step cap. Harness responsibilities: execution, argument validation, errors (return "ERROR: ..." observations, never crash), timeouts, retry policy (idempotent only), permissions, step limit, usage accounting.
**Billing.** Input tokens on call k = all tokens currently in messages. With c new tokens per call and call 1 sending c: input_k = c x k; total over n calls = c x n(n+1)/2 (quadratic in n). 10 calls x 2,000: 110,000 tokens; at $3/M = $0.33. Output tokens are billed separately at a higher rate (example $3 in / $15 out per M: 10k in + 1k out = $0.030 + $0.015 = $0.045).
**Prompt caching.** A byte-identical prefix can be read at a discount (reads about 5-10% of input price, writes about 125%). Any change early in the prompt invalidates everything after it. With caching, per call: new tokens written, earlier tokens read. 10 x 2,000 at $3/M with write 125% and read 10%: $0.102 vs $0.33. Keep system prompt and tool list byte-identical; order tools deterministically; MCP spec 2026-07-28 requires deterministic tool-list ordering for this reason.
**Context engineering (Anthropic).** Compaction (summarize near the limit, tune recall first), clear stale tool results, notes file outside context, sub-agents returning 1-2k token summaries, just-in-time retrieval, minimal non-overlapping tools.
**Reliability.** Per-step success p over n steps gives p^n (0.95^10 = 0.60; 0.90^10 = 0.35). pass^k = probability all k trials succeed. Verification must be independent of the generator.
**Security.** Indirect prompt injection: instructions hidden in data the agent reads. Lethal trifecta: private data + untrusted content + external communication. Rule of Two: unsupervised agents hold at most two. Treat configs, skills and MCP servers as executable code.

## 6. Tooling (lesson L6)
git: `git switch -c b`, `git reset --soft HEAD~1` (keep changes staged), `--hard` (discard), `git revert` (new inverse commit). SSH: `ssh -L local:localhost:remote user@host` forwards a local port. Slurm: `srun --partition=P --gres=gpu:1 --time=HH:MM:SS --pty bash` interactive shell; `sbatch script.sh` queued batch job; `squeue`, `scancel`. Always release GPUs and stop rented instances.

## 7. Serving concepts for Part II (reference; not yet taught)
Continuous batching (iteration-level scheduling), PagedAttention (KV in fixed-size blocks, like paging), chunked prefill, prefix caching / RadixAttention, prefill-decode disaggregation (separate pools, KV transfer), speculative decoding (draft proposes, target verifies; distribution-preserving via accept/reject), quantization (FP8, FP4, AWQ, GPTQ), KV offload, cache-aware routing. Engines: learn vLLM first, then SGLang; Dynamo and llm-d are cluster layers. Honest benchmarking: TTFT and TPOT p50/p99, goodput at an SLO, throughput vs per-user interactivity, realistic prompt lengths, prefix caching on/off deliberately, accuracy after quantization, pinned versions, cost per million tokens.
