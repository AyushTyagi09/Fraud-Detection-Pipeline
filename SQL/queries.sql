-- Total transactions
SELECT COUNT(*) AS total_transactions FROM processed_transactions;

-- Total fraud cases
SELECT COUNT(*) AS total_fraud FROM fraud_alerts;

-- Fraud rate
SELECT 
    (SELECT COUNT(*) FROM fraud_alerts) * 100.0 /
    (SELECT COUNT(*) FROM processed_transactions) AS fraud_rate;

-- High risk transactions
SELECT *
FROM processed_transactions
ORDER BY risk_score DESC
LIMIT 10;