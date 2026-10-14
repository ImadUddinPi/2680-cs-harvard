import agent


def scripted(*steps):
    it = iter(steps)
    seen = []

    def model(messages):
        seen.append(list(messages))
        return next(it)

    model.seen = seen
    return model


U = {"in": 100, "out": 10}


def test_tool_then_final():
    m = scripted(
        {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}, "usage": U},
        {"type": "final", "text": "5", "usage": U},
    )
    r = agent.run_agent(m, {"add": lambda a, b: a + b}, "2+3?")
    assert r["final"] == "5" and r["stopped"] == "final" and r["steps"] == 2
    assert r["usage"] == {"in": 200, "out": 20}
    last = m.seen[-1][-1]
    assert last["role"] == "tool" and last["name"] == "add" and last["content"] == "5"


def test_unknown_tool_does_not_crash():
    m = scripted(
        {"type": "tool_call", "name": "nope", "args": {}, "usage": U},
        {"type": "final", "text": "ok", "usage": U},
    )
    r = agent.run_agent(m, {}, "x")
    assert r["final"] == "ok"
    assert m.seen[-1][-1]["content"].startswith("ERROR:")


def test_tool_exception_and_bad_args():
    def boom():
        raise RuntimeError("disk on fire")

    m = scripted(
        {"type": "tool_call", "name": "boom", "args": {}, "usage": U},
        {"type": "tool_call", "name": "boom", "args": {"unexpected": 1}, "usage": U},
        {"type": "final", "text": "gave up", "usage": U},
    )
    r = agent.run_agent(m, {"boom": boom}, "x")
    assert r["final"] == "gave up"
    errs = [x["content"] for x in m.seen[-1] if x.get("role") == "tool"]
    assert len(errs) == 2 and all(e.startswith("ERROR:") for e in errs)


def test_step_cap():
    call = {"type": "tool_call", "name": "t", "args": {}, "usage": U}
    m = scripted(*[call] * 10)
    r = agent.run_agent(m, {"t": lambda: "x"}, "loop forever", max_steps=3)
    assert r["final"] is None and r["stopped"] == "max_steps" and r["steps"] == 3
    assert r["usage"]["in"] == 300


def test_cost():
    assert abs(agent.cost_usd({"in": 10_000, "out": 1_000}, 3.0, 15.0) - 0.045) < 1e-12
