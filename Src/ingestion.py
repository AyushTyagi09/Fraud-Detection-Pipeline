
# ============================================================
#  ingestion.py — Reads CSV in batches
# ============================================================

import pandas as pd
from config import CONFIG


def get_data_batches(file_path=None, batch_size=None):
    """
    Reads the CSV file in chunks to handle large datasets efficiently.
    Returns a generator of DataFrames.
    """
    file_path  = file_path  or CONFIG["file_path"]
    batch_size = batch_size or CONFIG["batch_size"]

    return pd.read_csv(file_path, chunksize=batch_size)
