"""L5 Agent loop lab (this is the skeleton of Assignment 2). Run: uv run pytest labs/L5_agent -q

`model(messages)` is any callable returning one of:
  {"type": "tool_call", "name": str, "args": dict, "usage": {"in": int, "out": int}}
  {"type": "final",     "text": str,                "usage": {"in": int, "out": int}}
Tests use a scripted fake model, so no API key and no cost. Wire a real API in live_run.py later.
"""
from typing import Callable


def run_agent(model: Callable, tools: dict, task: str, max_steps: int = 8) -> dict:
    """Run the loop and return:
      {"final": str | None, "steps": int, "usage": {"in": int, "out": int}, "stopped": "final" | "max_steps"}

    Rules (each is tested):
      * messages start as [{"role": "user", "content": task}]
      * on a tool_call: append the assistant call, run tools[name](**args), append
        {"role": "tool", "name": name, "content": str(result)}
      * unknown tool, bad arguments, or a tool that raises: do NOT crash. Append an observation
        starting with "ERROR:" so the model can recover
      * sum token usage over every model call
      * stop at the first "final", or after max_steps model calls with final=None, stopped="max_steps"
    """
    raise NotImplementedError  # TODO


def cost_usd(usage: dict, price_in_per_m: float, price_out_per_m: float) -> float:
    """Dollar cost of a usage dict {"in":..., "out":...}."""
    raise NotImplementedError  # TODO
