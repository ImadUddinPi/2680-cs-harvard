# Industry research digest (14 Oct 2026): why each skill matters

Source: the repo's docs/research/industry-outlook-2026-q4.html (five research streams, about 190 tool calls). Grades: P = primary page fetched and seen; S = secondary; C = sources conflict. Use this to justify priorities and to answer "why learn X". Do not quote S or C items as established facts.

## Ten findings
1. Small-tier input prices are $0.10-$0.30 per million tokens; flagships are $10 in / $50 out (Anthropic and OpenAI pages, P). Cache reads cost 5-10% of input, batch is 50% off (P). Google schedules increases (Gemini 4 Argon to $4/$20 on 1 Dec 2026; Gemini 3.8 Flash to $1.50/$7.50 on 1 Jan 2027, P).
2. Agent benchmarks are unreliable: SWE-bench Verified reported contaminated, SWE-bench Pro grading questioned, OSWorld results differ by source (S/C). METR says its suite is unreliable above 16 hours; page not actively updated since 8 Sep 2026 (P); no verified doubling time.
3. Open-weight models trail closed by about 4 months or about 12 index points (Epoch 29 May 2026 P; Artificial Analysis Oct 2026 P). The best are 300B-2.8T mixture-of-experts models; the best dense single-GPU model scores 34 vs 58 for the best closed.
4. Indeed (P, data to Jun 2026): US software postings about +15% since Feb 2025 but 27.5% below Feb 2020; 71% of the May 2025-May 2026 increase from senior roles; entry-level is 4.5% of software postings. Stanford (P, revised 12 Aug 2026): ages 22-25 in AI-exposed occupations 19% below peers, mainly reduced hiring; no broad displacement; descriptive, not causal.
5. AI-skill pay premium: headline 28% (Lightcast, S) and 62% (PwC, S) compare roles; Indeed's within-occupation estimate is about 5% (P).
6. Agent reliability comes from structure (Anthropic harness post P, Cursor P, Cognition P): one feature per session, git checkpoints, JSON feature list only tests can flip, end-to-end tests, clean-context reviewer, single-threaded writes. Unstructured swarms underperform. Multi-agent costs about 15x chat tokens; token use explained 80% of BrowseComp variance (Anthropic P).
7. Verified incidents share a root cause: trust granted by location or name, not content. LiteLLM PyPI compromise (24 Mar 2026, P), Cursor CVE-2025-54135/54136 (P), Codex CLI CVE-2025-61260 config execution (P), ClawHub malicious skills (P core), Replit database deletion (P).
8. Serving: learn vLLM first (v0.31.0), then SGLang (v0.5.21); Dynamo and llm-d are cluster layers (release pages P). Vendor "up to Nx" gains shrink under honest workloads; report TTFT/TPOT percentiles and goodput at an SLO. A student project on a rented 24 GB GPU costs under about $10 (S pricing).
9. EU Digital Omnibus on AI in force 27 Jul 2026 (P): stand-alone high-risk rules 2 Dec 2027, embedded 2 Aug 2028; Article 50 disclosure from 2 Aug 2026; general-purpose model enforcement from 2 Aug 2026 (S).
10. Adoption statistics are weak: Gartner's ">40% of agentic projects cancelled by end of 2027" rests on a poll of 3,412 webinar attendees (S); MIT "95% of pilots fail" has a contested, small sample (S/C).

## Skills in demand (most consistent evidence first)
Python and deployment fundamentals (Python in 62-71% of AI-engineer postings, S); agent loop with tracing and a small eval set; cost and latency engineering; serving, profiling and honest benchmarking; security by architecture; directing coding agents with verification. Observability appears in about 40% of AI engineering postings and CI/CD in about a third (one analysis, S). Prompt writing alone is table stakes.

## Productivity evidence
METR RCT early 2025: 19% slower (16 developers); late-2025 follow-up: about 4% to 18% faster with intervals including zero, selection effects (P). NBER w35275: commits +30% (autocomplete), +180% (interactive agents), +240% (autonomous agents), but releases only about +30% (P). Verification is the bottleneck.

## Exact workflows (runbooks)
- W1 agentic coding session: spec in a file; feature list JSON all failing; one feature per session; end-to-end test the agent cannot edit; commit; clean-context review; human merges; archive session files.
- W2 evaluation loop: 20-50 tasks from real failures; reference solutions; code graders first; k trials, report pass@k and pass^k; read transcripts; error-analysis taxonomy over 100+ traces; add failures as tests.
- W3 cost and latency: fix workload and success check; trace tokens and dollars per step; stabilize and cache the prefix; route easy calls to a small model; batch offline work; sub-agent summaries of 1-2k tokens; re-measure with variance.
- W4 serving: hypothesis with a number; baseline on vLLM; TTFT, TPOT p50/p99, goodput; toggle prefix cache and chunked prefill; quantize and recheck accuracy; repeat on SGLang; cost per million tokens.
- W5 agent security: list data, inputs and actions; score the trifecta; remove one leg or gate it; least-privilege credentials; pin and vet dependencies, skills and MCP servers; log tool calls; red-team with injected content.

## Scheduled dates to watch (Oct 2026 - Jan 2027)
1 Dec 2026 Gemini 4 Argon price rise; 2 Dec 2026 EU machine-readable marking duty for existing systems; 1 Jan 2027 Gemini 3.8 Flash price rise and Colorado SB 26-189 effective; vLLM v0.32 removes the V1 engine.

## Unverified (do not rely on)
Model release lists from aggregators; METR figures above 16 hours; market-size numbers; "dynamic workflows" announcement; Agent Plugins 1.0; OWASP v2.01 statistics (PDF not read); Gartner exact wording; McKinsey 2026 primary page.
