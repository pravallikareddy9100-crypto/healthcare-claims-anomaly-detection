import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sys

sys.path.insert(0, r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly")
from config import DB_CONFIG

engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

print("Loading claims features...")
df = pd.read_sql("SELECT * FROM claims_features", engine)
print(f"Loaded {len(df)} claims")

# Select features for the model
features = [
    'claim_amount',
    'claims_per_provider',
    'avg_claim_per_provider',
    'amount_vs_avg',
    'amount_zscore',
    'duplicate_flag',
    'high_volume_flag',
    'high_amount_flag'
]

# Drop rows with nulls in feature columns
df_model = df[features].copy()
df_model = df_model.fillna(0)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_model)

# Train Isolation Forest
print("Training Isolation Forest model...")
model = IsolationForest(
    contamination=0.05,  # expect ~5% anomalies
    random_state=42,
    n_estimators=100
)
model.fit(X_scaled)

# Score every claim
print("Scoring claims...")
df['anomaly_prediction'] = model.predict(X_scaled)  # -1 = anomaly, 1 = normal
df['anomaly_score'] = model.decision_function(X_scaled)  # lower = more anomalous

# Convert to 0-100 suspicion score (higher = more suspicious)
min_score = df['anomaly_score'].min()
max_score = df['anomaly_score'].max()
df['suspicion_score'] = (
    100 * (1 - (df['anomaly_score'] - min_score) / (max_score - min_score))
).round(1)

# Flag anomalies
df['is_anomaly'] = (df['anomaly_prediction'] == -1).astype(int)

# Add risk tier
def risk_tier(score):
    if score >= 80:
        return 'HIGH'
    elif score >= 60:
        return 'MEDIUM'
    else:
        return 'LOW'

df['risk_tier'] = df['suspicion_score'].apply(risk_tier)

# Save results
print("Saving scored claims to database...")
df.to_sql('claims_scored', engine, if_exists='replace', index=False)

# Summary
anomalies = df[df['is_anomaly'] == 1]
print("\n--- Model Results ---")
print(f"Total claims scored:     {len(df):,}")
print(f"Anomalies detected:      {len(anomalies):,}")
print(f"Anomaly rate:            {len(anomalies)/len(df)*100:.1f}%")
print(f"Total $ in anomalies:    ${anomalies['claim_amount'].sum():,.2f}")
print(f"\nRisk Tier Breakdown:")
print(df['risk_tier'].value_counts().to_string())
print(f"\nTop 10 Most Suspicious Claims:")
top10 = df.nlargest(10, 'suspicion_score')[
    ['clm_id', 'provider_id', 'claim_amount', 'suspicion_score', 'risk_tier']
]
print(top10.to_string(index=False))
print("\nModel complete!")