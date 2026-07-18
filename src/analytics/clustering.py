import os
import sqlite3
import warnings

import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "db",
    "nifty100.db"
)

SECTOR_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "supplementry",
    "sectors.xlsx"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "output"
)

REPORT_DIR = os.path.join(
    PROJECT_ROOT,
    "reports"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ==========================================================
# LOAD DATABASE
# ==========================================================

print("=" * 60)
print("Loading Data...")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

companies_df = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print(f"Companies Loaded        : {len(companies_df)}")
print(f"Financial Ratios Loaded : {len(ratios_df)}")

# ==========================================================
# LOAD SECTOR INFORMATION
# ==========================================================

sectors_df = pd.read_excel(SECTOR_FILE)

print(f"Sectors Loaded          : {len(sectors_df)}")

# ==========================================================
# KEEP ONLY LATEST ANNUAL RECORD
# ==========================================================

annual_ratios = ratios_df[
    ~ratios_df["year"]
    .astype(str)
    .str.upper()
    .eq("TTM")
].copy()

annual_ratios["year_num"] = (
    annual_ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(float)
)

latest_ratios = (
    annual_ratios
    .sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

print(f"Latest Annual Records   : {len(latest_ratios)}")

# ==========================================================
# MERGE DATASETS
# ==========================================================

cluster_df = (
    companies_df
    .merge(
        sectors_df[
            [
                "company_id",
                "broad_sector",
                "sub_sector",
                "market_cap_category"
            ]
        ],
        left_on="id",
        right_on="company_id",
        how="left"
    )
    .merge(
        latest_ratios,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("_company", "")
    )
)

cluster_df = cluster_df.loc[
    :,
    ~cluster_df.columns.duplicated()
]

print("\nMerged Dataset Shape :", cluster_df.shape)

# ==========================================================
# FEATURES FOR CLUSTERING
# ==========================================================

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct"
]

required_columns = [
    "company_id",
    "company_name",
    "broad_sector"
] + FEATURES

data = cluster_df[required_columns].copy()

# ==========================================================
# MISSING VALUE REPORT
# ==========================================================

print("\nMissing Values Before Imputation")
print("-" * 45)

print(data[FEATURES].isna().sum())

# ==========================================================
# SECTOR MEDIAN IMPUTATION
# ==========================================================

for feature in FEATURES:

    data[feature] = (
        data
        .groupby("broad_sector")[feature]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )

# Overall Median Backup

for feature in FEATURES:

    data[feature] = data[feature].fillna(
        data[feature].median()
    )

print("\nMissing Values After Imputation")
print("-" * 45)

print(data[FEATURES].isna().sum())

print("\nData Ready For Clustering")

print(f"Rows    : {len(data)}")
print(f"Columns : {len(data.columns)}")

print("\nPreview")

print(data.head())


# ==========================================================
# IMPORTS FOR CLUSTERING
# ==========================================================

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# ==========================================================
# STANDARDIZE FEATURES
# ==========================================================

print("\n" + "=" * 60)
print("Standardizing Features")
print("=" * 60)

X = data[FEATURES].copy()

# ==========================================================
# OUTLIER TREATMENT (IQR CLIPPING)
# ==========================================================

print("\nRemoving Extreme Outliers...")

for feature in FEATURES:

    Q1 = data[feature].quantile(0.25)
    Q3 = data[feature].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    data[feature] = data[feature].clip(lower, upper)

print("Outlier Treatment Completed")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Scaling Completed Successfully")
print("Feature Matrix Shape :", X_scaled.shape)

# ==========================================================
# ELBOW METHOD
# ==========================================================

print("\nGenerating Elbow Plot...")

inertia = []

K = range(1, 11)

for k in K:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertia.append(model.inertia_)

plt.figure(figsize=(8, 5))

plt.plot(
    K,
    inertia,
    marker="o",
    linewidth=2
)

plt.title("Elbow Method for Optimal K")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.xticks(K)

plt.grid(True)

elbow_path = os.path.join(
    REPORT_DIR,
    "elbow_plot.png"
)

plt.savefig(
    elbow_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Elbow Plot Saved :", elbow_path)

# ==========================================================
# FINAL KMEANS MODEL
# ==========================================================

print("\nRunning KMeans Clustering...")

NUM_CLUSTERS = 5

kmeans = KMeans(
    n_clusters=NUM_CLUSTERS,
    random_state=42,
    n_init=10
)

cluster_labels = kmeans.fit_predict(X_scaled)

data["cluster"] = cluster_labels

# ==========================================================
# DISTANCE TO CLUSTER CENTROID
# ==========================================================

distances = kmeans.transform(X_scaled)

data["distance_to_centroid"] = [

    distances[i][cluster]

    for i, cluster in enumerate(cluster_labels)

]

# ==========================================================
# CLUSTER SIZE SUMMARY
# ==========================================================

print("\nCluster Distribution")
print("-" * 40)

cluster_summary = (
    data["cluster"]
    .value_counts()
    .sort_index()
)

print(cluster_summary)

# ==========================================================
# CLUSTER PROFILE
# ==========================================================

print("\nCluster Statistics")
print("-" * 40)

cluster_profile = (

    data
    .groupby("cluster")[FEATURES]
    .mean()
    .round(2)

)

print(cluster_profile)

# ==========================================================
# SAVE CLUSTER LABELS
# ==========================================================

cluster_csv = os.path.join(
    OUTPUT_DIR,
    "cluster_labels.csv"
)

data.to_csv(
    cluster_csv,
    index=False
)

print("\nCluster Labels Saved")

print(cluster_csv)

# ==========================================================
# SAVE CLUSTER PROFILE
# ==========================================================

profile_csv = os.path.join(
    OUTPUT_DIR,
    "cluster_profile.csv"
)

cluster_profile.to_csv(
    profile_csv
)

print("Cluster Profile Saved")

print(profile_csv)

# ==========================================================
# TOP COMPANIES FROM EACH CLUSTER
# ==========================================================

print("\nSample Companies by Cluster")
print("-" * 60)

for cluster in sorted(data["cluster"].unique()):

    print(f"\nCluster {cluster}")

    companies = (

        data[data["cluster"] == cluster]

        .sort_values(
            "distance_to_centroid"
        )

        .head(5)

    )

    print(

        companies[
            [
                "company_name",
                "broad_sector",
                "distance_to_centroid"
            ]
        ]

    )

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("DAY 36 COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Companies Clustered : {len(data)}")

print(f"Number of Clusters  : {NUM_CLUSTERS}")

print(f"Cluster CSV         : {cluster_csv}")

print(f"Cluster Profile     : {profile_csv}")

print(f"Elbow Plot          : {elbow_path}")

print("=" * 60)