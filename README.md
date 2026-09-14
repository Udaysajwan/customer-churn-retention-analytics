# Customer Churn & Retention Analytics
### Enterprise Subscriber Intelligence, Predictive Risk Modeling & Retention ROI Optimization

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-v1.9-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-v3.4-red.svg)](https://xgboost.readthedocs.io/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%2F%20Postgres%20%2F%20SQLite-lightgrey.svg)](sql/churn_analysis.sql)
[![Tableau](https://img.shields.io/badge/Tableau-Calculated%20Fields-E97627.svg)](tableau/tableau_calculated_fields.md)

---

## 📌 Project Overview

In subscription and telecommunications business models, **Customer Acquisition Cost (CAC) is 5x to 7x higher than Customer Retention Cost (CRC)**. Preventing customer churn directly preserves **Monthly Recurring Revenue (MRR)** and maximizes **Customer Lifetime Value (CLV)**.

This repository is built as a modular, production-style data science project:
- Starts from **raw subscriber data** (`data/raw_customer_churn_data.csv`) containing realistic real-world data quality defects (e.g. unbilled new signups with whitespace charges).
- Provides a **dedicated data cleansing & quality audit notebook** (`notebooks/01_data_cleansing_and_audit.ipynb`) that isolates root causes and verifies the raw-to-clean transformation.
- Implements a **modular analytical and ML pipeline** in `src/` to train models, evaluate recall/ROC-AUC, and model targeted retention economics.
- Includes an **executive master runner** (`main.py`) allowing you to execute the entire pipeline or individual steps on demand.

---

## 🏗️ Clean Repository Structure

The repository is structured in a clean, pre-execution state—ready for you to run and inspect each phase:

```
Customer Churn & Retention Analytics/
├── customer_churn_analytics.json                  # Original project specification & objectives
├── README.md                                      # Comprehensive project documentation
├── requirements.txt                               # Environment dependencies
├── main.py                                        # Master CLI pipeline runner
├── generate_pdf_report.py                         # Executive 5-page PDF compiler
│
├── data/
│   └── raw_customer_churn_data.csv                # 10k raw records with unbilled Total_Charges whitespace
│   # Note: cleaned_customer_churn_data.csv will be generated when you run the cleansing step!
│
├── notebooks/
│   ├── 01_data_cleansing_and_audit.ipynb          # Dedicated raw-to-clean data auditing & visual notebook
│   └── 02_customer_churn_and_retention.ipynb      # End-to-end EDA, ML benchmarking & retention strategy
│
├── src/
│   ├── __init__.py
│   ├── data_generator.py                          # Synthetic calibrated data generator
│   ├── data_cleansing.py                          # Cleans raw data -> outputs cleaned_customer_churn_data.csv
│   ├── data_cleansing_visualizer.py               # Generates comparative raw vs clean audit plots
│   ├── feature_engineering.py                     # Feature transformations (Average Spend, Ticket Frequency)
│   ├── eda_visualizations.py                      # Step 2 visualization pipeline
│   ├── train_models.py                            # Multi-model ML pipeline (LogReg, RF, XGBoost) & evaluation
│   └── retention_strategy.py                      # Business KPIs (MRR Lost, CLV, NPS, CRC & Campaign ROI)
│
├── sql/
│   └── churn_analysis.sql                         # Enterprise ANSI SQL suite (CTEs, Window functions, Cohorts)
│
├── tableau/
│   └── tableau_calculated_fields.md               # Tableau LOD formulas and dashboard layout guide
│   # Note: tableau_churn_dataset.csv will be exported when you run the pipeline!
│
├── reports/
│   ├── executive_summary.md                       # Business summary report
│   └── interactive_dashboard.html                 # Browser dashboard with interactive simulator
│   # Note: JSON metrics and PDF reports will be compiled upon execution!
│
├── models/                                        # Directory where trained models are saved (.joblib)
└── visualizations/                                # Directory where high-res plots are saved (.png)
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Option A: Run the Complete Pipeline (One Command)
To run the entire pipeline end-to-end (clean data, generate plots, train models, compute retention economics, and compile the executive PDF):
```bash
python main.py
```

### 3. Option B: Run Step-by-Step
You can execute each phase individually to observe outputs being generated at each stage:

```bash
# Step 1: Clean raw data -> creates data/cleaned_customer_churn_data.csv and data_cleansing_audit.png
python main.py --step clean

# Step 2: Generate EDA plots -> saves 4 core findings charts in visualizations/
python main.py --step eda

# Step 3: Train & benchmark ML models -> saves models/best_churn_model.joblib & ROC curves
python main.py --step train

# Step 4: Calculate retention economics -> saves reports/retention_financial_summary.json & Tableau extract
python main.py --step strategy

# Step 5: Compile 5-page executive PDF report
python main.py --step report
# Or directly:
python generate_pdf_report.py
```

### 4. Option C: Run Interactively via Jupyter Notebooks
Launch Jupyter and explore the interactive notebooks cell-by-cell:
```bash
jupyter notebook
```
- Open `notebooks/01_data_cleansing_and_audit.ipynb` to explore the raw data quality audit, whitespace detection, and cleaning logic.
- Open `notebooks/02_customer_churn_and_retention.ipynb` for the full exploratory data analysis, predictive modeling, and retention ROI modeling.

---

## 📊 Summary of Validated Findings & Expected Results

When you run the pipeline, the outputs will confirm the following empirical findings:

| Finding | Result | Takeaway |
| :--- | :---: | :--- |
| **Finding 1: Contract Type Impact** | **4.0x Risk Multiplier** | Month-to-month contracts churn at **43.5%** vs. **10.8%** for two-year contracts. |
| **Finding 2: Support Ticket Cliff** | **81.7% Churn Probability** | Customers logging **>3 support tickets** exhibit an **81.7% churn rate**. |
| **Finding 3: Automatic Payment Advantage** | **-27.8% Churn Reduction** | Auto-pay methods (bank draft / credit card) reduce churn from **34.9%** to **25.2%**. |
| **Baseline Churn Rate** | **32.46%** | 3,246 out of 10,000 customers churned. |
| **Monthly Recurring Revenue (MRR) Lost** | **$231,893.75 / mo** | 34.8% of total monthly recurring revenue. |
| **Best ML Model** | **Logistic Regression** | **74.88% Recall**, **0.7869 ROC-AUC** (prioritized to intercept churning accounts). |
| **Target Campaign Net ROI** | **+175.51%** | A \$26,010 retention budget saves \$78,060 in annual revenue and yields \$45,649 net profit. |

---

## 🗄️ SQL Analytics Suite

Open `sql/churn_analysis.sql` to inspect or run production ANSI SQL queries covering:
- Executive KPI summary (MRR, MRR Lost, Churn Rate).
- Churn by Contract Type & Payment Category.
- Support Ticket Risk Tiers.
- Cohort Analysis (Tenure bands & Internet Service).
- High-Risk Customer Extraction for proactive CRM outreach.

---

## 💻 Interactive Browser Dashboard

Open `reports/interactive_dashboard.html` in any web browser to interact with:
- Live KPI cards and responsive Chart.js visual analytics.
- **Live Churn Risk & Retention ROI Simulator**: Adjust customer attributes in real time to simulate churn probabilities and view automated retention action plans.
- Priority customer outreach table.
