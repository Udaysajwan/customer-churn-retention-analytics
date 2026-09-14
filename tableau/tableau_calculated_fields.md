# Tableau Dashboard Guide: Customer Churn & Retention Analytics

This guide provides data analysts and BI developers with calculated field formulas, data modeling details, and layout architecture to build a portfolio-grade Tableau dashboard using `tableau_churn_dataset.csv`.

---

## 1. Data Source Details
- **File**: `tableau/tableau_churn_dataset.csv`
- **Total Records**: 10,000 customers
- **Target Variable**: `Churn_Status` (`Yes` / `No`)

---

## 2. Tableau Calculated Fields (Formulas)

### Metric 1: Customer Churn Rate (%)
```tableau
// Churn Rate
SUM([Churn_Numeric]) / COUNT([CustomerID])
```
*Format*: Percentage, 1 decimal place (`32.5%`).

### Metric 2: Monthly Recurring Revenue (MRR)
```tableau
// Total MRR
SUM([Monthly_Charges])
```
*Format*: Currency (Standard USD, `$666.5K`).

### Metric 3: Monthly Recurring Revenue Lost (MRR Lost)
```tableau
// MRR Lost to Attrition
SUM(IF [Churn_Status] = 'Yes' THEN [Monthly_Charges] ELSE 0 END)
```
*Format*: Currency (Standard USD, `$231.9K`).

### Metric 4: MRR Loss Ratio (%)
```tableau
// Percent of MRR Lost
[MRR Lost] / [Total MRR]
```
*Format*: Percentage, 1 decimal place (`34.8%`).

### Metric 5: Average Revenue Per User (ARPU)
```tableau
// ARPU
AVG([Monthly_Charges])
```
*Format*: Currency (USD, `$66.65`).

### Metric 6: Customer Lifetime Value (CLV)
```tableau
// Customer Lifetime Value (Assuming 75% Gross Margin & Annual Churn)
([ARPU] * 0.75) / ([Churn Rate] / 12)
```
*Format*: Currency (USD, `$1,848`).

### Dimension 7: Attrition Risk Multiplier (LOD Calculation)
```tableau
// Risk Multiplier vs. Baseline (Two-Year Contract)
[Churn Rate] / { FIXED : SUM(IF [Contract_Type] = 'Two year' THEN [Churn_Numeric] END) / SUM(IF [Contract_Type] = 'Two year' THEN 1 END) }
```

### Dimension 8: High-Risk Cohort Indicator
```tableau
// Priority Retention Campaign Target
IF [Tenure_Months] < 12 AND [Tech_Support_Tickets] > 3 THEN 'Target Retention Cohort'
ELSE 'Standard Cohort'
END
```

---

## 3. Recommended Tableau Dashboard Architecture

### View A: Executive Summary KPI Strip (Top Row)
1. **Total Customer Base**: `10,000`
2. **Overall Churn Rate**: `32.5%`
3. **Total MRR Lost**: `$231.9K / month`
4. **Estimated Lifetime Value Lost**: `$6.43M`
5. **Campaign ROI**: `175.5%`

### View B: Behavioral Root Cause Analysis (Middle Row)
1. **Contract Type Breakdown (Bar Chart)**:
   - Rows: `Contract_Type`
   - Columns: `[Churn Rate]`
   - Annotate: Month-to-Month at 4x churn rate vs Two-Year.
2. **Support Ticket Risk Inflexion Curve (Line / Bar)**:
   - Rows: `[Churn Rate]`
   - Columns: `Tech_Support_Tickets`
   - Reference Line: Vertical line at 3.5 tickets showing 82% churn probability.
3. **Payment Method Analysis (Bullet / Horizontal Bar)**:
   - Rows: `Payment_Method`
   - Columns: `[Churn Rate]`
   - Color: By `Payment_Category` showing automatic payment 28% churn reduction.

### View C: Actionable Retention Strategy (Bottom Row)
1. **Tenure Cohort & Service Matrix (Heatmap / Grouped Bar)**:
   - Columns: `Tenure_Cohort`
   - Rows: `Internet_Service_Type`
   - Color: `[Churn Rate]`
2. **Target High-Risk Cohort Table (Interactive Outreach Table)**:
   - Filter: `Retention_Target_Cohort = 'Target Retention Cohort'` AND `Churn_Status = 'No'`
   - Columns: `CustomerID`, `Tenure_Months`, `Tech_Support_Tickets`, `Monthly_Charges`, `Estimated_CLV`
   - Action: Click-through to simulate outreach and save $85 CRC vs $820+ CLV.

---

## 4. Color Palette Specifications
- **Retained / Favorable**: `#2ecc71` (Emerald Green)
- **Churned / High Risk**: `#e74c3c` (Crimson Red)
- **Neutral / Informational**: `#2b5c8f` (Navy Blue)
- **Warning / Elevated**: `#f39c12` (Amber Orange)
