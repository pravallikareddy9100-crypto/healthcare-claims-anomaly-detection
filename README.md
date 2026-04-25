# healthcare-claims-anomaly-detection
End-to-end healthcare claims fraud detection pipeline using Python, MySQL, Isolation Forest ML, and Power BI
# Healthcare Claims Anomaly Detection Pipeline
## Overview
End-to-end fraud detection pipeline built on 642K+ CMS Medicare synthetic claims records. Detects suspicious billing patterns using machine learning and visualizes results in Power BI.

## Key Results
- 58,066 inpatient claims analyzed
- 2,900+ HIGH-risk claims flagged
- $791M in potentially anomalous billing identified
- 19.68 average suspicion score across flagged claims

## Tech Stack
- **Python** — ETL pipeline, feature engineering, ML model
- **MySQL** — Data warehouse with 4 tables and 3 SQL views
- **Scikit-learn** — Isolation Forest anomaly detection
- **Power BI** — Interactive compliance dashboard
- **SQLAlchemy/PyMySQL** — Database connectivity

## Project Structure
healthcare-claims-anomaly/
├── etl/
│   ├── load_data.py      # Extract & load CMS data into MySQL
│   └── transform.py      # Feature engineering
├── models/
│   └── anomaly_model.py  # Isolation Forest ML model
├── dashboard/            # Power BI dashboard
└── docs/                 # Architecture diagram & findings

## How It Works
1. **Extract** — Load CMS synthetic Medicare claims CSV files
2. **Transform** — Engineer 7 anomaly detection features per claim
3. **Model** — Train Isolation Forest (contamination=5%)
4. **Score** — Assign 0-100 suspicion score + HIGH/MEDIUM/LOW tier
5. **Visualize** — Power BI dashboard with KPIs, provider analysis, flagged claims table

## Data Source
[CMS Synthetic Medicare Claims](https://data.cms.gov/collection/synthetic-medicare-enrollment-fee-for-service-claims-and-prescription-drug-event) — publicly available, HIPAA-safe synthetic dataset

## Author
Pravallika Mettukuru | Healthcare Data Analyst
