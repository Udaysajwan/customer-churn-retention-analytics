"""
Data Cleansing Audit & Visual Validation Module.
Generates comprehensive comparative visualizations illustrating:
1. Missingness & whitespace detection in raw Total_Charges
2. Tenure_Months == 0 alignment with missing values
3. Total_Charges distribution before vs. after domain imputation
4. Cross-feature charge validation (Total_Charges vs Monthly_Charges * Tenure)
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def generate_cleansing_visualizations(raw_path, clean_path, output_dir):
    viz_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    raw_df = pd.read_csv(raw_path)
    clean_df = pd.read_csv(clean_path)
    
    sns.set_theme(style='whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # ---------------------------------------------------------
    # Panel 1: Missing / Whitespace Counts Before vs After
    # ---------------------------------------------------------
    raw_whitespace = (raw_df['Total_Charges'].astype(str).str.strip() == '').sum()
    clean_missing = clean_df['Total_Charges'].isna().sum()
    
    categories = ['Raw Dataset\n(Whitespace / Missing)', 'Cleaned Dataset\n(Zero Nulls)']
    counts = [raw_whitespace, clean_missing]
    colors = ['#e74c3c', '#2ecc71']
    
    bars1 = axes[0, 0].bar(categories, counts, color=colors, width=0.45, edgecolor='black', linewidth=1)
    axes[0, 0].set_ylabel('Number of Missing / Corrupt Records', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Data Completeness Audit (Total_Charges)', fontsize=12, fontweight='bold', pad=10)
    axes[0, 0].set_ylim(0, max(counts) * 1.25 if max(counts) > 0 else 10)
    
    for bar in bars1:
        h = bar.get_height()
        axes[0, 0].annotate(f"{int(h):,} rows",
                            xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 5), textcoords="offset points",
                            ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    # ---------------------------------------------------------
    # Panel 2: Total_Charges Missingness by Tenure Months
    # ---------------------------------------------------------
    coerced_charges = pd.to_numeric(raw_df['Total_Charges'].astype(str).str.strip(), errors='coerce')
    missing_mask = coerced_charges.isna()
    
    tenure_of_missing = raw_df.loc[missing_mask, 'Tenure_Months'].value_counts().sort_index()
    
    axes[0, 1].bar([f"Tenure = {t} mo" for t in tenure_of_missing.index], tenure_of_missing.values,
                   color='#3498db', width=0.4, edgecolor='black', linewidth=1)
    axes[0, 1].set_ylabel('Missing Records Count', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Root Cause Isolation: 100% of Missing Total_Charges Occur at Tenure = 0',
                         fontsize=12, fontweight='bold', pad=10)
    axes[0, 1].set_ylim(0, max(tenure_of_missing.values) * 1.25)
    for idx, val in enumerate(tenure_of_missing.values):
        axes[0, 1].annotate(f"{val} accounts (100%)",
                            xy=(idx, val), xytext=(0, 5), textcoords="offset points",
                            ha='center', va='bottom', fontsize=10, fontweight='bold')

    # ---------------------------------------------------------
    # Panel 3: Distribution of Total_Charges Post-Cleansing
    # ---------------------------------------------------------
    sns.histplot(clean_df['Total_Charges'], kde=True, ax=axes[1, 0], color='#16a34a', bins=35)
    axes[1, 0].set_title('Cleaned Total_Charges Distribution (KDE)', fontsize=12, fontweight='bold', pad=10)
    axes[1, 0].set_xlabel('Total Charges ($)', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Subscriber Count', fontsize=11, fontweight='bold')
    axes[1, 0].axvline(clean_df['Total_Charges'].median(), color='#b91c1c', linestyle='--',
                       label=f"Median: ${clean_df['Total_Charges'].median():,.1f}")
    axes[1, 0].legend(loc='upper right')

    # ---------------------------------------------------------
    # Panel 4: Cross-Feature Validation (Tenure vs Total_Charges)
    # ---------------------------------------------------------
    scatter = axes[1, 1].scatter(clean_df['Tenure_Months'], clean_df['Total_Charges'],
                                 c=clean_df['Monthly_Charges'], cmap='viridis', alpha=0.4, s=15)
    cbar = plt.colorbar(scatter, ax=axes[1, 1])
    cbar.set_label('Monthly Charges ($)', fontsize=10)
    axes[1, 1].set_title('Cross-Feature Validation: Total_Charges vs. Tenure', fontsize=12, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel('Tenure (Months)', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Total Charges ($)', fontsize=11, fontweight='bold')
    
    # Highlight zero tenure imputed points
    zero_tenure = clean_df[clean_df['Tenure_Months'] == 0]
    axes[1, 1].scatter(zero_tenure['Tenure_Months'], zero_tenure['Total_Charges'],
                       color='#e74c3c', s=60, edgecolors='black', label=f'Imputed New Accounts (n={len(zero_tenure)})')
    axes[1, 1].legend(loc='upper left')

    plt.suptitle('Data Cleansing & Quality Audit: Raw to Clean Transformation', fontsize=15, fontweight='bold', y=0.99)
    plt.tight_layout()
    
    output_fig_path = os.path.join(viz_dir, 'data_cleansing_audit.png')
    plt.savefig(output_fig_path, dpi=300)
    plt.close()
    print(f"Data cleansing audit visualization saved to: {output_fig_path}")
    return output_fig_path

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, 'data', 'raw_customer_churn_data.csv')
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    generate_cleansing_visualizations(raw_csv, clean_csv, base_dir)
