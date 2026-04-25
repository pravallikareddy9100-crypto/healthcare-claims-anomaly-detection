import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sys

sys.path.insert(0, r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly")
from config import DB_CONFIG

engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

print("Loading beneficiary data...")
df_bene = pd.read_csv(r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly\data\beneficiary_2024.csv", sep="|", low_memory=False)
df_bene.columns = df_bene.columns.str.strip().str.lower()
df_bene.to_sql("beneficiary_raw", engine, if_exists="replace", index=False)
print(f"Loaded {len(df_bene)} beneficiary rows")

print("Loading inpatient claims...")
df_inp = pd.read_csv(r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly\data\inpatient.csv", sep="|", low_memory=False)
df_inp.columns = df_inp.columns.str.strip().str.lower()
df_inp.to_sql("inpatient_claims_raw", engine, if_exists="replace", index=False)
print(f"Loaded {len(df_inp)} inpatient rows")

print("Loading outpatient claims...")
df_out = pd.read_csv(r"C:\Users\pravallika\Desktop\healthcare-claims-anomaly\data\Outpatient\outpatient.csv", sep="|", low_memory=False)
df_out.columns = df_out.columns.str.strip().str.lower()
df_out.to_sql("outpatient_claims_raw", engine, if_exists="replace", index=False)
print(f"Loaded {len(df_out)} outpatient rows")

print("\nAll data loaded successfully!")