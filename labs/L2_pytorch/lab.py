"""L2 PyTorch lab. Run: uv run pytest labs/L2_pytorch -q"""
import torch


def broadcast_shape(a: tuple, b: tuple) -> tuple:
    """NumPy/PyTorch broadcasting rule WITHOUT calling torch. Raise ValueError if incompatible."""
    raise NotImplementedError  # TODO


def shares_memory(x: torch.Tensor, y: torch.Tensor) -> bool:
    """True if x and y are views onto the same underlying storage."""
    raise NotImplementedError  # TODO


def flatten_transposed(x: torch.Tensor) -> torch.Tensor:
    """Return x.T flattened to 1-D in logical (row-major of x.T) order. Must work for non-contiguous x.T."""
    raise NotImplementedError  # TODO


def sgd_losses(zero_grad: bool, steps: int = 50, lr: float = 0.2) -> list:
    """Train y = 3x + 1 with a single nn.Linear(1,1) using torch.manual_seed(0), SGD, MSE.

    Data: x = torch.linspace(-1, 1, 32).unsqueeze(1), y = 3x + 1.
    If zero_grad is False, never clear gradients (the bug). Return the list of float losses per step.
    """
    raise NotImplementedError  # TODO


def grad_after_two_backwards() -> float:
    """w=tensor([2.0], requires_grad=True); loss=(3*w).sum(); call backward twice (retain_graph=True).
    Return w.grad.item(). Predict it before running."""
    raise NotImplementedError  # TODO
