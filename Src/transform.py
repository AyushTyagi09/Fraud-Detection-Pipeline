import pandas as pd
import numpy as np

def transform_data(df):

    # ---------------------------
    # 1. Amount category
    # ---------------------------
    df['amount_category'] = pd.cut(
        df['Amount'],
        bins=[0, 100, 1000, 5000, 100000],
        labels=['low', 'medium', 'high', 'very_high']
    )

    # ---------------------------
    # 2. Z-score (statistical anomaly)
    # ---------------------------
    mean = df['Amount'].mean()
    std = df['Amount'].std()

    df['amount_zscore'] = (df['Amount'] - mean) / std
    df['anomaly_flag'] = df['amount_zscore'].abs() > 3

    # ---------------------------
    # 3. High amount rule
    # ---------------------------
    df['high_amount_flag'] = df['Amount'] > 2000

    # ---------------------------
    # 4. Behavioral simulation (NEW 🔥)
    # ---------------------------
    df['velocity_flag'] = df['Amount'].rolling(window=5).mean() > 1500

    # ---------------------------
    # 5. Risk score (improved)
    # ---------------------------
    df['risk_score'] = (
        (df['high_amount_flag'].astype(int) * 0.3) +
        (df['anomaly_flag'].astype(int) * 0.3) +
        (df['velocity_flag'].astype(int) * 0.2) +
        (df['Class'] * 0.2)
    )

    # ---------------------------
    # 6. Final fraud detection
    # ---------------------------
    df['is_fraud_detected'] = df['risk_score'] > 0.5

    return df