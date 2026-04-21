
# ============================================================
#  load.py — Loads data into SQLite (3 separate tables)
# ============================================================

import sqlite3
from config import CONFIG


def load_raw(df):
    """
    Saves the original untransformed batch to raw_transactions.
    Called BEFORE transform_data() in pipeline.py.
    """
    conn = sqlite3.connect(CONFIG["db_path"])
    df.to_sql("raw_transactions", conn, if_exists="append", index=False)
    conn.close()


def load_processed(df):
    """
    Saves the transformed batch to processed_transactions.
    Also extracts and saves fraud alerts to fraud_alerts table.
    """
    conn = sqlite3.connect(CONFIG["db_path"])

    # Full transformed data
    df.to_sql("processed_transactions", conn, if_exists="append", index=False)

    # Only fraud rows
    fraud_df = df[df['is_fraud_detected'] == True]
    if not fraud_df.empty:
        fraud_df.to_sql("fraud_alerts", conn, if_exists="append", index=False)

    conn.close()
