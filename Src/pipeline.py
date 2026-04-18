from ingestion import get_data_batches
from transform import transform_data
from load import load_data

import time
import logging

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():

    logging.info("Pipeline started")

    batches = get_data_batches("Data/raw/creditcard.csv", batch_size=5000)

    for i, batch in enumerate(batches):
        logging.info(f"Processing batch {i}")

        transformed = transform_data(batch)
        load_data(transformed)

        logging.info(f"Completed batch {i}")

        time.sleep(2)  # simulate real-time

    logging.info("Pipeline completed")


if __name__ == "__main__":
    run_pipeline()