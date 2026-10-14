import roofline as r


def test_matmul():
    f, b = r.matmul_cost(4096, 4096, 4096)
    assert f == 2 * 4096**3
    assert b == 3 * 4096**2 * 2
    assert abs(r.intensity(f, b) - 1365.3) < 0.5


def test_ridge_and_bound():
    assert abs(r.ridge(1000e12, 3e12) - 333.3) < 0.1
    f, b = r.matmul_cost(4096, 4096, 4096)
    assert r.bound(f, b, 1000e12, 3e12) == "compute"
    f1, b1 = r.matmul_cost(1, 4096, 4096)  # one token through one layer: matrix x vector
    assert r.bound(f1, b1, 1000e12, 3e12) == "memory"


def test_decode_ceiling():
    assert abs(r.decode_tps_ceiling(14e9, 2e12) - 142.857) < 0.01
    assert abs(r.decode_tps_ceiling(14e9, 2e12, kv_bytes_per_seq=2e9, batch=16) - 695.65) < 0.1
    # int4 weights give 4x the ceiling
    assert abs(r.decode_tps_ceiling(3.5e9, 2e12) / r.decode_tps_ceiling(14e9, 2e12) - 4) < 1e-9
