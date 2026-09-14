"""
Predictive Modeling & Evaluation Module for Customer Churn & Retention Analytics.
Corresponds to Step 4 in Methodology:
- Trains Logistic Regression, Random Forest, and XGBoost classifiers
- Evaluates ROC-AUC, Recall, Precision, F1-Score, and PR-AUC
- Exports ROC curves, feature importances, and confusion matrices
- Persists best trained model pipeline for production inference
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    roc_auc_score, recall_score, precision_score,
    f1_score, accuracy_score, roc_curve, precision_recall_curve,
    confusion_matrix, classification_report
)

from feature_engineering import prepare_train_test_data

def train_and_evaluate_models(clean_data_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    models_dir = os.path.join(output_dir, 'models')
    viz_dir = os.path.join(output_dir, 'visualizations')
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Load and partition data
    df = pd.read_csv(clean_data_path)
    data_dict = prepare_train_test_data(df)
    
    X_train = data_dict['X_train']
    X_test = data_dict['X_test']
    y_train = data_dict['y_train']
    y_test = data_dict['y_test']
    preprocessor = data_dict['preprocessor']
    
    # Calculate class imbalance weighting
    churn_count = (y_train == 1).sum()
    non_churn_count = (y_train == 0).sum()
    scale_pos_weight = non_churn_count / churn_count
    print(f"Training set: Non-churn={non_churn_count}, Churn={churn_count} (ratio: {scale_pos_weight:.2f})")
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000, class_weight='balanced', random_state=42
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=150, max_depth=8, class_weight='balanced',
            random_state=42, n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=150, max_depth=5, learning_rate=0.08,
            scale_pos_weight=scale_pos_weight, random_state=42,
            eval_metric='logloss'
        )
    }
    
    results = {}
    fitted_pipelines = {}
    test_probs = {}
    test_preds = {}
    
    print("\n--- Training and Evaluating Models ---")
    for name, clf in models.items():
        pipe = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]
        
        roc_auc = roc_auc_score(y_test, y_prob)
        rec = recall_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        
        results[name] = {
            'Accuracy': round(acc, 4),
            'Precision': round(prec, 4),
            'Recall': round(rec, 4),
            'F1_Score': round(f1, 4),
            'ROC_AUC': round(roc_auc, 4)
        }
        fitted_pipelines[name] = pipe
        test_probs[name] = y_prob
        test_preds[name] = y_pred
        
        print(f"[{name}] ROC-AUC: {roc_auc:.4f} | Recall: {rec:.4f} | Precision: {prec:.4f} | F1: {f1:.4f} | Acc: {acc:.4f}")
        
    # Save benchmark metrics to JSON
    benchmark_file = os.path.join(reports_dir, 'model_benchmarks.json')
    with open(benchmark_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\nModel benchmark metrics saved to: {benchmark_file}")
    
    # Determine best model based on ROC-AUC and Recall
    best_model_name = max(results.keys(), key=lambda k: results[k]['ROC_AUC'])
    print(f"Best overall model: {best_model_name}")
    
    best_pipe = fitted_pipelines[best_model_name]
    best_model_path = os.path.join(models_dir, 'best_churn_model.joblib')
    joblib.dump(best_pipe, best_model_path)
    print(f"Best model pipeline saved to: {best_model_path}")
    
    # --- Generate Visualizations ---
    sns.set_theme(style='whitegrid')
    
    # 1. ROC Curves Plot
    plt.figure(figsize=(8, 6))
    for name in models.keys():
        fpr, tpr, _ = roc_curve(y_test, test_probs[name])
        auc = results[name]['ROC_AUC']
        plt.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {auc:.3f})")
    plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Chance (AUC = 0.500)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    plt.ylabel('True Positive Rate (Recall)', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curves', fontsize=14, fontweight='bold', pad=15)
    plt.legend(loc="lower right", fontsize=11)
    plt.tight_layout()
    roc_plot_path = os.path.join(viz_dir, 'model_roc_curves.png')
    plt.savefig(roc_plot_path, dpi=300)
    plt.close()
    print(f"Saved ROC curves plot to: {roc_plot_path}")
    
    # 2. Confusion Matrices Plot
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for idx, (name, y_pred) in enumerate(test_preds.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                    cbar=False, annot_kws={"size": 13})
        axes[idx].set_title(f"{name}\nRecall: {results[name]['Recall']:.2%}", fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label', fontsize=11)
        axes[idx].set_ylabel('Actual Label' if idx == 0 else '', fontsize=11)
        axes[idx].set_xticklabels(['Retained (0)', 'Churned (1)'])
        axes[idx].set_yticklabels(['Retained (0)', 'Churned (1)'])
    plt.suptitle('Confusion Matrix Comparison Across Models', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    cm_plot_path = os.path.join(viz_dir, 'confusion_matrices.png')
    plt.savefig(cm_plot_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrices plot to: {cm_plot_path}")
    
    # 3. Feature Importance Plot (Extracted from Random Forest & XGBoost)
    # Extract feature names from preprocessor
    fitted_preprocessor = best_pipe.named_steps['preprocessor']
    cat_encoder = fitted_preprocessor.named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(data_dict['categorical_features']).tolist()
    all_feature_names = data_dict['numeric_features'] + cat_feature_names
    
    rf_clf = fitted_pipelines['Random Forest'].named_steps['classifier']
    xgb_clf = fitted_pipelines['XGBoost'].named_steps['classifier']
    
    feat_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Random_Forest': rf_clf.feature_importances_,
        'XGBoost': xgb_clf.feature_importances_
    })
    feat_df['Combined_Score'] = (feat_df['Random_Forest'] + feat_df['XGBoost']) / 2
    feat_df = feat_df.sort_values(by='Combined_Score', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feat_df, y='Feature', x='Combined_Score', palette='mako')
    plt.title('Top 10 Feature Importances (Random Forest & XGBoost)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Normalized Relative Importance', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    fi_plot_path = os.path.join(viz_dir, 'feature_importance.png')
    plt.savefig(fi_plot_path, dpi=300)
    plt.close()
    print(f"Saved feature importance plot to: {fi_plot_path}")
    
    return results, best_model_name

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_path = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    train_and_evaluate_models(clean_path, base_dir)
