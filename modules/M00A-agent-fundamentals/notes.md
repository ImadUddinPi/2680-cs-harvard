# M00A notes (my own words)

## L5 predict (write BEFORE reading or coding)
An agent runs 10 turns. Each turn the model sees everything so far, and each turn adds 2,000 new tokens (tool result + reply).
- Input tokens billed on turn 1: ____
- Input tokens billed on turn 2: ____
- Input tokens billed on turn 3: ____
- Input tokens billed on turn 10: ____
- Total input tokens billed over all 10 turns: ____
- Cost at $3 per million input tokens: ____
- With caching, which tokens are the "new" ones each turn and what fraction of each turn's input is a repeat of an earlier turn? ____
