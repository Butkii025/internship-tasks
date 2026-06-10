"""
TRAIN_MODEL.PY
Author: Priyanshu Vijay
Description: Production Machine Learning Training Pipeline.
             Loads cleaned JSON records, engineers categorical dimensions 
             (Publisher & Book_Type), runs a 5-fold cross-validation loop, 
             and serializes model artifacts for real-time inference.
"""

import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def load_data(filepath):
    """Loads records from the local JSON storage warehouse."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Storage file missing: {filepath}. Run pipeline.py first!")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    return pd.DataFrame(payload['data'])

def train_production_engine():
    print("🚀 Starting Production Machine Learning Engine...")
    
    # 1. Load Data Layers
    print("📂 Loading raw data layers...")
    data_file = "retrieve_data.json"
    df = load_data(data_file)
    
    # 2. Stage 1: Feature Transformation & Category Aggregation
    print("📐 Executing Stage 1: Feature Transformation & Category Aggregation...")
    
    # Handle rare publishers by grouping them into 'Other' to maintain matrix stability
    publisher_counts = df['Publisher'].value_counts()
    rare_publishers = publisher_counts[publisher_counts < 2].index
    df['Publisher'] = df['Publisher'].apply(lambda x: 'Other' if x in rare_publishers else x)
    
    # Isolate Target (y) and Features (X)
    y = df['Pages'].values
    
    # One-Hot Encode both 'Publisher' AND the new 'Book_Type' feature safely!
    categorical_features = ['Publisher', 'Book_Type']
    X_encoded = pd.get_dummies(df[['Year'] + categorical_features], columns=categorical_features, drop_first=True)
    
    # Convert boolean true/false flags to numeric integers (1/0) for sklearn stability
    for col in X_encoded.columns:
        if X_encoded[col].dtype == 'bool':
            X_encoded[col] = X_encoded[col].astype(int)
            
    feature_names = X_encoded.columns.tolist()
    X = X_encoded.values
    
    # 3. Stage 2: Running 5-Fold Cross-Validation Utility Loop
    print("🔬 Executing Stage 2: Running 5-Fold Cross-Validation Data Utility Loop...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    mae_scores = []
    r2_scores = []
    
    for fold, (train_idx, test_idx) in enumerate(kf.split(X, y), 1):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        # Initialize and fit model fold
        fold_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)
        fold_model.fit(X_train, y_train)
        
        # Predict and Score
        predictions = fold_model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        mae_scores.append(mae)
        r2_scores.append(r2)
        
    print("\n==================================================")
    print("📊 5-FOLD CROSS-VALIDATION DIAGNOSTICS")
    print("--------------------------------------------------")
    print(f"📉 Avg Cross-Validated MAE : {np.mean(mae_scores):.2f} pages")
    print(f"🎯 True Cross-Validated R² : {np.mean(r2_scores) * 100:.2f}%")
    print(f"📈 MAE Volatility (Std Dev) : {np.std(mae_scores):.2f} pages")
    print(f"📊 R² Folds Breakdown      : {[round(x * 100, 2) for x in r2_scores]}%")
    print("==================================================\n")
    
    # 4. Stage 3: Training Final Robust Model Ensemble
    print("✂️ Executing Stage 3: Fitting Final Random Forest Ensemble Model on Full Dataset...")
    final_model = RandomForestRegressor(n_estimators=150, random_state=42, max_depth=7)
    final_model.fit(X, y)
    
    # 5. Save production artifacts to disk
    os.makedirs('models', exist_ok=True)
    model_path = 'models/book_length_regressor.pkl'
    features_path = 'models/model_features.pkl'
    
    print("💾 Saving trained model binary artifact for production usage...")
    joblib.dump(final_model, model_path)
    joblib.dump(feature_names, features_path)
    
    print("🎉 Production ML deployment pipelines completed successfully!")

if __name__ == "__main__":
    train_production_engine()