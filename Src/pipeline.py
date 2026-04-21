
# ============================================================
#  pipeline.py — Main ETL orchestrator
# ============================================================

import time
import logging
import os

from ingestion import get_data_batches
from transform  import transform_data
from load       import load_raw, load_processed
from config     import CONFIG

# ----------------------------------------------------------
# Setup logging
# ----------------------------------------------------------
os.makedirs("logs", exist_ok=True)
os.makedirs("Data/exports", exist_ok=True)

logging.basicConfig(
    filename=CONFIG["log_path"],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    logging.info("=" * 50)
    logging.info("PIPELINE STARTED")
    logging.info("=" * 50)

    total_rows       = 0
    total_fraud      = 0
    failed_batches   = 0

    batches = get_data_batches()

    for i, batch in enumerate(batches):
        try:
            rows = len(batch)
            logging.info(f"Batch {i} started | Rows: {rows}")

            # BUG FIX: Save raw BEFORE transforming
            load_raw(batch)

            # Transform
            transformed = transform_data(batch)

            # Save processed + fraud alerts
            load_processed(transformed)

            fraud_count  = int(transformed['is_fraud_detected'].sum())
            total_rows  += rows
            total_fraud += fraud_count

            logging.info(
                f"Batch {i} completed | "
                f"Rows: {rows} | "
                f"Fraud detected: {fraud_count} | "
                f"Fraud rate: {round(fraud_count / rows * 100, 2)}%"
            )

            time.sleep(0.5)  # simulate near real-time processing

        except Exception as e:
            failed_batches += 1
            logging.error(f"Batch {i} FAILED: {str(e)}")
            continue  # skip bad batch, don't crash entire pipeline

    # ----------------------------------------------------------
    # Final summary log
    # ----------------------------------------------------------
    logging.info("=" * 50)
    logging.info("PIPELINE COMPLETED")
    logging.info(f"Total rows processed : {total_rows}")
    logging.info(f"Total fraud detected : {total_fraud}")
    logging.info(f"Overall fraud rate   : {round(total_fraud / total_rows * 100, 2)}%")
    logging.info(f"Failed batches       : {failed_batches}")
    logging.info("=" * 50)

    print(f"\n✅ Pipeline complete!")
    print(f"   Rows processed : {total_rows}")
    print(f"   Fraud detected : {total_fraud}")
    print(f"   Fraud rate     : {round(total_fraud / total_rows * 100, 2)}%")


if __name__ == "__main__":
    run_pipeline()
