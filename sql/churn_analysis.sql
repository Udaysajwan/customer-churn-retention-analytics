-- =====================================================================
-- Customer Churn & Retention Analytics - Enterprise SQL Analysis Suite
-- Domain: Telecommunications & Subscription Services
-- Database Dialect: Standard ANSI SQL (Compatible with PostgreSQL, BigQuery, Snowflake, SQLite)
-- =====================================================================

-- ---------------------------------------------------------------------
-- TABLE CREATION & SCHEMA DEFINITION
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customer_churn (
    CustomerID              VARCHAR(20) PRIMARY KEY,
    Tenure_Months           INTEGER NOT NULL,
    Contract_Type           VARCHAR(30) NOT NULL,
    Monthly_Charges         DECIMAL(10, 2) NOT NULL,
    Total_Charges           DECIMAL(10, 2) NOT NULL,
    Payment_Method          VARCHAR(50) NOT NULL,
    Tech_Support_Tickets    INTEGER NOT NULL,
    Internet_Service_Type   VARCHAR(30) NOT NULL,
    Paperless_Billing       VARCHAR(5) NOT NULL,
    Churn_Status            VARCHAR(5) NOT NULL
);

-- =====================================================================
-- QUERY 1: EXECUTIVE KPI SUMMARY
-- Computes overall customer base, churned customers, global churn rate,
-- Total Monthly Recurring Revenue (MRR), and Total MRR Lost.
-- =====================================================================
WITH kpi_metrics AS (
    SELECT
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS retained_customers,
        ROUND(AVG(CASE WHEN Churn_Status = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
        ROUND(SUM(Monthly_Charges), 2) AS total_mrr,
        ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost,
        ROUND(AVG(Monthly_Charges), 2) AS overall_arpu
    FROM customer_churn
)
SELECT 
    total_customers,
    churned_customers,
    retained_customers,
    churn_rate_pct,
    total_mrr,
    mrr_lost,
    ROUND((mrr_lost / total_mrr) * 100, 2) AS mrr_lost_percentage,
    overall_arpu
FROM kpi_metrics;


-- =====================================================================
-- QUERY 2: KEY FINDING 1 - CHURN BY CONTRACT TYPE
-- Validates: Month-to-month holders are ~4x more likely to churn than two-year holders.
-- =====================================================================
WITH contract_stats AS (
    SELECT
        Contract_Type,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(AVG(CASE WHEN Churn_Status = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
        ROUND(SUM(Monthly_Charges), 2) AS cohort_mrr,
        ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost,
        ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charge
    FROM customer_churn
    GROUP BY Contract_Type
)
SELECT
    Contract_Type,
    total_customers,
    churned_customers,
    churn_rate_pct,
    cohort_mrr,
    mrr_lost,
    avg_monthly_charge,
    ROUND(churn_rate_pct / MIN(churn_rate_pct) OVER (), 2) AS churn_risk_multiplier
FROM contract_stats
ORDER BY churn_rate_pct DESC;


-- =====================================================================
-- QUERY 3: KEY FINDING 2 - CHURN RATE BY TECH SUPPORT TICKETS
-- Validates: Customers with >3 tickets show an ~82% churn probability.
-- =====================================================================
SELECT
    Tech_Support_Tickets,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(AVG(CASE WHEN Churn_Status = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
    CASE 
        WHEN Tech_Support_Tickets > 3 THEN 'CRITICAL RISK (>3 Tickets)'
        WHEN Tech_Support_Tickets = 3 THEN 'ELEVATED RISK (3 Tickets)'
        ELSE 'NORMAL RISK (0-2 Tickets)'
    END AS risk_classification,
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost
FROM customer_churn
GROUP BY Tech_Support_Tickets
ORDER BY Tech_Support_Tickets ASC;


-- =====================================================================
-- QUERY 4: KEY FINDING 3 - AUTOMATIC VS. MANUAL PAYMENT METHODS
-- Validates: Opting for automatic payment methods reduces churn by ~28%.
-- =====================================================================
WITH payment_aggregation AS (
    SELECT
        Payment_Method,
        CASE 
            WHEN Payment_Method LIKE '%automatic%' THEN 'Automatic Payment'
            ELSE 'Manual / Check Payment'
        END AS payment_category,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(AVG(CASE WHEN Churn_Status = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost
    FROM customer_churn
    GROUP BY Payment_Method
),
category_aggregation AS (
    SELECT
        payment_category,
        SUM(total_customers) AS category_customers,
        SUM(churned_customers) AS category_churned,
        ROUND(AVG(churn_rate_pct), 2) AS avg_churn_rate_pct,
        ROUND(SUM(mrr_lost), 2) AS category_mrr_lost
    FROM payment_aggregation
    GROUP BY payment_category
)
SELECT 
    p.Payment_Method,
    p.payment_category,
    p.total_customers,
    p.churned_customers,
    p.churn_rate_pct,
    p.mrr_lost,
    c.avg_churn_rate_pct AS category_avg_churn_rate
FROM payment_aggregation p
JOIN category_aggregation c ON p.payment_category = c.payment_category
ORDER BY p.churn_rate_pct DESC;


-- =====================================================================
-- QUERY 5: COHORT ANALYSIS - TENURE BANDS & INTERNET SERVICE TYPE
-- Window functions calculating cumulative MRR lost and percentage contribution.
-- =====================================================================
WITH cohort_data AS (
    SELECT
        CASE 
            WHEN Tenure_Months BETWEEN 0 AND 12 THEN '01. 0-12 Months'
            WHEN Tenure_Months BETWEEN 13 AND 24 THEN '02. 13-24 Months'
            WHEN Tenure_Months BETWEEN 25 AND 48 THEN '03. 25-48 Months'
            ELSE '04. 49-72 Months'
        END AS tenure_band,
        Internet_Service_Type,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(AVG(CASE WHEN Churn_Status = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS segment_mrr_lost
    FROM customer_churn
    GROUP BY 
        CASE 
            WHEN Tenure_Months BETWEEN 0 AND 12 THEN '01. 0-12 Months'
            WHEN Tenure_Months BETWEEN 13 AND 24 THEN '02. 13-24 Months'
            WHEN Tenure_Months BETWEEN 25 AND 48 THEN '03. 25-48 Months'
            ELSE '04. 49-72 Months'
        END,
        Internet_Service_Type
)
SELECT
    tenure_band,
    Internet_Service_Type,
    total_customers,
    churned_customers,
    churn_rate_pct,
    segment_mrr_lost,
    ROUND(SUM(segment_mrr_lost) OVER (PARTITION BY tenure_band), 2) AS tenure_band_total_mrr_lost,
    ROUND(segment_mrr_lost / SUM(segment_mrr_lost) OVER () * 100, 2) AS pct_of_global_mrr_lost
FROM cohort_data
ORDER BY tenure_band ASC, segment_mrr_lost DESC;


-- =====================================================================
-- QUERY 6: TARGET RETENTION INTERVENTION COHORT (PRIORITY CAMPAIGN)
-- Step 5 Implementation: Extracts high-value at-risk customers (Tenure < 12m & Tickets > 3)
-- with priority ranking for proactive outreach.
-- =====================================================================
WITH high_risk_cohort AS (
    SELECT
        CustomerID,
        Tenure_Months,
        Contract_Type,
        Monthly_Charges,
        Tech_Support_Tickets,
        Internet_Service_Type,
        Payment_Method,
        ROUND(Monthly_Charges * 12, 2) AS annual_projected_value,
        ROW_NUMBER() OVER (ORDER BY Monthly_Charges DESC, Tech_Support_Tickets DESC) AS outreach_priority_rank
    FROM customer_churn
    WHERE Tenure_Months < 12 
      AND Tech_Support_Tickets > 3
      AND Churn_Status = 'No' -- Currently active but at imminent 82% risk
)
SELECT 
    outreach_priority_rank,
    CustomerID,
    Tenure_Months,
    Contract_Type,
    Tech_Support_Tickets,
    Monthly_Charges,
    annual_projected_value,
    Internet_Service_Type,
    Payment_Method,
    'Urgent Concierge Outreach + $20 Discount Offer' AS recommended_action
FROM high_risk_cohort
ORDER BY outreach_priority_rank ASC
LIMIT 50;
