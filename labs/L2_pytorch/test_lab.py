import pytest
import torch

import lab


def test_broadcast_shape():
    assert lab.broadcast_shape((8, 1, 5), (3, 1)) == (8, 3, 5)
    assert lab.broadcast_shape((4,), (2, 4)) == (2, 4)
    assert lab.broadcast_shape((1,), ()) == (1,)
    with pytest.raises(ValueError):
        lab.broadcast_shape((2, 3), (4,))


def test_views():
    x = torch.arange(6).reshape(2, 3)
    assert lab.shares_memory(x, x.T)
    assert not lab.shares_memory(x, x.T.contiguous())
    assert lab.flatten_transposed(x).tolist() == [0, 3, 1, 4, 2, 5]


def test_zero_grad_matters():
    good = lab.sgd_losses(zero_grad=True)
    assert good[-1] < 0.01
    bad = lab.sgd_losses(zero_grad=False)
    assert bad[-1] > 0.1  # gradients pile up; training goes wrong


def test_accumulation():
    assert lab.grad_after_two_backwards() == 6.0
