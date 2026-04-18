import sqlite3

def load_data(df):

    conn = sqlite3.connect("Data/transactions.db")

    # 1. Raw data (as is)
    df.to_sql("raw_transactions", conn, if_exists="append", index=False)

    # 2. Processed data
    df.to_sql("processed_transactions", conn, if_exists="append", index=False)

    # 3. Fraud alerts (filtered)
    fraud_df = df[df['is_fraud_detected'] == True]
    fraud_df.to_sql("fraud_alerts", conn, if_exists="append", index=False)

    conn.close()