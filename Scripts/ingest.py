import pandas as pd

# Load data
file_path = "C:/Users/Hp/Desktop/Fraud-Detection-Dashboard/Data/raw/transactions.csv"
df = pd.read_csv(file_path)

# Show first 5 rows
print("First 5 rows:")
print(df.head())

# Show basic info
print("\nDataset Info:")
print(df.info())