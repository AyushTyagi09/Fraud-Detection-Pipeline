-- ============================================================
--  queries.sql — Analytics queries for Power BI dashboard
-- ============================================================


-- 1. Total transactions
SELECT COUNT(*) AS total_transactions
FROM processed_transactions;


-- 2. Total fraud cases
SELECT COUNT(*) AS total_fraud
FROM fraud_alerts;


-- 3. Fraud rate (%)
SELECT
    ROUND(
        (SELECT COUNT(*) FROM fraud_alerts) * 100.0 /
        (SELECT COUNT(*) FROM processed_transactions),
    2) AS fraud_rate_percent;


-- 4. Fraud vs Non-Fraud count (for pie/bar chart)
SELECT
    is_fraud_detected,
    COUNT(*) AS transaction_count
FROM processed_transactions
GROUP BY is_fraud_detected;


-- 5. Fraud by amount category (bar chart)
SELECT
    amount_category,
    COUNT(*) AS fraud_count
FROM fraud_alerts
GROUP BY amount_category
ORDER BY fraud_count DESC;


-- 6. Average risk score
SELECT ROUND(AVG(risk_score), 4) AS avg_risk_score
FROM processed_transactions;


-- 7. Risk score distribution buckets (histogram)
SELECT
    CASE
        WHEN risk_score = 0          THEN '0.0'
        WHEN risk_score <= 0.2       THEN '0.0-0.2'
        WHEN risk_score <= 0.4       THEN '0.2-0.4'
        WHEN risk_score <= 0.6       THEN '0.4-0.6'
        WHEN risk_score <= 0.8       THEN '0.6-0.8'
        ELSE '0.8-1.0'
    END AS risk_bucket,
    COUNT(*) AS count
FROM processed_transactions
GROUP BY risk_bucket
ORDER BY risk_bucket;


-- 8. Top 10 highest risk transactions (table visual)
SELECT
    Time,
    Amount,
    risk_score,
    amount_category,
    anomaly_flag,
    velocity_flag
FROM processed_transactions
ORDER BY risk_score DESC
LIMIT 10;


-- 9. Fraud amount stats (KPI cards)
SELECT
    MIN(Amount)          AS min_fraud_amount,
    MAX(Amount)          AS max_fraud_amount,
    ROUND(AVG(Amount), 2) AS avg_fraud_amount,
    ROUND(SUM(Amount), 2) AS total_fraud_amount
FROM fraud_alerts;


-- 10. Anomaly flag summary
SELECT
    anomaly_flag,
    COUNT(*) AS count
FROM processed_transactions
GROUP BY anomaly_flag;
