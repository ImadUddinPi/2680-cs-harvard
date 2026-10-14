# Assessment bank, form B (fresh questions for the M00 retest and spot checks)

USE: tutor-only, contains answers. Same skills and point weights as form A (MC 1, numeric 2 within 3%, short 3 by rubric). Total 56 points. Never show answers before grading. Do not reuse a question once it has been asked; write new variants with the same structure.

## Section A. Systems (12 pts)
**B-A1 (short, 3).** A parent calls fork(), then the child writes to a heap page that both processes map. Describe what the kernel does, step by step.
Key: after fork both map the same physical pages read-only (copy-on-write). The write causes a page fault on a write-protected page. The kernel allocates a new physical page, copies the contents, maps the copy writable into the child, and resumes. The parent's mapping is unchanged. Rubric: 1 shared read-only mapping; 1 page fault on write; 1 copy and remap for the writer only.

**B-A2 (numeric, 2).** 2,097,152 doubles (8 bytes each) are summed sequentially; 64-byte lines; cold cache. Compulsory misses?
Key: 2,097,152 x 8 / 64 = 262,144.

**B-A3 (numeric, 2).** 80% of runtime parallelizes perfectly. Speedup on 16 cores? Key: 1/(0.2 + 0.8/16) = 4.00.

**B-A4 (short, 3).** Give a two-lock deadlock between two threads and one fix.
Key: T1 takes lock A then B; T2 takes B then A; each holds one and waits for the other. Fix: impose a global lock order (always A before B), or use try-lock with back-off, or one coarser lock. Rubric: 1 circular wait example; 1 identify the cause (inconsistent lock order, hold-and-wait); 1 valid fix.

**B-A6 (MC, 1).** A page fault differs from a TLB miss in that: (a) a page fault means the translation was not cached; (b) a page fault means the page is not mapped or resident and the kernel must handle it, while a TLB miss only needs a page-table walk; (c) they are the same event; (d) a page fault only happens on writes. Key: b.

**B-A5 (MC, 1).** Which pair is a data race? (a) two threads read a shared int; (b) one thread writes a shared int while another reads it, no synchronization; (c) two threads write to separate arrays; (d) two threads each lock the same mutex around their writes. Key: b.

## Section B. Python and PyTorch (9 pts)
**B-B1 (MC, 1).** `torch.ones(5,1,4) + torch.ones(3,4)` has shape: (a) (5,3,4) (b) (5,1,4) (c) (3,5,4) (d) error. Key: a.

**B-B2 (short, 3).** `x = torch.arange(12).reshape(3,4); y = x[:,1]; y[0] = 100; print(x[0,1], y.is_contiguous())` Output and why.
Key: `100 False`. Slicing returns a view sharing storage with x, so writing y changes x. Column slice has stride 4, so it is not contiguous. Rubric: 1 value 100; 1 view shares storage; 1 non-contiguous because stride is 4.

**B-B3 (short, 3).** You want an effective batch of 32 but memory fits 8. Describe the loop using gradient accumulation, including how the loss is scaled and when step() and zero_grad() are called.
Key: loop over micro-batches of 8; loss = criterion(...) / 4; loss.backward() each micro-batch (grads accumulate in .grad); after every 4 micro-batches call optimizer.step() then optimizer.zero_grad(). Rubric: 1 accumulate via repeated backward; 1 divide loss by 4 (or equivalent); 1 step and zero_grad every 4.

**B-B4 (MC, 1).** What does `torch.no_grad()` change? (a) switches dropout off (b) stops autograd recording, so activations are not kept for backward and memory drops (c) moves tensors to CPU (d) disables training mode only. Key: b.

**B-B5 (MC, 1).** Two Python threads each run pure-Python CPU-bound loops (CPython with GIL). Speed versus one thread: (a) 2x (b) about the same (c) 2x slower always (d) crash. Key: b.

## Section C. Transformers and inference (13 pts)
**B-C1 (numeric, 2).** KV cache bytes per token: 28 layers, 4 KV heads, head dim 128, bf16. Key: 2 x 28 x 4 x 128 x 2 = 57,344 B.

**B-C2 (numeric, 2).** KV cache for batch 16, 8,192 tokens each, same model. Key: 57,344 x 8,192 x 16 = 7,516,192,768 B = 7.0 GiB (7.52 GB).

**B-C3 (short, 3).** What is recomputed at each decoding step without a KV cache, and how does total cost scale with output length?
Key: all earlier tokens' keys and values (and hidden states) in every layer are recomputed from scratch by running the full sequence; per-step cost grows with current length, total cost over n steps grows about n^2 for the dense layers (attention part about n^3). With the cache each step processes one new token and attends to cached K,V. Rubric: 1 recompute all prior K,V; 1 per-step cost grows with length; 1 total grows superlinearly / cache removes it.

**B-C4 (MC, 1).** Why divide attention scores by sqrt(d_k)? Key: keep the variance of the dot products near 1 so softmax does not saturate (tiny gradients). Distractors: speed, causal masking, normalization of weights to sum 1.

**B-C5 (MC, 1).** Grouped-query attention reduces: (a) parameters of the FFN (b) KV cache size by sharing K,V heads across query heads (c) vocabulary size (d) number of layers. Key: b.

**B-C6 (short, 3).** Why does prefill reach higher GPU utilization than batch-1 decode? Key: prefill multiplies matrices by matrices (all prompt tokens at once), reusing each weight byte many times, so intensity is high and it is compute-bound; decode at batch 1 is matrix-vector, reading all weights per token with about 1 FLOP per byte, so it is memory-bandwidth-bound. Rubric: 1 matrix-matrix vs matrix-vector; 1 arithmetic intensity / weight reuse; 1 names compute-bound vs memory-bound correctly.

**B-C7 (MC, 1).** Which part of a transformer layer costs O(n^2) in sequence length n? (a) the feed-forward network (b) the attention score matrix QK^T (c) the embedding lookup (d) layer norm. Key: b.

## Section D. Performance arithmetic (8 pts)
**B-D1 (numeric, 2).** Decode ceiling, 13B fp16 (26 GB), 3.35 TB/s, batch 1. Key: 3.35e12 / 26e9 = 128.8 tok/s.

**B-D2 (numeric, 2).** Same model with 8-bit weights (13 GB). Key: 257.7 tok/s.

**B-D3 (short, 3).** FLOPs, bytes, intensity of a (1 x 8192) by (8192 x 8192) fp16 matmul; bound?
Key: FLOPs = 2 x 8192 x 8192 = 134,217,728. Bytes = (8192 + 8192^2 + 8192) x 2 = 134,250,496. Intensity about 1.0 FLOP/byte, far below any GPU's ridge point (hundreds), so memory-bound. Rubric: 1 FLOPs; 1 bytes and intensity; 1 conclusion with ridge comparison.

**B-D4 (MC, 1).** An agent makes 30 sequential calls. Probability at least one lands in the slowest 1% of latencies: (a) 0.01 (b) 0.26 (c) 0.30 (d) 0.74. Key: b (1 - 0.99^30 = 0.260).

## Section E. Agents and APIs (9 pts)
**B-E1 (numeric, 2).** 12 turns, each adds 1,000 tokens, full history resent, call 1 sends 1,000. Total billed input tokens, and cost at $4 per million. Key: 1,000 x 78 = 78,000 tokens; $0.312.

**B-E2 (numeric, 2).** Same run with caching: writes 125% and reads 10% of $4/M. Key: writes 12,000 x $5/M = $0.060; reads 66,000 x $0.40/M = $0.0264; total $0.0864.

**B-E3 (short, 3).** A tool call times out. Specify the harness behavior.
Key: enforce a bounded timeout; return an observation beginning "ERROR: timeout after Ns" so the model can adapt; retry only if the tool is idempotent, with a cap and backoff; never retry non-idempotent actions blindly; count against the step limit; log. Rubric: 1 bounded timeout and error observation; 1 retry policy distinguishing idempotent; 1 step cap or termination guarantee.

**B-E4 (MC, 1).** Which design follows the "Rule of Two"? An unsupervised agent has at most two of: untrusted input, access to sensitive data, ability to act externally or change state. Choose the configuration that satisfies it: (a) reads web pages, reads company files, sends email; (b) reads web pages, reads company files, cannot send or write anything; (c) all three with a prompt that says to be careful. Key: b.

## Section F. Tooling (5 pts)
**B-F1 (MC, 1).** Undo the last commit and discard its changes: (a) git revert HEAD (b) git reset --soft HEAD~1 (c) git reset --hard HEAD~1 (d) git stash. Key: c.

**B-F2 (short, 3).** Difference between srun and sbatch. Key: srun runs a command (or interactive shell with --pty) in an allocation and blocks your terminal; sbatch submits a batch script to the queue and returns immediately, with output to files, for long non-interactive jobs. Rubric: 1 interactive/foreground vs queued batch; 1 script with #SBATCH directives; 1 use cases.

**B-F3 (MC, 1).** `ssh -L 9000:localhost:8000 user@host` makes: (a) remote 9000 reach local 8000 (b) local port 9000 forward to port 8000 on the remote host (c) copy files (d) kill port 9000. Key: b.

**B-E5 (MC, 1).** Which change most likely invalidates a prompt cache? (a) appending a tool result to the end (b) editing a sentence at the start of the system prompt (c) a different final user question (d) waiting 10 seconds between calls. Key: b.

## Scoring
Sum points. 51 of 56 (90%) passes the quiz criterion. Also record per-section points. A blank scores 0; encourage "unsure" plus reasoning so blanks stop being uninformative.

## L5 formative check (agents module M00A)
Fresh numeric items used in the hub page: 8 turns x 1,500 tokens -> 54,000 input tokens; at $2/M -> $0.108; with caching (write 125%, read 10%) -> $0.0384. MC: tool executes in harness; cache breaks when an early prefix changes; tool exception -> ERROR observation and continue.
