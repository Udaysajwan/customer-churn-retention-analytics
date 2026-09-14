"""
Data Cleansing Module for Customer Churn & Retention Analytics.
Corresponds to Step 1 in Methodology:
- Ingests raw data
- Detects and handles whitespace/missing values in Total_Charges
- Converts data types appropriately
- Validates data distributions and formats
"""

import os
import pandas as pd
import numpy as np

def clean_churn_data(raw_filepath, output_filepath=None):
    print(f"Loading raw dataset from: {raw_filepath}")
    df = pd.read_csv(raw_filepath)
    
    initial_shape = df.shape
    print(f"Initial dataset shape: {initial_shape}")
    
    # 1. Detect missing/whitespace values in Total_Charges
    # Replace whitespace strings with NaN
    raw_whitespace_count = (df['Total_Charges'].astype(str).str.strip() == '').sum()
    print(f"Detected {raw_whitespace_count} records with empty/whitespace Total_Charges.")
    
    # Convert Total_Charges to numeric
    df['Total_Charges'] = pd.to_numeric(df['Total_Charges'].astype(str).str.strip(), errors='coerce')
    nan_count = df['Total_Charges'].isna().sum()
    print(f"Total NaN records in Total_Charges after coercion: {nan_count}")
    
    # 2. Imputation logic for Total_Charges
    # For customers with Tenure_Months == 0, Total_Charges is 0.0 (they haven't completed a billing cycle)
    zero_tenure_mask = (df['Tenure_Months'] == 0) & df['Total_Charges'].isna()
    df.loc[zero_tenure_mask, 'Total_Charges'] = 0.0
    
    # For any remaining missing Total_Charges, impute with Monthly_Charges * Tenure_Months
    remaining_nan = df['Total_Charges'].isna()
    if remaining_nan.sum() > 0:
        df.loc[remaining_nan, 'Total_Charges'] = df.loc[remaining_nan, 'Monthly_Charges'] * df.loc[remaining_nan, 'Tenure_Months']
    
    print(f"Remaining null values across dataset:\n{df.isna().sum()}")
    
    # 3. Data type validations
    df['Tenure_Months'] = df['Tenure_Months'].astype(int)
    df['Monthly_Charges'] = df['Monthly_Charges'].astype(float)
    df['Total_Charges'] = df['Total_Charges'].astype(float)
    df['Tech_Support_Tickets'] = df['Tech_Support_Tickets'].astype(int)
    
    # 4. Standardize Categorical Strings
    categorical_cols = [
        'Contract_Type', 'Payment_Method', 'Internet_Service_Type',
        'Paperless_Billing', 'Churn_Status'
    ]
    for col in categorical_cols:
        df[col] = df[col].astype(str).str.strip()
        
    print("Data cleansing successfully completed.")
    print(f"Summary Statistics:\n{df.describe()}")
    
    if output_filepath:
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df.to_csv(output_filepath, index=False)
        print(f"Saved cleansed dataset to: {output_filepath}")
        
    return df

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw_customer_churn_data.csv')
    clean_path = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    clean_churn_data(raw_path, clean_path)
