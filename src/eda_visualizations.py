"""
Exploratory Data Analysis (EDA) & Visualization Module for Customer Churn & Retention Analytics.
Corresponds to Step 2 in Methodology:
- Analyzes churn distribution across contract types, payment methods, and tenure bands
- Generates high-resolution visualizations for the 3 key findings:
  1. Month-to-month vs. Two-year churn (4x likelihood)
  2. Support tickets > 3 showing ~82% churn probability
  3. Automatic payment methods reducing churn by ~28%
  4. Fiber optic vs. DSL tenure dynamics
  5. Correlation matrix
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def generate_eda_visualizations(clean_data_path, output_dir):
    viz_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    df = pd.read_csv(clean_data_path)
    df['Churn_Flag'] = (df['Churn_Status'] == 'Yes').astype(int)
    
    sns.set_theme(style='whitegrid')
    palette = ['#2b5c8f', '#d9534f', '#2ecc71', '#f39c12']
    
    # -------------------------------------------------------------
    # 1. Churn by Contract Type (Key Finding 1: 4x More Likely)
    # -------------------------------------------------------------
    contract_churn = df.groupby('Contract_Type')['Churn_Flag'].agg(['count', 'mean']).reset_index()
    contract_churn['Churn_Rate_Pct'] = contract_churn['mean'] * 100
    contract_order = ['Month-to-month', 'One year', 'Two year']
    contract_churn['Contract_Type'] = pd.Categorical(contract_churn['Contract_Type'], categories=contract_order, ordered=True)
    contract_churn = contract_churn.sort_values('Contract_Type')
    
    m2m_rate = contract_churn.loc[contract_churn['Contract_Type'] == 'Month-to-month', 'Churn_Rate_Pct'].values[0]
    two_yr_rate = contract_churn.loc[contract_churn['Contract_Type'] == 'Two year', 'Churn_Rate_Pct'].values[0]
    ratio = m2m_rate / two_yr_rate if two_yr_rate > 0 else 0
    
    plt.figure(figsize=(8, 5.5))
    bars = plt.bar(contract_churn['Contract_Type'], contract_churn['Churn_Rate_Pct'],
                   color=['#d9534f', '#f39c12', '#2ecc71'], width=0.55, edgecolor='black', linewidth=1)
    plt.ylabel('Churn Rate (%)', fontsize=12)
    plt.title(f'Customer Churn Rate by Contract Type\n(Month-to-Month is {ratio:.1f}x More Likely to Churn than Two-Year)',
              fontsize=13, fontweight='bold', pad=15)
    plt.ylim(0, max(contract_churn['Churn_Rate_Pct']) * 1.25)
    
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f"{height:.1f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    plt.tight_layout()
    contract_path = os.path.join(viz_dir, 'churn_by_contract.png')
    plt.savefig(contract_path, dpi=300)
    plt.close()
    print(f"Saved: {contract_path}")
    
    # -------------------------------------------------------------
    # 2. Churn by Tech Support Tickets (Key Finding 2: >3 calls => 82% churn)
    # -------------------------------------------------------------
    ticket_churn = df.groupby('Tech_Support_Tickets')['Churn_Flag'].agg(['count', 'mean']).reset_index()
    ticket_churn['Churn_Rate_Pct'] = ticket_churn['mean'] * 100
    
    plt.figure(figsize=(9, 5.5))
    colors = ['#2b5c8f' if t <= 3 else '#d9534f' for t in ticket_churn['Tech_Support_Tickets']]
    bars = plt.bar(ticket_churn['Tech_Support_Tickets'], ticket_churn['Churn_Rate_Pct'],
                   color=colors, width=0.6, edgecolor='black', linewidth=1)
    
    # Highlight threshold
    plt.axvline(x=3.5, color='#c0392b', linestyle='--', linewidth=2, label='Critical Inflexion Threshold (> 3 Tickets)')
    plt.ylabel('Churn Rate (%)', fontsize=12)
    plt.xlabel('Number of Tech Support Tickets (Past 6 Months)', fontsize=12)
    plt.title('Churn Rate vs. Tech Support Tickets\n(Customers with >3 Tickets Exceed ~82% Churn Probability)',
              fontsize=13, fontweight='bold', pad=15)
    plt.ylim(0, 105)
    plt.legend(loc='upper left', fontsize=11)
    
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f"{height:.0f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    ticket_path = os.path.join(viz_dir, 'churn_by_support_tickets.png')
    plt.savefig(ticket_path, dpi=300)
    plt.close()
    print(f"Saved: {ticket_path}")
    
    # -------------------------------------------------------------
    # 3. Churn by Payment Method (Key Finding 3: Auto Pay 28% reduction)
    # -------------------------------------------------------------
    pay_churn = df.groupby('Payment_Method')['Churn_Flag'].agg(['count', 'mean']).reset_index()
    pay_churn['Churn_Rate_Pct'] = pay_churn['mean'] * 100
    pay_churn['Is_Auto'] = pay_churn['Payment_Method'].str.contains('automatic')
    
    manual_churn = df[~df['Payment_Method'].str.contains('automatic')]['Churn_Flag'].mean() * 100
    auto_churn = df[df['Payment_Method'].str.contains('automatic')]['Churn_Flag'].mean() * 100
    pct_reduction = ((manual_churn - auto_churn) / manual_churn) * 100
    
    plt.figure(figsize=(10, 5.5))
    bar_colors = ['#2ecc71' if auto else '#e74c3c' for auto in pay_churn['Is_Auto']]
    bars = plt.barh(pay_churn['Payment_Method'], pay_churn['Churn_Rate_Pct'],
                    color=bar_colors, height=0.55, edgecolor='black', linewidth=1)
    plt.xlabel('Churn Rate (%)', fontsize=12)
    plt.title(f'Customer Churn Rate by Payment Method\n(Automatic Payment Methods Reduce Churn by {pct_reduction:.1f}%)',
              fontsize=13, fontweight='bold', pad=15)
    plt.xlim(0, max(pay_churn['Churn_Rate_Pct']) * 1.25)
    
    for bar in bars:
        width = bar.get_width()
        plt.annotate(f"{width:.1f}%",
                     xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    pay_path = os.path.join(viz_dir, 'churn_by_payment_method.png')
    plt.savefig(pay_path, dpi=300)
    plt.close()
    print(f"Saved: {pay_path}")
    
    # -------------------------------------------------------------
    # 4. Churn by Tenure Bands & Internet Service Type
    # -------------------------------------------------------------
    bins = [-1, 12, 24, 48, 72]
    labels = ['0-12m', '13-24m', '25-48m', '49-72m']
    df['Tenure_Band'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels)
    
    band_service = df.groupby(['Tenure_Band', 'Internet_Service_Type'], observed=False)['Churn_Flag'].mean().unstack() * 100
    
    plt.figure(figsize=(9, 5.5))
    band_service.plot(kind='bar', figsize=(9, 5.5), colormap='viridis', edgecolor='black', linewidth=1)
    plt.title('Churn Rate by Tenure Band & Internet Service Type\n(Fiber Optic Exhibits Elevated Churn in Early Tenure)',
              fontsize=13, fontweight='bold', pad=15)
    plt.ylabel('Churn Rate (%)', fontsize=12)
    plt.xlabel('Tenure Cohort', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Internet Service', fontsize=10)
    plt.tight_layout()
    tenure_path = os.path.join(viz_dir, 'churn_by_tenure_band.png')
    plt.savefig(tenure_path, dpi=300)
    plt.close()
    print(f"Saved: {tenure_path}")
    
    # -------------------------------------------------------------
    # 5. Correlation Heatmap
    # -------------------------------------------------------------
    numeric_df = df[['Tenure_Months', 'Monthly_Charges', 'Total_Charges', 'Tech_Support_Tickets', 'Churn_Flag']].copy()
    corr = numeric_df.corr()
    
    plt.figure(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=1, square=True, cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix of Core Numerical Features & Churn', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    corr_path = os.path.join(viz_dir, 'correlation_matrix.png')
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"Saved: {corr_path}")
    
    print("All EDA visualizations successfully generated.")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_path = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    generate_eda_visualizations(clean_path, base_dir)
