#!/usr/bin/env python3
"""
IERC Risk Score ML Baseline
RandomForest regression to validate/recalibrate additive model weights.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import json
import sys

print("Loading features...")
X = pd.read_parquet('lakehouse/curated/ierc_features_h3_8.parquet')

print("Loading target...")
y = pd.read_parquet('lakehouse/curated/ierc_risk_h3_8.parquet')[['h3_cell_8', 'ierc_score']]

print(f"Features: {X.shape}, Target: {y.shape}")

df = X.merge(y, on='h3_cell_8').dropna(subset=['ierc_score'])
print(f"Merged: {df.shape}")

feat_cols = [c for c in df.columns if c not in ['h3_cell_8', 'ierc_score']]
print(f"Feature columns ({len(feat_cols)}): {feat_cols}")

# Split
train, test = train_test_split(df, test_size=0.2, random_state=42)
print(f"Train: {train.shape}, Test: {test.shape}")

# RandomForest
print("Training RandomForest...")
rf = RandomForestRegressor(n_estimators=200, max_depth=12, n_jobs=-1, random_state=42)
rf.fit(train[feat_cols], train['ierc_score'])

# Eval
pred = rf.predict(test[feat_cols])
r2 = r2_score(test['ierc_score'], pred)
mae = mean_absolute_error(test['ierc_score'], pred)
print(f"\nR²: {r2:.4f}")
print(f"MAE: {mae:.4f}")

# Feature importance
imp = pd.Series(rf.feature_importances_, index=feat_cols).sort_values(ascending=False)
print("\nTop 10 Feature Importances:")
for i, (feat, val) in enumerate(imp.head(10).items(), 1):
    print(f"  {i:2d}. {feat:<35s} {val:.4f}")

# Save model + metadata
joblib.dump(rf, 'models/ierc_rf_v1.pkl')
meta = {
    'features': feat_cols,
    'importance': imp.to_dict(),
    'metrics': {'r2': float(r2), 'mae': float(mae)},
    'n_train': int(train.shape[0]),
    'n_test': int(test.shape[0])
}
with open('models/ierc_rf_v1_meta.json', 'w') as f:
    json.dump(meta, f, indent=2)

print("\nSaved: models/ierc_rf_v1.pkl, models/ierc_rf_v1_meta.json")

# Ponytail check: R² threshold for "worth recalibrating weights"
if r2 > 0.7:
    print(f"\n✓ R²={r2:.3f} > 0.7 — feature importances are reliable for weight recalibration")
    sys.exit(0)
else:
    print(f"\n✗ R²={r2:.3f} ≤ 0.7 — model not predictive enough, check features/target")
    sys.exit(1)