import pandas as pd

def get_data_batches(file_path, batch_size=5000):
    return pd.read_csv(file_path, chunksize=batch_size)