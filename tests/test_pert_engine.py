"""
Unit test suite for PERT math and estimation metrics.
"""
import pytest
from src.services.pert_engine import (
    calculate_pert,
    calculate_calibrated_effort,
    calculate_bayesian_update,
    compute_mre,
    compute_mmre,
    compute_pred25
)

def test_pert_standard_calculation():
    # O=10, M=16, P=34 -> E = (10 + 64 + 34)/6 = 108/6 = 18.0
    # sigma = (34 - 10)/6 = 24/6 = 4.0
    # variance = 16.0
    expected, sigma, var = calculate_pert(10.0, 16.0, 34.0)
    assert expected == 18.0
    assert sigma == 4.0
    assert var == 16.0

def test_pert_invalid_order_raises():
    with pytest.raises(ValueError):
        calculate_pert(20.0, 10.0, 30.0)  # O > M

def test_pert_negative_effort_raises():
    with pytest.raises(ValueError):
        calculate_pert(-5.0, 10.0, 20.0)

def test_calibrated_effort():
    calibrated = calculate_calibrated_effort(100.0, 1.15)
    assert calibrated == 115.0

def test_bayesian_update_smooth_adjustment():
    # Prior: 1.0, Strength: 5.0. Observed: [1.3, 1.4] (N=2)
    # Post = (5.0*1.0 + 2.7) / (5.0 + 2) = 7.7 / 7 = 1.100
    post = calculate_bayesian_update(1.0, 5.0, [1.3, 1.4])
    assert post == 1.100

def test_bayesian_update_no_observations_returns_prior():
    post = calculate_bayesian_update(1.15, 5.0, [])
    assert post == 1.15

def test_mre_calculation():
    # Est = 80, Act = 100 -> |100 - 80| / 100 = 0.20
    assert compute_mre(80.0, 100.0) == 0.20

def test_mmre_and_pred25():
    # Pairs: (80, 100) -> MRE = 0.20 (<= 0.25)
    #        (110, 100) -> MRE = 0.10 (<= 0.25)
    #        (50, 100) -> MRE = 0.50 (> 0.25)
    pairs = [(80.0, 100.0), (110.0, 100.0), (50.0, 100.0)]
    mmre = compute_mmre(pairs)
    # Average MRE = (0.20 + 0.10 + 0.50) / 3 = 0.80 / 3 = 0.2667
    assert mmre == 0.2667
    pred25 = compute_pred25(pairs)
    # 2 out of 3 within 25% -> 66.67%
    assert pred25 == 66.67
