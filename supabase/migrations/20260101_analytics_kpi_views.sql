-- =====================================================================
-- Abaco Analytics – Base + KPI Views
-- Schema: analytics
-- =====================================================================

BEGIN;

CREATE SCHEMA IF NOT EXISTS analytics;

SET search_path TO public, analytics;

-- ---------------------------------------------------------------------
-- 1. CUSTOMER SEGMENT VIEW
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.customer_segment AS
WITH src AS (
    SELECT
        COALESCE(c.customer_id::text, '') AS customer_id,
        LOWER(COALESCE(c.segment, '')) AS segment_raw,
        COALESCE(c.subcategoria_linea, '') AS subcategoria_linea,
        COALESCE(c.kam_id, '') AS kam_id,
        COALESCE(c.industry, '') AS industry_code
    FROM customer_data c
)
SELECT
    customer_id,
    segment_raw AS segment_source,
    subcategoria_linea,
    kam_id,
    industry_code,
    CASE
        WHEN segment_raw = 'gob' THEN 'Gob'
        ELSE 'Private'
    END AS sector_segment,
    CASE
        WHEN segment_raw = 'oc' THEN 'OC'
        WHEN segment_raw = 'top' THEN 'Top'
        WHEN subcategoria_linea ILIKE '%ccf%' THEN 'CCF'
        WHEN subcategoria_linea ILIKE '%dte%' THEN 'DTE'
        WHEN segment_raw = 'nimal' THEN 'Nimal'
        ELSE 'Other'
    END AS business_segment
FROM src;

-- ---------------------------------------------------------------------
-- 2. LOAN_MONTH VIEW
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.loan_month AS
WITH month_ends AS (
    SELECT
        (date_trunc('month', d) + INTERVAL '1 month - 1 day')::date AS month_end
    FROM generate_series('2024-01-01'::date, '2025-12-31'::date, INTERVAL '1 month') AS d
),
principal_cum AS (
    SELECT
        loan_id,
        true_payment_date::date AS pay_date,
        SUM(true_principal_payment) OVER (PARTITION BY loan_id ORDER BY true_payment_date) AS cum_principal
    FROM real_payment
),
loan_month AS (
    SELECT
        m.month_end,
        l.loan_id AS loan_id,
        l.customer_id AS customer_id,
        l.disbursement_amount AS disbursement_amount,
        l.interest_rate_apr AS interest_rate_apr,
        l.origination_fee AS origination_fee,
        l.origination_fee_taxes AS origination_fee_taxes,
        l.disbursement_date::date AS disbursement_date,
                (l.disbursement_amount - COALESCE(
                    (SELECT pc.cum_principal 
                     FROM principal_cum pc 
                     WHERE pc.loan_id = l.loan_id AND pc.pay_date <= m.month_end 
                     ORDER BY pc.pay_date DESC LIMIT 1), 0)
                ) AS outstanding,
                l.days_past_due AS days_past_due
        FROM month_ends m
        JOIN loan_data l ON m.month_end >= l.disbursement_date::date
)
SELECT * FROM loan_month;

-- ---------------------------------------------------------------------
-- 3. PRICING KPI VIEW
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.kpi_monthly_pricing AS
WITH income_per_loan AS (
    SELECT
        loan_id,
        SUM(COALESCE(true_interest_payment, 0)) AS total_int,
        SUM(COALESCE(true_fee_payment, 0))      AS total_fee,
        SUM(COALESCE(true_other_payment, 0))    AS total_other,
        SUM(COALESCE(true_tax_payment, 0))      AS total_tax,
        SUM(COALESCE(true_fee_tax_payment, 0))  AS total_fee_tax,
        SUM(COALESCE(true_rebates, 0))          AS total_rebates
    FROM real_payment
    GROUP BY 1
),
loan_rates AS (
    SELECT
        lm.month_end,
        lm.loan_id,
        lm.outstanding,
        lm.interest_rate_apr AS apr,
        (lm.origination_fee + lm.origination_fee_taxes)
            / NULLIF(lm.disbursement_amount, 0)      AS fee_rate,
        (
            (COALESCE(i.total_fee, 0)
            + COALESCE(i.total_other, 0)
            + COALESCE(i.total_tax, 0)
            + COALESCE(i.total_fee_tax, 0)
            - COALESCE(i.total_rebates, 0))
            / NULLIF(lm.disbursement_amount, 0)
        )                                           AS other_income_rate
    FROM analytics.loan_month lm
    LEFT JOIN income_per_loan i
      ON i.loan_id = lm.loan_id
)
SELECT
    month_end                           AS year_month,
    SUM(apr * outstanding)
        / NULLIF(SUM(outstanding), 0)   AS weighted_apr,
    SUM(fee_rate * outstanding)
        / NULLIF(SUM(outstanding), 0)   AS weighted_fee_rate,
    SUM(other_income_rate * outstanding)
        / NULLIF(SUM(outstanding), 0)   AS weighted_other_income_rate,
    SUM((apr + fee_rate + other_income_rate) * outstanding)
        / NULLIF(SUM(outstanding), 0)   AS weighted_effective_rate
FROM loan_rates
WHERE outstanding > 0
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------
-- 4. RISK KPI VIEW
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.kpi_monthly_risk AS
SELECT
    month_end AS year_month,
    SUM(outstanding) AS total_outstanding,

    SUM(CASE WHEN days_past_due >= 7  THEN outstanding ELSE 0 END) AS dpd7_amount,
    SUM(CASE WHEN days_past_due >= 7  THEN outstanding ELSE 0 END)
        / NULLIF(SUM(outstanding),0)                               AS dpd7_pct,

    SUM(CASE WHEN days_past_due >= 15 THEN outstanding ELSE 0 END) AS dpd15_amount,
    SUM(CASE WHEN days_past_due >= 15 THEN outstanding ELSE 0 END)
        / NULLIF(SUM(outstanding),0)                               AS dpd15_pct,

    SUM(CASE WHEN days_past_due >= 30 THEN outstanding ELSE 0 END) AS dpd30_amount,
    SUM(CASE WHEN days_past_due >= 30 THEN outstanding ELSE 0 END)
        / NULLIF(SUM(outstanding),0)                               AS dpd30_pct,

    SUM(CASE WHEN days_past_due >= 60 THEN outstanding ELSE 0 END) AS dpd60_amount,
    SUM(CASE WHEN days_past_due >= 60 THEN outstanding ELSE 0 END)
        / NULLIF(SUM(outstanding),0)                               AS dpd60_pct,

    SUM(CASE WHEN days_past_due >= 90 THEN outstanding ELSE 0 END) AS dpd90_amount,
    SUM(CASE WHEN days_past_due >= 90 THEN outstanding ELSE 0 END)
        / NULLIF(SUM(outstanding),0)                               AS default_pct
FROM analytics.loan_month
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------
-- 5. CUSTOMER TYPES KPI VIEW
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.kpi_customer_types AS
WITH ranked_loans AS (
    SELECT
        customer_id,
        disbursement_date::date AS disbursement_date,
        disbursement_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY disbursement_date) AS rn,
        LAG(disbursement_date::date) OVER (PARTITION BY customer_id ORDER BY disbursement_date) AS prev_disb
    FROM loan_data
),
classified AS (
    SELECT
        customer_id,
        disbursement_date,
        disbursement_amount,
        CASE
            WHEN rn = 1 THEN 'New'
            WHEN prev_disb IS NOT NULL AND (disbursement_date - prev_disb) > 180 THEN 'Reactivated'
            ELSE 'Recurrent'
        END AS customer_type
    FROM ranked_loans
)
SELECT
    (date_trunc('month', disbursement_date) + INTERVAL '1 month - 1 day')::date AS year_month,
    customer_type,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(disbursement_amount) AS disbursement_amount
FROM classified
GROUP BY 1, 2
ORDER BY 1, 2;

COMMIT;
