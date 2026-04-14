import pandas as pd
import sqlite3

# Load cleaned data (FIXED)
df = pd.read_csv("C:/Users/Hp/Desktop/Fraud-Detection-Dashboard/Data/processed/clean_transactions.csv")

# Connect to SQLite database
conn = sqlite3.connect("C:/Users/Hp/Desktop/Fraud-Detection-Dashboard/Data/transactions.db")

# Load data into table
df.to_sql("transactions", conn, if_exists="replace", index=False)

print("Data loaded into SQL successfully!")

conn.close()