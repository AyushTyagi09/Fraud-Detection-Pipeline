
# ============================================================
#  summary_report.py — Generates summary after pipeline runs
# ============================================================

import sqlite3
import pandas as pd
from config import CONFIG


def generate_report():

    conn = sqlite3.connect(CONFIG["db_path"])

    # ----------------------------------------------------------
    # Core stats
    # ----------------------------------------------------------
    total = pd.read_sql(
        "SELECT COUNT(*) as cnt FROM processed_transactions", conn
    ).iloc[0, 0]

    fraud = pd.read_sql(
        "SELECT COUNT(*) as cnt FROM fraud_alerts", conn
    ).iloc[0, 0]

    fraud_rate = round(fraud / total * 100, 2) if total > 0 else 0

    avg_risk = pd.read_sql(
        "SELECT ROUND(AVG(risk_score), 4) as avg FROM processed_transactions", conn
    ).iloc[0, 0]

    # ----------------------------------------------------------
    # Fraud by amount category
    # ----------------------------------------------------------
    category_df = pd.read_sql("""
        SELECT amount_category, COUNT(*) as fraud_count
        FROM fraud_alerts
        GROUP BY amount_category
        ORDER BY fraud_count DESC
    """, conn)

    # ----------------------------------------------------------
    # Top 5 highest risk transactions
    # ----------------------------------------------------------
    top_risk_df = pd.read_sql("""
        SELECT Time, Amount, risk_score, amount_category, is_fraud_detected
        FROM processed_transactions
        ORDER BY risk_score DESC
        LIMIT 5
    """, conn)

    conn.close()

    # ----------------------------------------------------------
    # Print report
    # ----------------------------------------------------------
    print("\n" + "=" * 50)
    print("       FRAUD DETECTION — SUMMARY REPORT")
    print("=" * 50)
    print(f"  Total Transactions : {total:,}")
    print(f"  Fraud Detected     : {fraud:,}")
    print(f"  Fraud Rate         : {fraud_rate}%")
    print(f"  Avg Risk Score     : {avg_risk}")
    print("\n--- Fraud by Amount Category ---")
    print(category_df.to_string(index=False))
    print("\n--- Top 5 Highest Risk Transactions ---")
    print(top_risk_df.to_string(index=False))
    print("=" * 50)

    # ----------------------------------------------------------
    # Export to CSV for Power BI
    # ----------------------------------------------------------
    category_df.to_csv(CONFIG["export_path"], index=False)
    print(f"\n📁 Summary exported to: {CONFIG['export_path']}")


if __name__ == "__main__":
    generate_report()
