import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect(r"C:\Users\Hp\Desktop\Fraud-Detection-Dashboard\Data\transactions.db")

# Export processed transactions
df = pd.read_sql("SELECT * FROM processed_transactions", conn)
df.to_csv(r"C:\Users\Hp\Desktop\Fraud-Detection-Dashboard\Data\exports\processed_transactions.csv", index=False)
print("✅ processed_transactions.csv created!")

# Export fraud alerts
fraud_df = pd.read_sql("SELECT * FROM fraud_alerts", conn)
fraud_df.to_csv(r"C:\Users\Hp\Desktop\Fraud-Detection-Dashboard\Data\exports\fraud_alerts.csv", index=False)
print("✅ fraud_alerts.csv created!")

conn.close()
print("\n📁 All files saved to Data/exports/")