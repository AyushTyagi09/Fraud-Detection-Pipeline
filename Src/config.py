
# ============================================================
#  config.py — Central configuration for the pipeline
# ============================================================

CONFIG = {
    # Paths
    "file_path"      : "../Data/raw/creditcard.csv",
    "db_path"        : "../Data/transactions.db",
    "log_path"       : "../logs/pipeline.log",
    "export_path"    : "../Data/exports/fraud_summary.csv",

    # Pipeline settings
    "batch_size"     : 5000,

    # Fraud detection thresholds
    "fraud_threshold"      : 0.5,
    "high_amount_limit"    : 2000,
    "zscore_threshold"     : 3,
    "velocity_window"      : 5,
    "velocity_threshold"   : 1500,

    # Risk score weights (must add up to 1.0)
    "weight_high_amount"   : 0.3,
    "weight_anomaly"       : 0.3,
    "weight_velocity"      : 0.2,
    "weight_class"         : 0.2,
}
