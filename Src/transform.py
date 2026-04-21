
# ============================================================
#  transform.py — Feature engineering & fraud detection logic
# ============================================================

import pandas as pd
import numpy as np
from config import CONFIG


def transform_data(df):
    """
    Applies feature engineering on a raw batch.
    Returns a transformed copy of the DataFrame.
    """

    # BUG FIX: Always work on a copy — never mutate original batch
    df = df.copy()

    # ----------------------------------------------------------
    # 1. Amount category
    # ----------------------------------------------------------
    df['amount_category'] = pd.cut(
        df['Amount'],
        bins=[0, 100, 1000, 5000, 100000],
        labels=['low', 'medium', 'high', 'very_high']
    )

    # ----------------------------------------------------------
    # 2. Z-score anomaly detection
    # ----------------------------------------------------------
    mean = df['Amount'].mean()
    std  = df['Amount'].std()
    std  = std if std > 0 else 1  # prevent division by zero

    df['amount_zscore'] = (df['Amount'] - mean) / std
    df['anomaly_flag']  = df['amount_zscore'].abs() > CONFIG["zscore_threshold"]

    # ----------------------------------------------------------
    # 3. High amount rule
    # ----------------------------------------------------------
    df['high_amount_flag'] = df['Amount'] > CONFIG["high_amount_limit"]

    # ----------------------------------------------------------
    # 4. Velocity flag
    #    BUG FIX: min_periods=1 prevents NaN at batch start
    # ----------------------------------------------------------
    df['velocity_flag'] = (
        df['Amount']
        .rolling(window=CONFIG["velocity_window"], min_periods=1)
        .mean() > CONFIG["velocity_threshold"]
    )

    # ----------------------------------------------------------
    # 5. Weighted risk score
    # ----------------------------------------------------------
    df['risk_score'] = (
        (df['high_amount_flag'].astype(int) * CONFIG["weight_high_amount"]) +
        (df['anomaly_flag'].astype(int)     * CONFIG["weight_anomaly"])     +
        (df['velocity_flag'].astype(int)    * CONFIG["weight_velocity"])    +
        (df['Class']                        * CONFIG["weight_class"])
    )

    # ----------------------------------------------------------
    # 6. Final fraud detection label
    # ----------------------------------------------------------
    df['is_fraud_detected'] = df['risk_score'] > CONFIG["fraud_threshold"]

    return df
