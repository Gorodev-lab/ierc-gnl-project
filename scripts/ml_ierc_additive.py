#!/usr/bin/env python3
"""
IERC Additive Model ML Baseline
RandomForest regression to learn official POA 2026 additive IERC formula weights.
Target: IERC_additive = H*0.40 + V*0.60 with 6 components.
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
X = pd.read_parquet('lakehouse/curated/ierc_features_adaptive_h3.parquet')
print(f"Features: {X.shape}")

# 2. Compute OFFICIAL ADDITIVE IERC target (same formula as MethodologyPanel.tsx)
def norm_0_100(s, invert=False):
    mn, mx = s.min(), s.max()
    if mx > mn:
        r = ((s - mn) / (mx - mn)) * 100
    else:
        r = pd.Series(50.0, index=s.index)
    if invert:
        r = 100.0 - r
    return r.clip(0.0, 100.0)

# H components (Amenaza + Exposición = 40%)
s_esfuerzo = norm_0_100(X['pangas_densidad_esfuerzo'].fillna(0))           # Exposición
s_gnl = norm_0_100(X['asea_count'].fillna(0))                               # Amenaza (infra GNL)
s_rutas = norm_0_100(X['asea_gasoducto'].fillna(0))                         # Amenaza (rutas/ductos)

H = (0.5 * s_esfuerzo) + (0.3 * s_gnl) + (0.2 * s_rutas)  # sub-indice H normalizado 0-100

# V components (Vulnerabilidad = 60%)  
s_sens = norm_0_100(X['chlor_a_mean'].fillna(0))                           # Sensibilidad (proxy clorofila)
s_dep = norm_0_100(pd.Series(0.7, index=X.index))                          # Dependencia (constante por ahora)
s_bio = norm_0_100(pd.Series(0.85, index=X.index))                         # Biocultural (constante)
s_cap = norm_0_100(pd.Series(0.35, index=X.index), invert=True)            # 1-Cap.Adaptativa

V = (0.25*s_sens + 0.25*s_dep + 0.20*s_bio + 0.15*s_cap) / 0.85  # renormalizado sin género

# IERC ADITIVO OFICIAL: H*0.40 + V*0.60
ierc_additive = (H * 0.40) + (V * 0.60)

print(f"IERC additive target: mean={ierc_additive.mean():.2f}, std={ierc_additive.std():.2f}, min={ierc_additive.min():.2f}, max={ierc_additive.max():.2f}")

# 3. Train RF to learn this mapping (captura no-lineal + interacciones)
df = X.copy()
df['ierc_additive'] = ierc_additive
feat_cols = [c for c in df.columns if c not in ['h3_cell', 'resolution', 'ierc_additive']]

train, test = train_test_split(df, test_size=0.2, random_state=42)
print(f"Train: {train.shape}, Test: {test.shape}")

rf = RandomForestRegressor(n_estimators=200, max_depth=12, n_jobs=-1, random_state=42)
rf.fit(train[feat_cols], train['ierc_additive'])

pred = rf.predict(test[feat_cols])
r2 = r2_score(test['ierc_additive'], pred)
mae = mean_absolute_error(test['ierc_additive'], pred)
print(f"\nR²: {r2:.4f}")
print(f"MAE: {mae:.4f}")

# Feature importance
imp = pd.Series(rf.feature_importances_, index=feat_cols).sort_values(ascending=False)
print("\nTop 10 Feature Importances:")
for i, (feat, val) in enumerate(imp.head(10).items(), 1):
    print(f"  {i:2d}. {feat:<35s} {val:.4f}")

# Save model + metadata
joblib.dump(rf, 'models/ierc_additive_rf_v1.pkl')
meta = {
    'features': feat_cols,
    'importance': imp.to_dict(),
    'metrics': {'r2': float(r2), 'mae': float(mae)},
    'n_train': int(train.shape[0]),
    'n_test': int(test.shape[0])
}
with open('models/ierc_additive_rf_v1_meta.json', 'w') as f:
    json.dump(meta, f, indent=2)

print("\nSaved: models/ierc_additive_rf_v1.pkl, models/ierc_additive_rf_v1_meta.json")

# Ponytail check: R² threshold for "worth recalibrating weights"
if r2 > 0.8:
    print(f"\n✓ R²={r2:.3f} > 0.8 — feature importances are reliable for weight recalibration")
    sys.exit(0)
else:
    print(f"\n✗ R²={r2:.3f} ≤ 0.8 — model not predictive enough, check features/target")
    sys.exit(1)