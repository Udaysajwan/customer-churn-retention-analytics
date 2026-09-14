"""
Customer Churn & Retention Analytics - Master Execution Pipeline
Author: Data Science & Analytics Team
Domain: Telecommunications & Subscription Services

Usage:
    python main.py                  # Runs the complete end-to-end pipeline
    python main.py --step clean     # Step 1: Clean raw data -> data/cleaned_customer_churn_data.csv
    python main.py --step eda       # Step 2: Generate EDA plots in visualizations/
    python main.py --step train     # Step 3: Train models, benchmark & save to models/
    python main.py --step strategy  # Step 4: Compute financial retention ROI
    python main.py --step report    # Step 5: Compile executive PDF report
"""

import os
import sys
import argparse
import time

# Ensure src is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

# Force headless non-interactive matplotlib backend
import matplotlib
matplotlib.use('Agg')

from data_cleansing import clean_churn_data
from eda_visualizations import generate_eda_visualizations
from data_cleansing_visualizer import generate_cleansing_visualizations
from train_models import train_and_evaluate_models
from retention_strategy import compute_financial_retention_analytics

def print_banner():
    print("=" * 72)
    print("   CUSTOMER CHURN & RETENTION ANALYTICS PIPELINE")
    print("   Domain: Telecommunications | Subscription Intelligence")
    print("=" * 72)

def run_cleaning():
    print("\n[Step 1/5] Ingesting & Cleansing Raw Customer Data...")
    start = time.time()
    raw_path = os.path.join(BASE_DIR, 'data', 'raw_customer_churn_data.csv')
    clean_path = os.path.join(BASE_DIR, 'data', 'cleaned_customer_churn_data.csv')
    
    if not os.path.exists(raw_path):
        print(f"[-] Raw dataset not found at: {raw_path}")
        print("[*] Synthesizing 10,000 raw customer records...")
        from data_generator import save_raw_dataset
        save_raw_dataset(raw_path)
        
    df = clean_churn_data(raw_path, clean_path)
    # Also generate the visual data quality audit plot
    generate_cleansing_visualizations(raw_path, clean_path, BASE_DIR)
    
    elapsed = time.time() - start
    print(f"[+] Step 1 Complete: Cleaned {len(df):,} records in {elapsed:.2f}s")
    print(f"    Output saved to: data/cleaned_customer_churn_data.csv")
    return clean_path

def run_eda(clean_path=None):
    print("\n[Step 2/5] Generating Exploratory Data Analysis & Finding Plots...")
    start = time.time()
    if clean_path is None or not os.path.exists(clean_path):
        clean_path = os.path.join(BASE_DIR, 'data', 'cleaned_customer_churn_data.csv')
        if not os.path.exists(clean_path):
            print("[-] Cleaned data not found. Running Step 1 first...")
            clean_path = run_cleaning()
            
    generate_eda_visualizations(clean_path, BASE_DIR)
    elapsed = time.time() - start
    print(f"[+] Step 2 Complete: Visualizations generated in {elapsed:.2f}s")
    print(f"    Plots saved to: visualizations/")

def run_training(clean_path=None):
    print("\n[Step 3/5] Training Classifiers (Logistic Regression, Random Forest, XGBoost)...")
    start = time.time()
    if clean_path is None or not os.path.exists(clean_path):
        clean_path = os.path.join(BASE_DIR, 'data', 'cleaned_customer_churn_data.csv')
        if not os.path.exists(clean_path):
            print("[-] Cleaned data not found. Running Step 1 first...")
            clean_path = run_cleaning()
            
    results, best_model_name = train_and_evaluate_models(clean_path, BASE_DIR)
    elapsed = time.time() - start
    print(f"[+] Step 3 Complete: Models benchmarked in {elapsed:.2f}s")
    print(f"    Best Model Selected: {best_model_name}")
    print(f"    Trained model saved to: models/best_churn_model.joblib")
    return results

def run_strategy(clean_path=None):
    print("\n[Step 4/5] Modeling Retention Financial Economics & Campaign ROI...")
    start = time.time()
    if clean_path is None or not os.path.exists(clean_path):
        clean_path = os.path.join(BASE_DIR, 'data', 'cleaned_customer_churn_data.csv')
        if not os.path.exists(clean_path):
            print("[-] Cleaned data not found. Running Step 1 first...")
            clean_path = run_cleaning()
            
    fin = compute_financial_retention_analytics(clean_path, BASE_DIR)
    
    # Also export Tableau extract
    tableau_dir = os.path.join(BASE_DIR, 'tableau')
    os.makedirs(tableau_dir, exist_ok=True)
    tableau_csv = os.path.join(tableau_dir, 'tableau_churn_dataset.csv')
    
    import pandas as pd
    import numpy as np
    df = pd.read_csv(clean_path)
    df['Churn_Numeric'] = (df['Churn_Status'] == 'Yes').astype(int)
    df['MRR_Lost'] = np.where(df['Churn_Status'] == 'Yes', df['Monthly_Charges'], 0.0)
    bins = [-1, 12, 24, 48, 72]
    labels = ['0-12 Months', '13-24 Months', '25-48 Months', '49-72 Months']
    df['Tenure_Cohort'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels)
    df['Payment_Category'] = np.where(df['Payment_Method'].str.contains('automatic'), 'Automatic Payment', 'Manual / Check Payment')
    df['Retention_Target_Cohort'] = np.where((df['Tenure_Months'] < 12) & (df['Tech_Support_Tickets'] > 3), 'Targeted High-Risk Cohort', 'Standard Cohort')
    df['Estimated_CLV'] = np.round((df['Monthly_Charges'] * 0.75) / (0.325 / 12), 2)
    df.to_csv(tableau_csv, index=False)
    
    elapsed = time.time() - start
    print(f"[+] Step 4 Complete: Financial retention metrics calculated in {elapsed:.2f}s")
    print(f"    Campaign Net ROI: {fin['targeted_campaign_strategy']['campaign_roi_pct']}%")
    print(f"    Tableau extract saved to: tableau/tableau_churn_dataset.csv")

def run_report():
    print("\n[Step 5/5] Compiling Executive PDF Reports & Syncing Web Dashboard...")
    start = time.time()
    import shutil
    
    # 1. Executive Intelligence Report (5 pages)
    from generate_pdf_report import build_pdf
    pdf_path = os.path.join(BASE_DIR, 'Customer_Churn_Retention_Analytics_Report.pdf')
    build_pdf(pdf_path)
    shutil.copy2(pdf_path, os.path.join(BASE_DIR, 'reports', 'Customer_Churn_Retention_Analytics_Report.pdf'))
    print("    [+] Executive PDF compiled: Customer_Churn_Retention_Analytics_Report.pdf")

    # 2. Architecture & Folder Guide (4 pages)
    from generate_folder_guide_pdf import build_folder_guide_pdf
    arch_pdf = os.path.join(BASE_DIR, 'Project_Architecture_and_Folder_Guide.pdf')
    build_folder_guide_pdf(arch_pdf)
    shutil.copy2(arch_pdf, os.path.join(BASE_DIR, 'reports', 'Project_Architecture_and_Folder_Guide.pdf'))
    print("    [+] Architecture Guide compiled: Project_Architecture_and_Folder_Guide.pdf")

    # 3. HR & Interview Discussion Guide (optional if present)
    hr_script = os.path.join(BASE_DIR, 'generate_hr_guide_pdf.py')
    if os.path.exists(hr_script):
        from generate_hr_guide_pdf import build_hr_guide_pdf
        hr_pdf = os.path.join(BASE_DIR, 'HR_and_Interview_Discussion_Guide.pdf')
        build_hr_guide_pdf(hr_pdf)
        shutil.copy2(hr_pdf, os.path.join(BASE_DIR, 'reports', 'HR_and_Interview_Discussion_Guide.pdf'))
        print("    [+] HR Interview Playbook compiled: HR_and_Interview_Discussion_Guide.pdf")

    # 4. Sync interactive dashboard to docs/index.html for GitHub Pages hosting
    docs_dir = os.path.join(BASE_DIR, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    shutil.copy2(os.path.join(BASE_DIR, 'reports', 'interactive_dashboard.html'), os.path.join(docs_dir, 'index.html'))
    print("    [+] Web Simulator synced for GitHub Pages: docs/index.html")
    
    elapsed = time.time() - start
    print(f"[+] Step 5 Complete: All reports and GitHub Pages assets compiled in {elapsed:.2f}s")

def main():
    parser = argparse.ArgumentParser(description="Customer Churn & Retention Analytics Master Pipeline")
    parser.add_argument('--step', choices=['clean', 'eda', 'train', 'strategy', 'report', 'all'], default='all',
                        help="Select a specific pipeline step to execute")
    args = parser.parse_args()

    print_banner()

    if args.step == 'clean':
        run_cleaning()
    elif args.step == 'eda':
        run_eda()
    elif args.step == 'train':
        run_training()
    elif args.step == 'strategy':
        run_strategy()
    elif args.step == 'report':
        run_report()
    else: # 'all'
        clean_path = run_cleaning()
        run_eda(clean_path)
        run_training(clean_path)
        run_strategy(clean_path)
        run_report()
        print("\n" + "=" * 72)
        print("   ALL PIPELINE PHASES EXECUTED SUCCESSFULLY!")
        print("   Cleaned data, models, visualizations, and PDF report generated.")
        print("=" * 72)

if __name__ == '__main__':
    main()
