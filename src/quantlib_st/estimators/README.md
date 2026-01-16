# estimators

Small, focused estimators for volatility and signal scaling.

## Volatility Estimators (`vol.py`)

- **robust_vol_calc** — Robust exponential volatility estimator for daily returns. Uses EWM std with an absolute minimum and an optional volatility floor.
- **mixed_vol_calc** — Blending short-term (robust) vol with a long-term slow vol component.

### Usage

```python
from quantlib_st.estimators.vol import robust_vol_calc
vol = robust_vol_calc(returns_series)
```

## Forecast Scaling (`forecast_scalar.py`)

In this modular framework, a **forecast** is a standardized number where positive values indicate a buy signal and negative values indicate a short signal.

To ensure proper risk control and prevent any single rule from dominating the portfolio's returns, all forecasts are eventually **capped within the range of -20 to +20**.

### Why a Forecast Scalar is Necessary

To convert any trading rule output into this specific scale, we use a forecast scalar to ensure that the "average" signal has an expected absolute value of **10.0**.

- **+10.0**: Represents an average buy.
- **+20.0**: Represents a very strong buy (the cap).
- **0.0**: Represents a neutral or weak signal.

This consistency allows the rest of the framework—such as position sizing and volatility targeting—to function correctly without needing redesign for every new rule.

### How to Calculate and Apply the Scalar

The forecast scalar is a fixed multiplier used to convert the "raw" output of a trading rule (e.g., price differences, moving average crossovers) into this standardized interface.

1.  **Measure the Average**: Calculate the average absolute value of the raw forecast outputs across a wide backtest of various instruments.
2.  **The Formula**:
    $$\text{Scalar} = \frac{\text{Target Average Absolute Forecast (10.0)}}{\text{Measured Average Absolute Raw Output}}$$
3.  **Example**: If a rule naturally generates an average absolute output of 0.33, the forecast scalar would be **30** ($10 / 0.33 \approx 30$).

### Common Scalar Examples

Different rules require unique scalars based on their mathematical sensitivity:

- **EWMAC Rules**: Variations like EWMAC 2,8 might use a scalar of ~10.6, while the slower EWMAC 64,256 uses ~1.87.
- **Carry Rule**: Raw carry measures (which act like annualized Sharpe ratios) typically require a scalar of approximately **30**.

### Usage

```python
from quantlib_st.estimators.forecast_scalar import forecast_scalar

# cs_forecasts: TxN DataFrame of raw, unscaled signals across multiple instruments
scalar_series = forecast_scalar(cs_forecasts, target_abs_forecast=10.0)

# Apply to raw signal
scaled_forecast = raw_signal * scalar_series
```

---

## Notes

- If you have price data for volatility estimation, use `robust_daily_vol_given_price(price_series)` which resamples to business days and computes differences to produce daily returns.
- `forecast_scalar` supports an `estimated` mode where the scalar is computed on a rolling basis, or it can be used on a full backtest to find a fixed value for configuration.
