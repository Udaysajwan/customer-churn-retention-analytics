"""
Feature Engineering Module for Customer Churn & Retention Analytics.
Corresponds to Step 3 in Methodology:
- Creates Average_Monthly_Spend
- Creates Support_Ticket_Frequency
- Creates Tenure_Group (binned tenure bands)
- Creates Auto_Payment_Flag and High_Risk_Segment indicators
- Prepares One-Hot Encoding and feature scaling pipelines for ML modeling
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

def engineer_features(df):
    """
    Applies feature engineering domain logic to customer churn dataset.
    """
    df = df.copy()
    
    # 1. Average_Monthly_Spend
    # If tenure is 0, average spend is equal to current Monthly_Charges
    safe_tenure = np.where(df['Tenure_Months'] == 0, 1, df['Tenure_Months'])
    df['Average_Monthly_Spend'] = np.where(
        df['Tenure_Months'] == 0,
        df['Monthly_Charges'],
        np.round(df['Total_Charges'] / safe_tenure, 2)
    )
    
    # 2. Spend Variation Ratio (current monthly charges relative to historical average spend)
    df['Spend_Ratio'] = np.round(df['Monthly_Charges'] / (df['Average_Monthly_Spend'] + 1e-5), 2)
    
    # 3. Support_Ticket_Frequency (tickets per month of tenure, +1 avoids division by zero)
    df['Support_Ticket_Frequency'] = np.round(df['Tech_Support_Tickets'] / (df['Tenure_Months'] + 1), 3)
    
    # 4. Critical ticket threshold indicator (> 3 calls indicates ~82% churn probability)
    df['High_Support_Tickets_Flag'] = (df['Tech_Support_Tickets'] > 3).astype(int)
    
    # 5. Tenure_Group Binned Categorical
    bins = [-1, 12, 24, 48, 72]
    labels = ['0-12 Months', '13-24 Months', '25-48 Months', '49-72 Months']
    df['Tenure_Group'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels)
    
    # 6. Automatic Payment Method Flag
    df['Auto_Payment_Flag'] = df['Payment_Method'].isin([
        'Bank transfer (automatic)', 'Credit card (automatic)'
    ]).astype(int)
    
    # 7. High-Risk Retention Target Cohort Flag (Tenure < 12 months & > 3 tickets)
    df['Target_Retention_Cohort'] = (
        (df['Tenure_Months'] < 12) & (df['Tech_Support_Tickets'] > 3)
    ).astype(int)
    
    return df

def get_preprocessor(categorical_features, numeric_features):
    """
    Builds a Scikit-Learn ColumnTransformer for categorical One-Hot Encoding and numerical scaling.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features)
        ]
    )
    return preprocessor

def prepare_train_test_data(df, test_size=0.2, random_state=42):
    """
    Splits dataset into stratified train/test partitions.
    """
    engineered_df = engineer_features(df)
    
    # Target variable
    y = (engineered_df['Churn_Status'] == 'Yes').astype(int)
    
    # Feature columns for modeling
    categorical_features = [
        'Contract_Type', 'Payment_Method', 'Internet_Service_Type',
        'Paperless_Billing', 'Tenure_Group'
    ]
    numeric_features = [
        'Tenure_Months', 'Monthly_Charges', 'Total_Charges',
        'Tech_Support_Tickets', 'Average_Monthly_Spend',
        'Support_Ticket_Frequency', 'Auto_Payment_Flag',
        'High_Support_Tickets_Flag'
    ]
    
    feature_cols = categorical_features + numeric_features
    X = engineered_df[feature_cols]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    preprocessor = get_preprocessor(categorical_features, numeric_features)
    
    return {
        'engineered_df': engineered_df,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'categorical_features': categorical_features,
        'numeric_features': numeric_features,
        'preprocessor': preprocessor
    }

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_path = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        data_dict = prepare_train_test_data(df)
        print("Feature engineering successfully executed.")
        print(f"Engineered dataframe shape: {data_dict['engineered_df'].shape}")
        print(f"X_train shape: {data_dict['X_train'].shape}, X_test shape: {data_dict['X_test'].shape}")
