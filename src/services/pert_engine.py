"""
Core mathematical calculations and algorithms for EstimateOS.
Implements 3-Point PERT, Beta variance, Bayesian updates, MMRE and Pred(25).
"""
import math
from typing import List, Tuple

def calculate_pert(o: float, m: float, p: float) -> Tuple[float, float, float]:
    """
    Computes 3-Point PERT expected effort, standard deviation, and variance.
    Formula:
        Expected E = (O + 4M + P) / 6
        Std Dev sigma = (P - O) / 6
        Variance var = sigma^2
    """
    if o < 0 or m < 0 or p < 0:
        raise ValueError("Effort values must be non-negative.")
    if not (o <= m <= p):
        raise ValueError(f"Effort violation: Must satisfy O <= M <= P. Got O={o}, M={m}, P={p}")

    expected = (o + 4.0 * m + p) / 6.0
    sigma = (p - o) / 6.0
    variance = sigma ** 2
    return round(expected, 2), round(sigma, 2), round(variance, 4)

def calculate_calibrated_effort(expected_pert: float, calibration_factor: float) -> float:
    """Applies empirical calibration multiplier to PERT expected hours."""
    if expected_pert < 0 or calibration_factor <= 0:
        raise ValueError("Invalid parameters for calibrated effort.")
    return round(expected_pert * calibration_factor, 2)

def calculate_bayesian_update(
    prior_mean: float,
    prior_strength: float,
    observed_factors: List[float]
) -> float:
    """
    Computes posterior calibration factor via conjugate Bayesian update.
    Formula:
        K_post = (S * K_prior + sum(K_obs)) / (S + N)
    """
    if prior_strength <= 0:
        raise ValueError("Prior strength must be strictly positive.")
    if not observed_factors:
        return round(prior_mean, 3)

    numerator = prior_strength * prior_mean + sum(observed_factors)
    denominator = prior_strength + len(observed_factors)
    return round(numerator / denominator, 3)

def compute_mre(estimated: float, actual: float) -> float:
    """Computes Magnitude of Relative Error: |Actual - Estimated| / Actual."""
    if actual <= 0:
        raise ValueError("Actual hours must be strictly positive to compute MRE.")
    return round(abs(actual - estimated) / actual, 4)

def compute_mmre(pairs: List[Tuple[float, float]]) -> float:
    """Computes Mean Magnitude of Relative Error across a list of (estimated, actual) pairs."""
    if not pairs:
        return 0.0
    total_mre = sum(compute_mre(est, act) for est, act in pairs)
    return round(total_mre / len(pairs), 4)

def compute_pred25(pairs: List[Tuple[float, float]]) -> float:
    """Computes percentage of projects where MRE <= 0.25 (Pred(25))."""
    if not pairs:
        return 0.0
    within_threshold = sum(1 for est, act in pairs if compute_mre(est, act) <= 0.25)
    return round((within_threshold / len(pairs)) * 100.0, 2)
