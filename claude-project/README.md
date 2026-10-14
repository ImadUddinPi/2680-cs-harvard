# Claude Project knowledge pack for CS2680 assessment

## How to use
1. Create a new Claude Project.
2. Open the project's **Instructions** (custom instructions) and paste the full contents of `INSTRUCTIONS.md`.
3. Add every other file in this folder to **Project knowledge**: files 01 to 10 (not this README, not INSTRUCTIONS.md).
4. Start a chat in the project. First message suggestion: paste `progress/answers/L5.json` and the output of `uv run python tools/learn.py status`, and say what you want assessed.

## Files
| File | Purpose |
|---|---|
| INSTRUCTIONS.md | Paste into project instructions. Role, style rules, gate, assessment protocol. |
| 01-course-overview.md | CS2680 syllabus, assignments, grading, policies, the 44 assumed terms |
| 02-student-profile-and-state.md | Student, environment, preferences, decisions, diagnostic results by question, known misconceptions |
| 03-curriculum-and-gating.md | 17 modules, dependencies, objectives, mastery gate (generated from curriculum.json) |
| 04-assessment-bank-form-a.md | The exam already taken, with keys and rubrics. Do not reuse for retest |
| 05-assessment-bank-form-b.md | Fresh 56-point question set with keys, plus L5 formative items |
| 06-technical-reference-notes.md | Precise lesson content: systems, PyTorch, attention and KV cache, roofline, agent loop and cost, tooling, serving concepts |
| 07-industry-research-digest.md | Graded research findings, workflows, forecast dates, unverified items |
| 08-methods-and-conventions.md | Learning method, assessment protocol, repo layout, git conventions, commands, SM-2 |
| 09-flashcards.md | 62-card deck (44 background terms plus key numbers) |
| 10-labs-reference.md | Lab specs and code review rubric |

## Keeping it current
The repo is the source of truth. After meaningful progress, regenerate or edit: 02 (state), 03 (run the generator snippet in the repo history or edit by hand), 09 (cards). Files 04 and 05 stay unless you add new question forms.

## Notes
- The student's private account details are not included. Keys go in `.env`, never in this folder.
- Files 04 and 05 contain answers. Keep this project private to the tutor session.
