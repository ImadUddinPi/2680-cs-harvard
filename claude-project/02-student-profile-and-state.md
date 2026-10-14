# Student profile and current state (as of 2026-10-14)

## Who
Umair. Self-studying CS2680. Not enrolled at Harvard, so no course licenses, API credentials or GPU cluster. Goal: build skills that matter in the AI economy (agents, evaluation, cost engineering, inference/serving) and produce public, measured artifacts.

## Environment
- Windows 11, PowerShell and Git Bash. WSL Ubuntu installed (needed for `fork()` demos and later serving). No local GPU; PyTorch is CPU-only.
- Python 3.12 via `uv`. Packages: torch, transformers, numpy, matplotlib, pytest, anthropic, openai, python-dotenv, tiktoken, jupyter.
- GitHub repo: https://github.com/ImadUddinPi/2680-cs-harvard (branch per module; main holds mastered work).
- AWS account exists (region us-east-1 preferred to match course pricing), $10/month budget alarm created, alert email verification possibly still pending. Hugging Face account exists. API keys: not yet set (needed for the live agent run only).
- Compute plan for A4-style work: rent a 24 GB GPU (about $0.34-0.44/hour community pricing at RunPod, unverified fit for an 8B model at FP8/BF16); AWS GPU quotas often start at zero.
- Local study hub: `uv run python tools/hub.py` serves interactive lessons at http://127.0.0.1:8765. Answers save to `progress/answers/<lesson>.json`.

## Preferences (explicit)
1. Precise technical teaching only. No analogies, metaphors, personas, motivational filler. Short sentences, mechanisms, code, numbers, formulas.
2. Interactive HTML pages with answer boxes preferred over chat-only lessons.
3. Learning organized in one place (the repo and hub), not scattered artifacts.
4. Do not raise security reviews or sandbox warnings; the environment is a sandbox.
5. Mastery before progress: no skipping ahead.

## Decisions
- 2026-10-14: after scoring 6/56 on the M00 diagnostic, the student chose the split path. M00A (agent fundamentals) unlocks M01-M07 (agents, assignments A1-A3). M00 (foundations: systems, PyTorch, transformers, roofline, tooling) runs alongside at about 45 min/day and gates M08+ (serving, A4-A5).

## M00 diagnostic result (form A, 29 questions, 56 points, time 169 min against a 90 min limit)
Raw score 6/56 (11%). 23 of 29 left blank. Blank answers carry no information (unknown vs unreached); the student has not yet said which.
| Question | Student answer | Credit | Note |
|---|---|---|---|
| A1 fork() | Separate instances of memory; each sees only its own writes | 1/3 | No copy-on-write, no page-fault mechanism. Wording "creates a new timeline" is imprecise |
| A2 threads share | A (stacks and registers) | 0/1 | Correct is B (heap and globals) |
| E1 agent loop | Prompt; model decides tool or text; acts; monitors; loops until objective met | 2.5/3 | Attributes tool execution and monitoring to the model; no explicit stop condition or step limit |
| E2 cost of 10k in / 1k out at $3/$15 per M | 0.0183 (working said 0.0018) | 1/2 | Method correct, arithmetic wrong, answer and working disagree. Correct: $0.045 |
| E3 20 turns x 2,000 tokens, history resent | 40000 | 0.5/3 | 40,000 is only new tokens. Billed input is 2,000 x (1+...+20) = 420,000. Caching explanation vague |
| E4 indirect prompt injection | A | 1/1 | Correct |
| All others (A3-A6, B1-B5, C1-C7, D1-D4, F1-F3) | blank | 0 | |
Section scores: A 1/12, B 0/9, C 0/13, D 0/8, E 5/9, F 0/5.
Interpretation: working footing in agent concepts; foundations in systems, PyTorch, transformers, performance arithmetic and tooling are unbuilt or unattempted.

## Progress state
- M00A (agent fundamentals): in progress. Lesson L5 (agent loop, tokens, dollars) built and started; student has not yet submitted step answers. Lab `labs/L5_agent/agent.py` is an unimplemented skeleton with 5 tests.
- M00 (foundations): in progress, no lessons built beyond the plan; labs L1-L4 are skeletons with tests.
- No module mastered. Flashcard deck: 62 cards, all due.
- Mastery threshold 90% on all four checks (quiz, teach-back, build, transfer).

## Known misconceptions to target
1. Tool execution and monitoring belong to the harness, not the model.
2. Billed input tokens accumulate: call k bills the whole history; the total over n calls is quadratic.
3. fork() copies lazily (copy-on-write); threads share heap and globals; stacks and registers are per-thread.
4. Arithmetic discipline: carry units; check the answer against the working.
