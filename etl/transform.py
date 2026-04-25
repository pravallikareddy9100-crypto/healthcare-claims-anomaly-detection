import pandas as pd
from sqlalchemy import create_engine
import sys

sys.path.insert(0, r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly")
from config import DB_CONFIG

engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

print("Loading inpatient claims...")
df = pd.read_sql("SELECT * FROM inpatient_claims_raw", engine)
print(f"Loaded {len(df)} claims")

df['clm_pmt_amt'] = pd.to_numeric(df['clm_pmt_amt'], errors='coerce')

provider_counts = df.groupby('at_physn_npi')['clm_id'].count().reset_index()
provider_counts.columns = ['provider_id', 'claims_per_provider']

provider_avg = df.groupby('at_physn_npi')['clm_pmt_amt'].mean().reset_index()
provider_avg.columns = ['provider_id', 'avg_claim_per_provider']

df = df.rename(columns={'at_physn_npi': 'provider_id', 'clm_pmt_amt': 'claim_amount'})
df = df.merge(provider_counts, on='provider_id', how='left')
df = df.merge(provider_avg, on='provider_id', how='left')

df['amount_vs_avg'] = df['claim_amount'] - df['avg_claim_per_provider']
mean_amt = df['claim_amount'].mean()
std_amt = df['claim_amount'].std()
df['amount_zscore'] = (df['claim_amount'] - mean_amt) / std_amt
df['duplicate_flag'] = df.duplicated(subset=['bene_id', 'clm_from_dt', 'provider_id'], keep=False).astype(int)
threshold = df['claims_per_provider'].quantile(0.95)
df['high_volume_flag'] = (df['claims_per_provider'] > threshold).astype(int)
df['high_amount_flag'] = (df['amount_zscore'].abs() > 2).astype(int)

df.to_sql('claims_features', engine, if_exists='replace', index=False)

print("\n--- Feature Summary ---")
print(f"Total claims: {len(df)}")
print(f"Duplicate claims: {df['duplicate_flag'].sum()}")
print(f"High volume providers: {df['high_volume_flag'].sum()}")
print(f"High amount claims: {df['high_amount_flag'].sum()}")
print(f"Avg claim amount: ${df['claim_amount'].mean():,.2f}")
print(f"Max claim amount: ${df['claim_amount'].max():,.2f}")
print("\nDone!")