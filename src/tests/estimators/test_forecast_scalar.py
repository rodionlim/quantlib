import pandas as pd
import numpy as np
import pytest

from quantlib_st.estimators.forecast_scalar import forecast_scalar


def test_forecast_scalar_basic():
    # Create 1000 days of data for 2 instruments
    dates = pd.date_range("2020-01-01", periods=1000)
    # Market 1 has avg abs value of 2
    # Market 2 has avg abs value of 4
    # Median should be 3
    data = {"m1": np.ones(1000) * 2, "m2": np.ones(1000) * 4}
    df = pd.DataFrame(data, index=dates)

    target = 10.0
    # Window 250000, min_periods 10
    scalar = forecast_scalar(
        df, target_abs_forecast=target, min_periods=10, backfill=False
    )

    # First 9 should be NaN
    assert scalar.iloc[:9].isna().all()
    # Thereafter should be 10 / 3 roughly
    assert pytest.approx(scalar.iloc[10], 0.01) == 10.0 / 3.0
    assert len(scalar) == 1000


def test_forecast_scalar_single_instrument():
    dates = pd.date_range("2020-01-01", periods=100)
    df = pd.DataFrame({"m1": np.ones(100) * 2.0}, index=dates)

    scalar = forecast_scalar(
        df, target_abs_forecast=10.0, min_periods=1, backfill=False
    )
    assert scalar.iloc[0] == 5.0


def test_forecast_scalar_with_zeros():
    dates = pd.date_range("2020-01-01", periods=100)
    # Constant 10, but some zeros
    # If zeros are treated as NaN/ignored, mean remains 10
    vals = np.ones(100) * 10.0
    vals[50:] = 0.0
    df = pd.DataFrame({"m1": vals}, index=dates)

    scalar = forecast_scalar(
        df, target_abs_forecast=10.0, min_periods=1, backfill=False
    )

    # Up to 50, scalar 1.0
    assert scalar.iloc[49] == 1.0
    # After 50, it should still be 1.0 because 0.0 becomes NaN and is ignored in mean
    assert scalar.iloc[75] == 1.0
