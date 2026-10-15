"""Model evaluation with explicit residual sign and spatial holdout groups."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ValidationMetrics:
    n: int
    mean_error: float  # predicted minus observed
    mean_absolute_error: float
    rmse: float
    interval_coverage: float | None


def evaluate_predictions(observed, predicted, lower=None, upper=None) -> ValidationMetrics:
    """Bias and accuracy metrics, with optional empirical interval coverage.

    Coverage should be calculated on genuinely held-out observations.
    """
    o, p = np.asarray(observed, float), np.asarray(predicted, float)
    if o.ndim != 1 or p.shape != o.shape or o.size == 0:
        raise ValueError("Expected same-length non-empty one-dimensional arrays")
    if not np.isfinite(o).all() or not np.isfinite(p).all():
        raise ValueError("Non-finite observations or predictions")
    coverage = None
    if (lower is None) != (upper is None):
        raise ValueError("Provide lower and upper together")
    if lower is not None:
        low, high = np.asarray(lower, float), np.asarray(upper, float)
        if low.shape != o.shape or high.shape != o.shape:
            raise ValueError("Interval bounds must match observations")
        if not np.isfinite(low).all() or not np.isfinite(high).all():
            raise ValueError("Interval bounds must be finite")
        if np.any(low > high):
            raise ValueError("Invalid interval bounds")
        coverage = float(np.mean((o >= low) & (o <= high)))
    residual = p - o
    return ValidationMetrics(
        int(o.size), float(np.mean(residual)), float(np.mean(np.abs(residual))),
        float(np.sqrt(np.mean(residual ** 2))), coverage,
    )


def leave_one_group_out(groups):
    """Generate nonoverlapping train/test site or ranch holdouts.

    Additional spatial, time and preprocessing leakage safeguards may be needed.
    """
    g = np.asarray(groups)
    if g.ndim != 1 or g.size < 2:
        raise ValueError("Need at least two observations")
    labels = np.unique(g)
    if labels.size < 2:
        raise ValueError("Need at least two independent groups")
    for label in labels:
        yield np.flatnonzero(g != label), np.flatnonzero(g == label)
