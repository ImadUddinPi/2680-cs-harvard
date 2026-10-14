"""L1 Systems lab. Fill in each TODO, then run: uv run pytest labs/L1_systems -q

Before coding: run stride_bench.py and write your PREDICTION of the row/column time ratio in notes.
"""
import threading
import time


def cold_misses(n_elems: int, elem_bytes: int, line_bytes: int = 64) -> int:
    """Compulsory cache misses for one sequential pass over a contiguous array on a cold cache."""
    raise NotImplementedError  # TODO


def amdahl(parallel_fraction: float, cores: int) -> float:
    """Speedup when `parallel_fraction` of the runtime scales perfectly over `cores`."""
    raise NotImplementedError  # TODO


class Counter:
    def __init__(self):
        self.value = 0


def racy_total(n_threads: int, n_incr: int) -> int:
    """Run n_threads threads, each doing n_incr increments on a shared Counter WITHOUT a lock.

    Implement each increment as read, time.sleep(0) (yields the GIL), then write read+1,
    so the lost-update race shows up reliably. Return the final counter value.
    """
    raise NotImplementedError  # TODO


def locked_total(n_threads: int, n_incr: int) -> int:
    """Same workload as racy_total but correct, using a threading.Lock."""
    raise NotImplementedError  # TODO


def sharded_total(n_threads: int, n_incr: int) -> int:
    """Third fix: no shared state while working. Each thread counts locally; sum at the end."""
    raise NotImplementedError  # TODO
