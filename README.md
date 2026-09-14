# Customer Churn & Retention Analytics
### Enterprise Subscriber Intelligence, Predictive Risk Modeling & Retention ROI Optimization

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://<your-username>.github.io/customer-churn-retention-analytics/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-v1.9-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-v3.4-red.svg)](https://xgboost.readthedocs.io/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%2F%20Postgres%20%2F%20SQLite-lightgrey.svg)](sql/churn_analysis.sql)
[![Tableau](https://img.shields.io/badge/Tableau-Calculated%20Fields-E97627.svg)](tableau/tableau_calculated_fields.md)

---

## 🌐 Live Interactive Web Simulator (Hosted on GitHub Pages)

Experience the live interactive web simulator without running any code:  
👉 **[Launch Live Interactive Dashboard & Churn Simulator](https://<your-username>.github.io/customer-churn-retention-analytics/)**  
*(Or open local `docs/index.html` or `reports/interactive_dashboard.html` in any browser)*

### How to Enable 1-Click Free Hosting on Your GitHub Repository:
1. Push this repository to your GitHub account (`git push -u origin main`).
2. On GitHub, navigate to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
4. Set Branch to **`main`** and folder to **`/docs`**, then click **Save**.
5. Your interactive dashboard is now hosted live at `https://<your-username>.github.io/customer-churn-retention-analytics/`!

---

## 📌 Project Overview

In subscription and telecommunications business models, **Customer Acquisition Cost (CAC) is 5x to 7x higher than Customer Retention Cost (CRC)**. Preventing customer churn directly preserves **Monthly Recurring Revenue (MRR)** and maximizes **Customer Lifetime Value (CLV)**.

This repository is built as a modular, production-grade data science project:
- Starts from **raw subscriber data** (`data/raw_customer_churn_data.csv`) containing realistic real-world data quality defects (e.g. unbilled new signups with whitespace charges).
- Provides a **dedicated data cleansing & quality audit notebook** (`notebooks/01_data_cleansing_and_audit.ipynb`) that isolates root causes and verifies the raw-to-clean transformation.
- Implements a **modular analytical and ML pipeline** in `src/` to train models, evaluate recall/ROC-AUC, and model targeted retention economics.
- Includes an **executive master runner** (`main.py`) allowing you to execute the entire pipeline or individual steps on demand.
- Delivers **3 publication-grade PDF documents** for executives, technical engineers, and HR interviewers.

---

## 📚 Comprehensive PDF Documentation Guides

This repository includes 3 distinct, publication-quality PDF guides compiled using ReportLab:

| Document | File Path | Audience & Purpose |
| :--- | :--- | :--- |
| **1. Executive Intelligence Report** (5 Pages) | [`Customer_Churn_Retention_Analytics_Report.pdf`](Customer_Churn_Retention_Analytics_Report.pdf) | Executive summary, data cleansing audit, 3 empirical churn findings, ML model benchmark table, and retention campaign ROI analysis. |
| **2. Architecture & Folder Guide** (4 Pages) | [`Project_Architecture_and_Folder_Guide.pdf`](Project_Architecture_and_Folder_Guide.pdf) | Technical document explaining the purpose of every folder (`data/`, `src/`, `sql/`, `tableau/`, `models/`, `reports/`) and software design patterns. |
| **3. HR & Interview Discussion Guide** (4 Pages) | [`HR_and_Interview_Discussion_Guide.pdf`](HR_and_Interview_Discussion_Guide.pdf) | **Candidate interview playbook:** 30-second & 2-minute elevator pitches, STAR method breakdown, exact answers to 6 tough interview questions, metric flashcards, and role-specific pitch strategies. |

---

## 🏗️ Repository Structure

```
Customer Churn & Retention Analytics/
├── customer_churn_analytics.json                  # Original project specification & objectives
├── README.md                                      # Comprehensive project documentation
├── RESUME_DESCRIPTION.md                          # ATS-optimized resume bullet points & pitch
├── LICENSE                                        # MIT open source license
├── requirements.txt                               # Environment dependencies
├── main.py                                        # Master CLI pipeline runner
├── generate_pdf_report.py                         # 5-page Executive PDF compiler
├── generate_folder_guide_pdf.py                   # 4-page Architecture & Folder Guide compiler
├── generate_hr_guide_pdf.py                       # 4-page HR & Interview Discussion Guide compiler
│
├── Customer_Churn_Retention_Analytics_Report.pdf  # Executive 5-page PDF report
├── Project_Architecture_and_Folder_Guide.pdf      # Technical 4-page architecture guide
├── HR_and_Interview_Discussion_Guide.pdf          # HR & candidate interview playbook
│
├── .github/
│   └── workflows/
│       └── deploy_pages.yml                       # Automated GitHub Actions Pages deployment
│
├── docs/
│   └── index.html                                 # Live GitHub Pages interactive dashboard
│
├── data/
│   ├── raw_customer_churn_data.csv                # 10k raw records with unbilled Total_Charges whitespace
│   └── cleaned_customer_churn_data.csv            # Cleaned, validated baseline dataset
│
├── notebooks/
│   ├── 01_data_cleansing_and_audit.ipynb          # Dedicated raw-to-clean data auditing & visual notebook
│   └── 02_customer_churn_and_retention.ipynb      # End-to-end EDA, ML benchmarking & retention strategy
│
├── src/
│   ├── __init__.py
│   ├── data_generator.py                          # Synthetic calibrated data generator
│   ├── data_cleansing.py                          # Cleans raw data -> outputs cleaned dataset
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
│   ├── tableau_calculated_fields.md               # Tableau LOD formulas and dashboard layout guide
│   └── tableau_churn_dataset.csv                  # Tableau-ready enriched dataset
│
├── reports/
│   ├── executive_summary.md                       # Business summary report
│   ├── interactive_dashboard.html                 # Browser dashboard with interactive simulator
│   ├── model_benchmarks.json                      # Precision, Recall, F1, ROC-AUC metrics
│   ├── retention_financial_summary.json           # Campaign financial ROI breakdown
│   ├── Customer_Churn_Retention_Analytics_Report.pdf
│   ├── Project_Architecture_and_Folder_Guide.pdf
│   └── HR_and_Interview_Discussion_Guide.pdf
│
├── models/
│   └── best_churn_model.joblib                    # Serialized production pipeline (Logistic Regression)
│
└── visualizations/                                # 10 publication-quality 300 DPI PNG charts
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Option A: Run the Complete Pipeline (One Command)
To run the entire pipeline end-to-end (clean data, generate plots, train models, compute retention economics, compile all 3 PDFs, and update the GitHub Pages dashboard):
```bash
python main.py
```

### 3. Option B: Run Step-by-Step via CLI
You can execute each phase individually:

```bash
# Step 1: Clean raw data -> creates cleaned data and data_cleansing_audit.png
python main.py --step clean

# Step 2: Generate EDA plots -> saves 4 core findings charts in visualizations/
python main.py --step eda

# Step 3: Train & benchmark ML models -> saves best model & ROC curves
python main.py --step train

# Step 4: Calculate retention economics -> saves financial ROI & Tableau extract
python main.py --step strategy

# Step 5: Compile all 3 PDF reports and sync GitHub Pages web app
python main.py --step report
```

### 4. Option C: Run Interactively via Jupyter Notebooks
Launch Jupyter and explore the interactive notebooks cell-by-cell:
```bash
jupyter notebook
```
- Open `notebooks/01_data_cleansing_and_audit.ipynb` to explore the raw data quality audit, whitespace detection, and cleaning logic.
- Open `notebooks/02_customer_churn_and_retention.ipynb` for the full exploratory data analysis, predictive modeling, and retention ROI modeling.

---

## 📊 Summary of Validated Findings & Benchmark Results

| Finding / Metric | Value | Business Impact & Takeaway |
| :--- | :---: | :--- |
| **Contract Multiplier** | **4.0x Risk Multiplier** | Month-to-month contracts churn at **43.5%** vs. **10.8%** for two-year contracts. |
| **Support Friction Cliff** | **81.7% Churn Probability** | Customers logging **>3 support tickets** exhibit an **81.7% churn rate**. |
| **Automatic Payment Advantage** | **-27.8% Churn Reduction** | Auto-pay methods reduce churn from **34.9%** (manual check) to **25.2%**. |
| **Baseline Churn Rate** | **26.50%** | 2,650 out of 10,000 customers churned in baseline dataset. |
| **Monthly Revenue Lost** | **$231,895.20 / mo** | 34.8% of total monthly recurring revenue at risk. |
| **Best Model Recall** | **74.88% (LogReg)** | Intercepts ~3 out of 4 churning accounts before cancellation. |
| **Model ROC-AUC** | **0.7869 (LogReg)** | Superior probability discrimination with 100% odds ratio explainability. |
| **Target Campaign Net ROI** | **+175.51%** | An \$85/user proactive intervention yields \$78,060 saved revenue and \$45,649 net profit. |

---

## 🗄️ SQL Analytics Suite

The SQL suite in `sql/churn_analysis.sql` contains production ANSI SQL queries employing:
- Common Table Expressions (CTEs) for multi-stage subscriber cohorts.
- Window functions (`ROW_NUMBER() OVER (...)`, `AVG() OVER (...)`) for ranking and peer benchmarks.
- Tenure band and payment method cohort retention matrices.
- High-risk customer extraction queries for CRM and retention campaign integrations.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
