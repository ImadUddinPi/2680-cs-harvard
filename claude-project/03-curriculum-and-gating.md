# Curriculum, dependencies and mastery gate

Source of truth: curriculum.json in the repo. Module state is in progress/state.json; scores in progress/log.jsonl.

## Mastery gate (non-negotiable)
- A module may start only when every module in its `requires` list is mastered.
- Mastered = the LATEST score is at least 90 on all four criteria:
  1. quiz: closed-book, fresh questions from the tutor
  2. teachback: the student explains the topic; the tutor plays a skeptical new engineer and asks naive questions
  3. build: working code or a measurement saved in modules/<id>/evidence/
  4. transfer: a novel problem not seen in the lessons, solved cold
- A failed gate: diagnose the specific gap, reteach differently, retest with NEW questions.
- Split path (decided 2026-10-14): M00A unlocks M01-M07. M00 runs alongside and gates M08 onward together with M07.

## Modules
### M00A Agent fundamentals: the loop, tokens and cost
- Part 0, course weeks -, assignment: none
- Requires: nothing
- Objectives:
  - Explain the agent loop and who does what (model vs harness)
  - Compute billed tokens and dollars for a multi-turn agent, with and without caching
  - Implement a tested agent loop with tool errors, step caps and usage accounting
  - Read one agent trace and say where cost and failures come from
- Readings: Anthropic: Building effective agents; Anthropic docs: Prompt caching; ReAct (abstract and trajectory examples)

### M00 Foundations: systems, PyTorch, transformers, roofline, tooling
- Part 0, course weeks -, assignment: none
- Requires: nothing
- Objectives:
  - Reproducible Python 3.12 + PyTorch env via uv
  - Explain process/thread/virtual memory/caches/syscalls (CS61 level)
  - Write a PyTorch training loop and tiny transformer block from memory
  - Explain latency vs throughput, roofline, memory-bound vs compute-bound
  - Read an arXiv systems paper with a structured method
- Readings: OSTEP (selected chapters: virtualization, concurrency); mlsysbook.ai ch. on training & HW; arXiv 2501.09223 Foundations of LLMs ch.1-2; Little Book of Deep Learning

### M01 Agents use I-II: Claude Code & multi-agent
- Part 1, course weeks 2-3, assignment: A1 Mads-Lens (10%)
- Requires: M00A
- Objectives:
  - Explain the Claude Code loop, tools, context, permissions
  - Run parallel agents/teams on a real task
  - Trace and annotate an agent session (A1)
- Readings: Claude Code best practices; Agentic Engineering Patterns; Claude Code agent teams; Research acceleration at OpenAI; cs2680 readings/sep-09, sep-14

### M02 Agents design I: loop, context management, tool design
- Part 1, course weeks 3, assignment: A2 Mads-Loop (10%) starts
- Requires: M01
- Objectives:
  - Implement ReAct loop against a model API from scratch
  - Design tools with good schemas/errors
  - Manage context window: truncation, summarization, compaction
- Readings: ReAct; A practical guide to building agents; readings/sep-16

### M03 Agents design II: multi-agent architecture & coordination
- Part 1, course weeks 4, assignment: A2 Mads-Loop
- Requires: M02
- Objectives:
  - Compare orchestrator-worker, debate, pipeline topologies
  - Quantify when multi-agent helps vs hurts
- Readings: Multi-agent research system (Anthropic); Scaling agent systems; readings/sep-23

### M04 Agents design III: memory & reliability
- Part 1, course weeks 5, assignment: A2 Mads-Loop
- Requires: M03
- Objectives:
  - Classify agent failure modes
  - Implement tiered memory (MemGPT-style)
  - Add retries/verification/guardrails
- Readings: Where agents fail; MemGPT; readings/sep-28

### M05 Agents design IV: evaluation
- Part 1, course weeks 5, assignment: A2 Mads-Loop due
- Requires: M04
- Objectives:
  - Build an eval harness with graders
  - Measure pass@k, cost, latency, variance
  - Spot eval contamination/leakage
- Readings: notes/agent-evaluation.html

### M06 Advanced agent design I: cost & performance (token efficiency)
- Part 1, course weeks 6, assignment: A3 Mads-Opt (20%)
- Requires: M05
- Objectives:
  - Profile token spend per step
  - Apply caching, routing, cascades, compaction
  - Show Pareto improvement on cost vs accuracy
- Readings: notes/cost-effective-agents.html

### M07 Advanced agent design II: safety & self-evolving harness
- Part 1, course weeks 7, assignment: none
- Requires: M06
- Objectives:
  - Threat-model an agent (prompt injection, tool abuse)
  - Explain self-improving harness loops
- Readings: course discussion papers

### M08 Efficient LLM serving: basics (batching, scheduling)
- Part 2, course weeks 8, assignment: A4 Mads-Serve (20%)
- Requires: M07, M00
- Objectives:
  - Derive prefill vs decode costs
  - Explain continuous batching, PagedAttention
  - Run vLLM/SGLang and measure TTFT/TPOT/throughput
- Readings: Orca; vLLM/PagedAttention; slides 1-8

### M09 Efficient LLM serving: speculative decoding
- Part 2, course weeks 9, assignment: A4
- Requires: M08
- Objectives:
  - Prove acceptance-rejection preserves distribution
  - Implement draft-verify loop
  - Model speedup vs acceptance rate
- Readings: Leviathan et al. speculative decoding; Medusa/EAGLE

### M10 Efficient agentic systems: scheduling & prefix caching
- Part 2, course weeks 10, assignment: A4
- Requires: M09
- Objectives:
  - Explain RadixAttention/prefix reuse
  - Design schedulers for agent workflows (program-level)
- Readings: SGLang; Continuum/Parrot-style papers

### M11 Efficient LLM serving: pruning & quantization
- Part 2, course weeks 10, assignment: A4/A5
- Requires: M10
- Objectives:
  - Implement int8/int4 weight quant by hand
  - Explain GPTQ/AWQ/FP8 tradeoffs
- Readings: LLM.int8(); GPTQ; AWQ

### M12 Efficient LLM serving: GPU & kernels
- Part 2, course weeks 11, assignment: A5 Mads-Stack (10%)
- Requires: M11
- Objectives:
  - Roofline analysis of attention/GEMM
  - Explain FlashAttention tiling
  - Write a Triton kernel
- Readings: FlashAttention 1-3; GPU MODE lectures

### M13 KV-cache optimization & model architectures
- Part 2, course weeks 12, assignment: A5
- Requires: M12
- Objectives:
  - Compute KV memory per token for MHA/GQA/MLA
  - Explain eviction/offload/compression
- Readings: GQA; DeepSeek MLA; KV cache compression papers

### M14 Efficient agentic systems: routing, load balancing, others
- Part 2, course weeks 13-14, assignment: A5 Mads-Stack
- Requires: M13
- Objectives:
  - Design cache-aware routing
  - Explain disaggregated prefill/decode
- Readings: DistServe; Mooncake; llm-d

### M15 Final project
- Part 3, course weeks 9-14, assignment: Final (20%)
- Requires: M14
- Objectives:
  - Proposal, implementation, poster, demo
- Readings: project.html

## Planned additions (proposed, not yet applied)
- M02: security lab (score the agent against the lethal trifecta, run an injection test); context engineering (compaction, notes file, sub-agent summaries).
- M05: production evaluation (trace-to-test-case loop, pass^k).
- M06: caching exercise with measured cost.
- M08 onward: honest benchmarking checklist as the grading rubric for serving write-ups.
