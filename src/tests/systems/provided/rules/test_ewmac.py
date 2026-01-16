import pandas as pd
import numpy as np

from quantlib_st.systems.provided.rules.ewmac import ewmac_calc_vol


def test_ewmac_calc_vol_basic():
    # Create synthetic daily price data
    dates = pd.date_range(start="2020-01-01", periods=100, freq="B")
    # Linear upward trend
    price = pd.Series(np.linspace(100, 110, 100), index=dates)

    # Run ewmac_calc_vol
    Lfast = 16
    Lslow = 64
    forecast = ewmac_calc_vol(price, Lfast=Lfast, Lslow=Lslow)

    assert isinstance(forecast, pd.Series)
    assert len(forecast) == 100
    # In an upward trend, fast EWMA should be above slow EWMA
    # So forecast should be positive
    # (Excluding the very beginning where they might be equal or influenced by initialization)
    assert forecast.iloc[-1] > 0


def test_ewmac_calc_vol_default_lslow():
    dates = pd.date_range(start="2020-01-01", periods=100, freq="B")
    price = pd.Series(np.linspace(100, 110, 100), index=dates)

    # Default Lslow is 4 * Lfast
    Lfast = 16
    forecast_default = ewmac_calc_vol(price, Lfast=Lfast)
    forecast_explicit = ewmac_calc_vol(price, Lfast=Lfast, Lslow=64)

    pd.testing.assert_series_equal(forecast_default, forecast_explicit)


def test_ewmac_calc_vol_resample():
    # Create non-business day data
    dates = pd.date_range(start="2020-01-01", periods=100, freq="D")
    price = pd.Series(np.linspace(100, 110, 100), index=dates)

    # This should resample to business days
    forecast = ewmac_calc_vol(price, Lfast=16, resample_bd=True)

    # Business days between 2020-01-01 and 100 days later
    expected_index = price.resample("1B").last().index
    pd.testing.assert_index_equal(forecast.index, expected_index)
