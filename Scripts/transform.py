import pandas as pd

# Load data
file_path = "C:/Users/Hp/Desktop/Fraud-Detection-Dashboard/Data/raw/transactions.csv"
df = pd.read_csv(file_path)

# ---------------- CLEANING ---------------- #

# 1. Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 2. Standardize location (lowercase)
df['location'] = df['location'].str.lower()

# 3. Remove duplicates (if any)
df = df.drop_duplicates()

# 4. Create new feature: transaction_hour
df['transaction_hour'] = df['timestamp'].dt.hour

# 5. Create new feature: high_value_transaction
df['high_value'] = df['amount'].apply(lambda x: 1 if x > 50000 else 0)

# ---------------- SAVE CLEAN DATA ---------------- #

output_path = "C:/Users/Hp/Desktop/Fraud-Detection-Dashboard/Data/processed/clean_transactions.csv"
df.to_csv(output_path, index=False)

print("Data cleaned and saved successfully!")
print(df.head())