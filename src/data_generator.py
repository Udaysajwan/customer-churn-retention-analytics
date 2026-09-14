"""
Data Generator for Customer Churn & Retention Analytics.
Synthesizes a realistic 10,000-record telecommunications customer dataset
calibrated to faithfully reflect the key findings specified in customer_churn_analytics.json:
1. Month-to-month churn rate is ~4x higher than two-year contracts.
2. Customers with >3 tech support tickets exhibit ~82% churn probability.
3. Automatic payment methods reduce churn by ~28% compared to manual methods.
4. Includes realistic missing/blank values in Total_Charges for new accounts (Tenure = 0).
"""

import numpy as np
import pandas as pd
import os

def generate_customer_churn_data(record_count=10000, random_state=42):
    np.random.seed(random_state)
    
    # 1. CustomerID
    customer_ids = [f"CUST-{i:05d}" for i in range(1, record_count + 1)]
    
    # 2. Tenure Months (0 to 72, with higher density in first 24 months)
    # Mixture of beta distribution scaled to 72 months
    raw_tenure = np.random.beta(a=0.8, b=1.4, size=record_count) * 72
    tenure_months = np.round(raw_tenure).astype(int)
    # Ensure a realistic small batch of brand new signups (tenure = 0)
    tenure_months[np.random.choice(record_count, size=15, replace=False)] = 0
    
    # 3. Contract Type: correlated with tenure
    contract_types = []
    for t in tenure_months:
        if t <= 12:
            probs = [0.75, 0.15, 0.10]
        elif t <= 36:
            probs = [0.45, 0.30, 0.25]
        else:
            probs = [0.25, 0.30, 0.45]
        contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], p=probs)
        contract_types.append(contract)
    contract_types = np.array(contract_types)
    
    # 4. Internet Service Type
    internet_types = np.random.choice(['Fiber optic', 'DSL', 'No'], size=record_count, p=[0.44, 0.34, 0.22])
    
    # 5. Monthly Charges
    monthly_charges = np.zeros(record_count)
    for i in range(record_count):
        itype = internet_types[i]
        if itype == 'No':
            monthly_charges[i] = np.random.uniform(18.25, 25.75)
        elif itype == 'DSL':
            monthly_charges[i] = np.random.uniform(42.50, 78.90)
        else: # Fiber optic
            monthly_charges[i] = np.random.uniform(70.00, 118.75)
    monthly_charges = np.round(monthly_charges, 2)
    
    # 6. Payment Method: Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)
    payment_methods = np.random.choice(
        ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
        size=record_count,
        p=[0.34, 0.16, 0.25, 0.25]
    )
    
    # 7. Paperless Billing
    paperless_billing = np.random.choice(['Yes', 'No'], size=record_count, p=[0.59, 0.41])
    
    # 8. Tech Support Tickets in past 6 months (Poisson distributed with long tail)
    base_tickets = np.random.poisson(lam=1.3, size=record_count)
    # Extra tickets for fiber optic or high monthly charges due to service complexity
    extra_prob = np.where(internet_types == 'Fiber optic', 0.25, 0.10)
    extra_tickets = np.random.binomial(n=3, p=extra_prob, size=record_count)
    tech_support_tickets = np.clip(base_tickets + extra_tickets, 0, 9)
    
    # 9. Total Charges: Monthly_Charges * Tenure_Months + slight realistic variance
    total_charges = []
    for i in range(record_count):
        t = tenure_months[i]
        m = monthly_charges[i]
        if t == 0:
            # Unbilled new accounts: represented as empty string or None (Methodology Step 1 requirement)
            total_charges.append(" ")
        else:
            # Accumulated charges with small variance
            tot = m * t * np.random.uniform(0.97, 1.03)
            total_charges.append(f"{tot:.2f}")
            
    # 10. Churn Status Generation Calibrated to JSON Key Findings:
    # Finding 1: Month-to-month churn is ~4x Two-year churn.
    # Finding 2: Tech_Support_Tickets > 3 yields ~82% churn probability.
    # Finding 3: Automatic payment methods reduce churn by ~28%.
    
    churn_status = []
    is_auto = np.isin(payment_methods, ['Bank transfer (automatic)', 'Credit card (automatic)'])
    
    for i in range(record_count):
        tickets = tech_support_tickets[i]
        contract = contract_types[i]
        auto_pay = is_auto[i]
        itype = internet_types[i]
        tenure = tenure_months[i]
        
        # Rule 1: High Tech Support Tickets (> 3) triggers ~82% churn rate
        if tickets > 3:
            p_churn = 0.82 + np.random.uniform(-0.03, 0.03)
        else:
            # Base probability determined by contract type
            if contract == 'Month-to-month':
                p_base = 0.435
            elif contract == 'One year':
                p_base = 0.190
            else: # Two year
                p_base = 0.108
                
            # Modifier 1: Automatic payment discount (-28% relative reduction)
            # e.g., manual payment retains full base, auto payment receives ~0.72 multiplier
            if auto_pay:
                p_base *= 0.72
            else:
                p_base *= 1.00
                
            # Modifier 2: Internet service type (Fiber optic churn is higher)
            if itype == 'Fiber optic':
                p_base += 0.05
            elif itype == 'No':
                p_base -= 0.04
                
            # Modifier 3: Tenure decay (longer tenure reduces churn)
            if tenure > 36:
                p_base *= 0.80
            elif tenure < 12:
                p_base *= 1.15
                
            # Modifier 4: Support tickets 0-3 effect
            if tickets == 0:
                p_base *= 0.85
            elif tickets == 3:
                p_base *= 1.25
                
            p_churn = np.clip(p_base, 0.02, 0.95)
            
        churn = 'Yes' if np.random.rand() < p_churn else 'No'
        churn_status.append(churn)
        
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'Tenure_Months': tenure_months,
        'Contract_Type': contract_types,
        'Monthly_Charges': monthly_charges,
        'Total_Charges': total_charges,
        'Payment_Method': payment_methods,
        'Tech_Support_Tickets': tech_support_tickets,
        'Internet_Service_Type': internet_types,
        'Paperless_Billing': paperless_billing,
        'Churn_Status': churn_status
    })
    
    return df

def save_raw_dataset(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_customer_churn_data(record_count=10000, random_state=42)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated and saved raw dataset with {len(df)} records to: {output_path}")
    return df

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, 'data', 'raw_customer_churn_data.csv')
    save_raw_dataset(target_csv)
