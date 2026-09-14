# Executive Summary Report: Customer Churn & Retention Analytics

**Project:** Customer Churn & Retention Analytics  
**Domain:** Telecommunications & Subscription Services  
**Dataset Scale:** 10,000 Customer Accounts  
**Primary Objective:** Identify attrition drivers, construct predictive models to forecast churn risk, and model high-ROI customer retention strategies.

---

## 1. Executive Overview

Customer attrition represents the single largest drag on recurrent revenue in the subscription telecommunications sector. In an analysis of **10,000 customer accounts**, our baseline findings show:
- **Global Churn Rate:** `32.46%` (3,246 churned accounts)
- **Monthly Recurring Revenue (MRR) Lost:** `$231,893.75 / month` ($2.78M annualized)
- **MRR Revenue Loss Ratio:** `34.79%` of total gross MRR ($666,549.67) is shed to churn
- **Average Customer Lifetime Value (CLV):** `$1,848.10`
- **Total Lifetime Value Lost to Attrition:** `$6,429,586.41`
- **Net Promoter Score (NPS Proxy):** `-10.0` (heavily dragged down by high-friction support callers)

Through data engineering, exploratory data analysis, and predictive machine learning, we isolated the primary operational drivers of attrition and constructed an actionable **Targeted Retention Campaign** delivering an estimated **175.51% net ROI**.

---

## 2. Validation of Core Analytical Findings

| Finding Hypothesis | Analytical Result | Statistical Evidence | Strategic Implication |
| :--- | :--- | :--- | :--- |
| **Finding 1: Contract Type Impact** | **Confirmed (4.0x Risk)** | Month-to-month churn is **43.5%** vs. **10.8%** for two-year contract holders. | Month-to-month contracts serve as the main churn channel. Migrate customers to term agreements via annual discounts. |
| **Finding 2: Support Ticket Tipping Point** | **Confirmed (81.7% Risk)** | Customers with **>3 support tickets** within 6 months exhibit an **81.7% churn probability**. | Customers with 3+ calls experience extreme friction. Algorithmic trigger needed at ticket 3 for concierge resolution. |
| **Finding 3: Automatic Payment Advantage** | **Confirmed (27.8% Churn Reduction)** | Automatic methods (Bank transfer / Credit card) exhibit **25.2%** churn vs. **34.9%** for manual check methods. | Billing friction triggers involuntary and voluntary attrition. Auto-pay incentives pay for themselves immediately. |

---

## 3. Predictive Modeling Benchmarking

We evaluated three production-grade classification architectures across 2,000 holdout test records with stratified class weighting:

| Model Architecture | Accuracy | Precision | Recall (Attrition Sensitivity) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Class Balanced)** | **71.65%** | **54.61%** | **74.88%** | **0.6316** | **0.7869** |
| **Random Forest Classifier (150 Trees)** | 71.90% | 55.79% | 64.56% | 0.5986 | 0.7774 |
| **XGBoost Classifier (scale_pos_weight)** | 70.75% | 53.90% | 68.10% | 0.6018 | 0.7718 |

### Model Selection Insights:
- **Logistic Regression** achieved the highest overall **ROC-AUC (0.7869)** and the highest **Recall (74.88%)**, capturing three out of four churning customers before departure.
- Key Feature Drivers: `Tech_Support_Tickets`, `Contract_Type_Two year`, `Tenure_Months`, `Payment_Method_Electronic check`, and `Average_Monthly_Spend`.

---

## 4. Priority Retention Strategy & Financial ROI

### Target Cohort Definition (Step 5 Priority)
- **Segment:** Early Tenure (`Tenure < 12 Months`) **AND** High Service Friction (`Tech_Support_Tickets > 3`).
- **Cohort Population:** `306 accounts`
- **Observed Cohort Churn Rate:** `81.70%` (250 accounts expected to churn without intervention)
- **Monthly Revenue at Risk:** `$22,879.80 / month`

### Retention Campaign Mechanics:
1. **Customer Retention Cost (CRC):** `$85.00 per customer`
   - Dedicated Senior Technical Concierge Outreach: `$25.00`
   - Bill Credit Incentive ($20/month for 3 billing cycles): `$60.00`
2. **Total Campaign Budget:** `306 * $85 = $26,010.00`
3. **Conservative Rescue Target:** `35%` of would-be churners retained (`87 customers`).

### Financial Return Summary:
- **Annualized Rescued Revenue:** `$78,060.49`
- **Preserved Customer Lifetime Value (CLV):** `$71,659.53`
- **Net Campaign Profit (CLV - CRC Budget):** **`$45,649.53`**
- **Return on Investment (ROI):** **`175.51%`**

---

## 5. Strategic Recommendations for Business Leadership

1. **Implement Algorithmic "Ticket 3" Concierge Escalations**:
   Establish an automated CRM webhook that triggers a senior engineering desk transfer when a customer logs their 3rd ticket. Intercepting issues before ticket 4 averts the 82% churn tipping point.

2. **Onboarding Auto-Pay Incentive Program**:
   Offer a one-time $10 account credit to users who enroll in automatic bank draft or credit card payments during signup. The 28% reduction in churn more than amortizes the $10 concession within 60 days.

3. **Early-Tenure Contract Transition Campaigns**:
   Target Month-to-Month customers in Month 3 and Month 6 with a 12-month contract lock discount (e.g. 10% off for 12 months). Moving subscribers into 1-year terms cuts attrition risk by over 50%.
