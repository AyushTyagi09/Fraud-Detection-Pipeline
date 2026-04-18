import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect("Data/transactions.db")

# load processed data
df = pd.read_sql("SELECT * FROM processed_transactions", conn)

# save as CSV
df.to_csv("processed_transactions.csv", index=False)

# close connection
conn.close()

print("CSV created successfully!")