# Methods, conventions and repository mechanics

## Learning method
| Technique | Use |
|---|---|
| Mastery learning | Hard 90% gate on four criteria per module. No skipping ahead. |
| Retrieval practice + spaced repetition (SM-2) | Flashcard deck (progress/cards.jsonl). Start each session with due cards. |
| Prediction before measurement | The student writes numeric predictions before any calculator, run or reveal. Compare after. |
| Interleaving | Mix 2-3 older items into every session. |
| Teach-back | The student explains in writing or aloud; the tutor asks skeptical technical questions. |
| Build to learn | Code or measurement saved as evidence; tests are the spec. |
| Error log | One entry per mistake: what, why, fix. Convert mistakes into flashcards. |
| Desirable difficulty / transfer | Mastery is performance on a problem not seen in the lessons. |
| Escalating hints | question -> nudge -> partial -> worked example of a DIFFERENT problem. Never give the answer first. |
| Numbers as habit | Every lesson ends with a quantity computed or measured. |

## Teaching style rules (student's explicit demand)
No analogies, metaphors, personas, enthusiasm or filler. State mechanisms precisely with code, numbers and formulas. Short sentences. Technical questions only. Do not mention security warnings or sandboxing.

## Lesson loop (each concept)
1. Predict (written). 2. Precise explanation, minimal. 3. Calculator or demo, compare with prediction. 4. Build (tests). 5. Check with fresh questions. 6. Teach-back. 7. Error log and flashcards.

## Assessment protocol (for a tutor or assessor session)
1. Ask one question at a time unless the student submits a batch. Do not reveal keys before grading.
2. Score with the rubric in the assessment banks (forms A and B). MC 1 point, numeric 2 (full credit within 3%; half credit for correct method with arithmetic slip), short 3 by rubric. Partial credit allowed in 0.5 steps.
3. A blank scores 0 and is uninformative: ask the student to write a best guess plus "unsure".
4. Report: per-question credit, per-section totals, total, and the specific misconception behind each lost point.
5. For each gap give one corrective micro-task (a calculation or short code exercise) and one fresh retest question of the same skill.
6. Never reuse a question the student has seen. Create variants with changed numbers and context.
7. Output the command to log the result in the repo: `uv run python tools/learn.py score <module> <kind> <percent> -n "<note>"` where kind is diagnostic, quiz, teachback, build or transfer.
8. Mastery decision is made only when all four kinds are at least 90, latest values.

## Repository layout (github.com/ImadUddinPi/2680-cs-harvard)
- `curriculum.json` modules, requires, objectives. `CLAUDE.md` tutor protocol.
- `modules/<id>-<slug>/` README (objectives, gate), notes.md, evidence/.
- `labs/L0..L5` skeleton `lab.py` plus `test_*.py` (the spec). Run via `uv run python tools/learn.py lab L5`.
- `tools/learn.py` tracker and spaced repetition; `tools/hub.py` local study hub; `tools/seed_cards.py` deck seeding.
- `hub/` interactive lesson pages (`hub/lessons/L5.html`), `hub/lessons.json` registry.
- `progress/` state.json, log.jsonl (events: start, score, master, card, lab), cards.jsonl, answers/<lesson>.json.
- `docs/` diagnostic exam (form A), answer key, lesson plan, research outlook, METHOD.md.
- `PROGRESS.md` auto-generated dashboard.

## Git conventions
`main` holds only mastered work (plus infrastructure). One branch per module: `module/<id>-<slug>` (created by `learn.py start`). Conventional commit messages: `feat(M00A): ...`, `notes(M00A): ...`, `eval(M00): ...`, `fix(hub): ...`. On mastery: `learn.py master <id>` tags `mastered/<id>`; commit, push branch, open PR, merge, `git push --tags`. Never commit secrets (.env is ignored). Never force-push main.

## tools/learn.py commands
`status` (regenerate PROGRESS.md), `start <module>` (gate check, branch), `score <module> <kind> <pct> -n note`, `master <module>` (enforces gate), `lab <Lx>` (run lab tests, logged), `card add|due|review`, `scaffold`.

## Answer files
`progress/answers/<lesson>.json` maps field ids to values, with `_updated`. L5 fields: m1, done1; p1,p2,p3,p10,ptot,pcost,pcache,pred_locked; reflect, done3; r1,r2,done4; plan,stuck,hints_used,last_test_ok,last_test_output,done5; z1..z8,done6; tb,err,done7. Review by reading the file, then give written feedback and scores.

## SM-2 (flashcards)
Grade 0-5. If grade < 3: reps = 0, interval = 1 day. Else interval = 1 (first), 6 (second), then round(interval x ease). ease += 0.1 - (5-g)(0.08 + (5-g)0.02), min 1.3.

## Cost and compute constraints
No local GPU. API-based labs use the student's own keys (not set yet; L5 tests use a scripted fake model at zero cost). Rent GPUs only with a spending cap; stop instances when done. AWS budget alarm is $10/month.
