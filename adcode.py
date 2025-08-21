# ---------- AI-based Ad Performance Predictor (CTR & Conversion Rate) ----------
# Requires: pandas, numpy, scikit-learn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error

# 1) Load data
historical = pd.read_csv("adperformancepredictor/historical_ads.csv")
upcoming = pd.read_csv("adperformancepredictor/upcoming_creatives.csv")

# 2) Features & targets
text_col = "headline"
cat_cols = ["platform", "creative_type", "target_audience"]
num_cols_hist = ["spend", "impressions"]
X = historical[[text_col] + cat_cols + num_cols_hist].copy()
y_ctr = historical["ctr"].values
y_cvr = historical["conversion_rate"].values

# 3) Preprocess & models
preprocess = ColumnTransformer([
    ("headline_tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=3, max_features=5000), text_col),
    ("cat_ohe", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("nums", "passthrough", num_cols_hist),
])

ridge_ctr = Pipeline([("prep", preprocess), ("model", Ridge(alpha=1.0, solver="sag", random_state=42))])
rf_ctr    = Pipeline([("prep", preprocess), ("model", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))])

ridge_cvr = Pipeline([("prep", preprocess), ("model", Ridge(alpha=1.0, solver="sag", random_state=42))])
rf_cvr    = Pipeline([("prep", preprocess), ("model", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))])

# 4) Quick validation (optional but recommended)
X_train, X_val, y_ctr_train, y_ctr_val, y_cvr_train, y_cvr_val = train_test_split(
    X, y_ctr, y_cvr, test_size=0.2, random_state=42
)

def evaluate(model, Xtr, ytr, Xv, yv):
    model.fit(Xtr, ytr)
    return {
        "r2_train": r2_score(ytr, model.predict(Xtr)),
        "r2_val":   r2_score(yv,  model.predict(Xv)),
        "mae_val":  mean_absolute_error(yv, model.predict(Xv)),
    }

m_ctr_ridge = evaluate(ridge_ctr, X_train, y_ctr_train, X_val, y_ctr_val)
m_ctr_rf    = evaluate(rf_ctr,    X_train, y_ctr_train, X_val, y_ctr_val)
m_cvr_ridge = evaluate(ridge_cvr, X_train, y_cvr_train, X_val, y_cvr_val)
m_cvr_rf    = evaluate(rf_cvr,    X_train, y_cvr_train, X_val, y_cvr_val)

best_ctr_model = rf_ctr if m_ctr_rf["r2_val"] >= m_ctr_ridge["r2_val"] else ridge_ctr
best_cvr_model = rf_cvr if m_cvr_rf["r2_val"] >= m_cvr_ridge["r2_val"] else ridge_cvr

# 5) Refit on full historical
best_ctr_model.fit(X, y_ctr)
best_cvr_model.fit(X, y_cvr)

# 6) Predict for upcoming
X_new = upcoming[[text_col] + cat_cols + ["planned_spend", "expected_impressions"]].rename(
    columns={"planned_spend":"spend", "expected_impressions":"impressions"}
)

pred_ctr = np.clip(best_ctr_model.predict(X_new), 0.0005, 0.6)
pred_cvr = np.clip(best_cvr_model.predict(X_new), 0.00005, 0.3)

upcoming["predicted_ctr"] = pred_ctr
upcoming["predicted_conversion_rate"] = pred_cvr
upcoming["predicted_clicks"] = (pred_ctr * X_new["impressions"]).round().astype(int)
upcoming["predicted_conversions"] = (pred_cvr * X_new["impressions"]).round().astype(int)

upcoming.to_csv("predicted_ad_performance.csv", index=False)
print("Saved: predicted_ad_performance.csv")
print(upcoming[["platform","headline","creative_type","target_audience",
                "predicted_ctr","predicted_conversion_rate",
                "predicted_clicks","predicted_conversions"]])
# ------------------------------------------------------------------------------
