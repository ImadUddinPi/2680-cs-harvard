import lab


def test_cold_misses():
    assert lab.cold_misses(1_048_576, 4) == 65_536
    assert lab.cold_misses(1000, 8) == 125
    assert lab.cold_misses(65, 1) == 2  # partial last line still costs a miss


def test_amdahl():
    assert abs(lab.amdahl(0.9, 10) - 5.263) < 0.01
    assert abs(lab.amdahl(0.9, 10**9) - 10.0) < 0.01
    assert lab.amdahl(0.0, 64) == 1.0


def test_race_loses_updates():
    assert lab.racy_total(4, 2000) < 4 * 2000


def test_fixes_are_correct():
    assert lab.locked_total(4, 2000) == 8000
    assert lab.sharded_total(4, 2000) == 8000
