from copy import copy
import pandas as pd
import numpy as np


def forecast_scalar(
    cs_forecasts: pd.DataFrame,
    target_abs_forecast: float = 10.0,
    window: int = 250000,  ## JUST A VERY LARGE NUMBER TO USE ALL DATA
    min_periods: int = 500,  # MINIMUM PERIODS BEFORE WE ESTIMATE A SCALAR
    backfill: bool = True,  ## BACKFILL OUR FIRST ESTIMATE, SLIGHTLY CHEATING, BUT...
) -> pd.Series:
    """
    Work out the scaling factor for cross-sectional forecasts such that T*x has an
    average absolute value equal to target_abs_forecast (typically 10.0).

    This implementation computes a rolling scalar based on historical forecast values.

    :param cs_forecasts: forecasts, cross-sectionally (TxN DataFrame)
    :type cs_forecasts: pd.DataFrame

    :param target_abs_forecast: The target average absolute value for the scaled forecast
    :type target_abs_forecast: float

    :param window: Lookback window for computing the average absolute value
    :type window: int

    :param min_periods: Minimum number of periods before producing an estimate
    :type min_periods: int

    :param backfill: If True, backfills the first valid estimate to the start of the series
    :type backfill: bool

    :returns: pd.Series -- The computed scaling factors
    """
    # Canonicalize boolean if passed as string (e.g. from YAML)
    if isinstance(backfill, str):
        backfill = backfill.lower() in ("t", "true", "yes", "1")

    # Remove zeros/nans to avoid bias from missing data
    copy_cs_forecasts = copy(cs_forecasts)
    copy_cs_forecasts[copy_cs_forecasts == 0.0] = np.nan

    # Take Cross-Sectional average first (median is more robust to outliers)
    # We do this before the Time-Series average to avoid jumps in scalar
    # when new markets are introduced.
    if copy_cs_forecasts.shape[1] == 1:
        x = copy_cs_forecasts.abs().iloc[:, 0]
    else:
        # ffill here ensures we have a view of the "current" forecast level across the pool
        x = copy_cs_forecasts.ffill().abs().median(axis=1)

    # Compute Rolling Time-Series average of absolute values
    avg_abs_value = x.rolling(window=window, min_periods=min_periods).mean()

    # Scaling factor is Target / Current Avg
    scaling_factor = target_abs_forecast / avg_abs_value

    if backfill:
        scaling_factor = scaling_factor.bfill()

    return scaling_factor
