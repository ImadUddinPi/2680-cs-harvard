# CS2680 course overview (source: cs2680.seas.harvard.edu, fetched 2026-10-14)

**Course:** CS2680 Modern AI Systems: Agents and System Optimizations. Harvard SEAS, Fall 2026. Instructor Juncheng Yang. No textbook, no exam. The student is NOT enrolled and self-studies the public materials.

**Idea:** follow one agentic system from the agent loop down through the serving stack. Students use a coding agent (Claude Code), design and measure their own agent, then serve an open-weight model and optimize the layers beneath it: batching and scheduling, KV cache and prefix reuse, routing, quantization, speculative decoding.

- **Part I: LLMs and agents.** Using coding agents, designing agents, architectures, use cases, optimizations.
- **Part II: Systems for LLMs and agents.** Serving (batching, scheduling, routing, caching, quantization, speculative decoding) and agentic systems.

## Prerequisites (stated)
CS61; at least one graduate computer-systems course; comfort with Python and PyTorch. The policy page says: if most of the background terms are unfamiliar, the course may not be a good fit.

## Background terms the course assumes (44)
Performance and scaling: latency, throughput, tail latency, scalability, Amdahl's law, IOPS, batching, pipelining, load balancing.
Execution and concurrency: process, threads, coroutine, concurrency, asynchronous execution, mutex, atomic operation, race condition, deadlock, starvation, context switch.
Memory and hardware: cache coherence, false sharing, virtual memory, page fault, copy-on-write, NUMA, DMA, interrupt, NIC, RDMA, locality, working set, LRU.
OS and I/O: system call.
Storage and data: write-ahead log, durability, transaction, ACID, serializability, B-tree, partitioning.
Distributed systems and networking: RPC, fault tolerance, congestion control.

## Schedule (tentative, 2026)
| Week | Topic |
|---|---|
| 1 | Overview and logistics; A1 out |
| 2 | Agents use I: how Claude Code works |
| 3 | Agents use II: 100x engineer with multi-agents; Agents design I: context management and tool design |
| 4 | Student sharing; Agents design II: multi-agent architecture, coordination, communication |
| 5 | Agents design III: memory and reliability; IV: agent evaluation |
| 6 | Guest: developing and evaluating agents in enterprise (Snowflake); Advanced agent design I: cost and performance |
| 7 | Advanced agent design II: safety, self-evolving harness |
| 8 | Efficient LLM serving: basics I and II |
| 9 | Assignment feedback; speculative decoding; project proposal due |
| 10 | Efficient agentic systems: scheduling and prefix caching; pruning and quantization |
| 11 | Guest (Meta): why infrastructure sets the pace of AI; GPU and kernels |
| 12 | KV-cache optimization and model architectures; agent-engine co-design |
| 13 | Efficient agentic systems: routing and load balancing |
| 14 | Others; full-stack optimizations; final project poster and demo (Dec 7), due Dec 8 |

## Assignments and grading
| Item | Weight | What |
|---|---|---|
| A1 Mads-Lens | 10% | Use Claude Code to build a web UI that streams a real agent session live: tool calls, inputs, results, subagent branching as a tree, failed runs flagged, session continuation, per-run cost. Writeup in repo. |
| A2 Mads-Loop | 10% | Build your own agent loop around a model API: tool calling with machine-readable schemas, context management, retries, termination, graceful handling of malformed output and broken tools. Evaluate on a provided benchmark and own tasks. Writeup. |
| A3 Mads-Opt | 20% | Optimize the system around a black-box model API: fewer tokens and calls, cheaper models where adequate, overlapped tool execution, compressed context, redesigned control flow. Task success fixed, cost and latency down. Published blog post. |
| A4 Mads-Serve | 20% | Replace the frontier API with a 7-8B open-weight model on an inference engine you operate. Measure quality drop, diagnose, recover via the harness. Writeup. |
| A5 Mads-Stack | 10% | Profile the full stack (agent loop, model, serving), write a performance hypothesis before changing anything, optimize across layers, rerun the same workload. Published blog post. |
| Final project | 20% | Proposal, poster and demo, final write-up. |
| Participation | 10% | |
| Bonus | up to 4% per presentation, 6% feedback, 2% each for problems current AI cannot solve | |

## Policies relevant to the student
- AI use is encouraged and must be disclosed (tools used and for what). The student owns every submitted line. Each assignment requires code, write-up and an archive of Claude Code session files. Claude Code is required in all five assignments.
- Course compute (not available to the student): Claude Code license via Harvard FAS; model APIs for A2-A3; course HPC with `gpu-cs2680` partition for A4-A5; AWS registration form (enrolled students). The student uses their own API keys and rented GPUs.

## Recommended background reading (from the course)
Operating Systems: Three Easy Pieces; Machine Learning Systems (mlsysbook.ai); Foundations of Large Language Models (arXiv 2501.09223); The Little Book of Deep Learning.

## Reading list by lecture (selected)
Claude Code best practices; Agentic Engineering Patterns; Claude Code agent teams; ReAct; a practical guide to building agents; Anthropic multi-agent research system; scaling agent systems; where agents fail; MemGPT; agent evaluation notes (notes/agent-evaluation.html); cost-effective agents notes (notes/cost-effective-agents.html); serving papers: Orca, vLLM/PagedAttention, speculative decoding, FlashAttention, DistServe, SGLang.
