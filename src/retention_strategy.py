"""
Retention Strategy & Financial Analytics Module for Customer Churn & Retention Analytics.
Corresponds to Step 5 in Methodology and Key Metrics from customer_churn_analytics.json:
- Customer Churn Rate
- Monthly Recurrent Revenue (MRR) Lost
- Customer Lifetime Value (CLV)
- Net Promoter Score (NPS proxy based on support friction)
- Customer Retention Cost (CRC) and Campaign ROI Modeling
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def compute_financial_retention_analytics(clean_data_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    reports_dir = os.path.join(output_dir, 'reports')
    viz_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    
    df = pd.read_csv(clean_data_path)
    
    total_customers = len(df)
    churn_mask = df['Churn_Status'] == 'Yes'
    churned_customers = churn_mask.sum()
    retained_customers = total_customers - churned_customers
    churn_rate = churned_customers / total_customers
    
    # 1. Monthly Recurrent Revenue (MRR) Calculations
    total_mrr = df['Monthly_Charges'].sum()
    mrr_lost = df.loc[churn_mask, 'Monthly_Charges'].sum()
    mrr_retained = df.loc[~churn_mask, 'Monthly_Charges'].sum()
    mrr_loss_percentage = mrr_lost / total_mrr
    
    # 2. Customer Lifetime Value (CLV) Modeling
    # CLV = (ARPU * Gross Margin) / Monthly Churn Rate
    # Assuming standard SaaS / Telecom gross margin of 75%
    gross_margin = 0.75
    arpu = df['Monthly_Charges'].mean()
    arpu_churned = df.loc[churn_mask, 'Monthly_Charges'].mean()
    
    # Global average CLV
    avg_clv = (arpu * gross_margin) / (churn_rate / 12) if churn_rate > 0 else 0
    total_clv_lost = churned_customers * ((arpu_churned * gross_margin) / (churn_rate / 12))
    
    # 3. Net Promoter Score (NPS) Proxy Metric
    # Correlated with support friction (Tech_Support_Tickets)
    # Tickets 0: Promoters (+50 NPS proxy)
    # Tickets 1-2: Passives (+10 NPS proxy)
    # Tickets 3+: Detractors (-70 NPS proxy)
    promoters = (df['Tech_Support_Tickets'] == 0).sum()
    passives = df['Tech_Support_Tickets'].isin([1, 2]).sum()
    detractors = (df['Tech_Support_Tickets'] >= 3).sum()
    nps_proxy = round(((promoters - detractors) / total_customers) * 100, 1)
    
    # 4. Targeted Retention Campaign Simulation (Step 5 Priority Cohort)
    # Priority segment: Tenure < 12 months AND Tech_Support_Tickets > 3
    target_mask = (df['Tenure_Months'] < 12) & (df['Tech_Support_Tickets'] > 3)
    target_cohort = df[target_mask]
    target_size = len(target_cohort)
    target_churned = (target_cohort['Churn_Status'] == 'Yes').sum()
    target_churn_rate = target_churned / target_size if target_size > 0 else 0
    target_mrr_at_risk = target_cohort['Monthly_Charges'].sum()
    target_arpu = target_cohort['Monthly_Charges'].mean()
    
    # Campaign Intervention Assumptions:
    # Dedicated Senior Concierge Tech Resolution + $20/month bill discount for 3 months
    cost_per_contact = 25.0  # Concierge engineering support cost
    discount_incentive = 60.0 # $20 * 3 months bill relief
    crc_per_customer = cost_per_contact + discount_incentive # $85 CRC
    total_campaign_cost = target_size * crc_per_customer
    
    # Realistic rescue/retention success rate of 35% among would-be churners
    retention_rescue_rate = 0.35
    customers_saved = int(target_churned * retention_rescue_rate)
    
    # Financial Returns
    # Annualized rescued revenue
    annual_revenue_saved = customers_saved * target_arpu * 12
    # Saved CLV over customer lifecycle
    cohort_clv = (target_arpu * gross_margin) / (target_churn_rate / 12) if target_churn_rate > 0 else 0
    total_clv_saved = customers_saved * cohort_clv
    
    net_campaign_profit = total_clv_saved - total_campaign_cost
    campaign_roi_percentage = (net_campaign_profit / total_campaign_cost) * 100 if total_campaign_cost > 0 else 0
    
    financial_summary = {
        "dataset_kpis": {
            "total_customers": int(total_customers),
            "churned_customers": int(churned_customers),
            "retained_customers": int(retained_customers),
            "customer_churn_rate_pct": round(churn_rate * 100, 2),
            "total_mrr_usd": round(total_mrr, 2),
            "mrr_lost_usd": round(mrr_lost, 2),
            "mrr_loss_percentage": round(mrr_loss_percentage * 100, 2),
            "overall_arpu_usd": round(arpu, 2),
            "avg_customer_lifetime_value_usd": round(avg_clv, 2),
            "total_clv_lost_usd": round(total_clv_lost, 2),
            "nps_proxy_score": nps_proxy
        },
        "targeted_campaign_strategy": {
            "target_segment_definition": "Tenure < 12 Months & Tech_Support_Tickets > 3",
            "target_cohort_size": int(target_size),
            "target_cohort_churn_rate_pct": round(target_churn_rate * 100, 2),
            "target_cohort_mrr_at_risk_usd": round(target_mrr_at_risk, 2),
            "customer_retention_cost_crc_per_user_usd": round(crc_per_customer, 2),
            "total_campaign_budget_usd": round(total_campaign_cost, 2),
            "projected_customers_saved": int(customers_saved),
            "projected_annual_revenue_saved_usd": round(annual_revenue_saved, 2),
            "projected_lifetime_value_saved_usd": round(total_clv_saved, 2),
            "net_retention_profit_usd": round(net_campaign_profit, 2),
            "campaign_roi_pct": round(campaign_roi_percentage, 2)
        }
    }
    
    # Save financial summary JSON
    json_path = os.path.join(reports_dir, 'retention_financial_summary.json')
    with open(json_path, 'w') as f:
        json.dump(financial_summary, f, indent=4)
    print(f"Saved financial strategy metrics to: {json_path}")
    
    # --- Generate Retention ROI Visualization ---
    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(9, 5.5))
    
    categories = ['Campaign Budget\n(CRC Cost)', 'Rescued 1-Yr\nRevenue', 'Rescued Customer\nLifetime Value (CLV)', 'Net Campaign\nProfit']
    values = [
        total_campaign_cost / 1000,
        annual_revenue_saved / 1000,
        total_clv_saved / 1000,
        net_campaign_profit / 1000
    ]
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#1abc9c']
    
    bars = ax.bar(categories, values, color=colors, width=0.55, edgecolor='black', linewidth=1)
    ax.set_ylabel('Amount ($ in Thousands)', fontsize=12)
    ax.set_title(f'Targeted Retention Campaign Financial ROI\nCohort: Tenure < 12m & >3 Tickets (ROI: {campaign_roi_percentage:.1f}%)',
                 fontsize=13, fontweight='bold', pad=15)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:,.1f}K",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    roi_plot_path = os.path.join(viz_dir, 'retention_campaign_roi.png')
    plt.savefig(roi_plot_path, dpi=300)
    plt.close()
    print(f"Saved retention ROI chart to: {roi_plot_path}")
    
    return financial_summary

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_path = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    compute_financial_retention_analytics(clean_path, base_dir)
