import os
import kagglehub
import pandas as pd
from typing import List
import numpy as np

def load_raw_marketing_data() -> pd.DataFrame:

    DATA_PATH = kagglehub.dataset_download("imakash3011/customer-personality-analysis")

    # Adjust filename if needed based on actual listing above
    csv_path = os.path.join(DATA_PATH, "marketing_campaign.csv")

    df = pd.read_csv(csv_path, sep="\t", encoding="utf-8")

    return df


def clean_data() -> pd.DataFrame:

    df = load_raw_marketing_data()

    # 1. Clean 'Marital_Status' column
    marital_map = {
        "Married": "Married",
        "Together": "Together",
        "Single": "Single",
        "Divorced": "Divorced",
        "Widow": "Widow",
        "Alone": "Single",   # Usually means living alone
        "Absurd": "Other",
        "YOLO": "Other"
    }
    df["Marital_Status"] = df["Marital_Status"].map(marital_map)

    # lowering the "Marital_Status" column values for comparison later on
    df["Marital_Status"] = df["Marital_Status"].str.strip().str.lower()

    # 2. Clean 'Education' column
    edu_map = {
        "Graduation": "Graduate",
        "PhD": "PhD",
        "Master": "Master",
        "2n Cycle": "Undergraduate",
        "Basic": "Basic"
    }
    df["Education"] = df["Education"].map(edu_map)

    # lowering the "Education" column values for comparison later on
    df["Education"] = df["Education"].str.strip().str.lower()

    # 3. Dropping constant columns
    df.drop(columns=["Z_CostContact", "Z_Revenue"], inplace=True)

    # 4. Capiing outliers
    cols = ["NumWebPurchases", "NumCatalogPurchases"]
    for col in cols:
        df[col] = df[col].clip(upper=round(df[col].quantile(0.99)))

    # 5. Handling missing values in 'Income' by median imputation
    df["Income"] = df["Income"].fillna(df["Income"].median())

    # 6. Parsing 'Dt_Customer' to datetime (dataset uses day-first formats)
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%d-%m-%Y")

    return df

def feature_engineering() -> pd.DataFrame:

    df = clean_data()

    # 1. Creating 'Total_Purchases' feature
    purchase_cols = [
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases",
        "NumWebVisitsMonth"
    ]
    df["Total_Purchases"] = df[purchase_cols].sum(axis=1)

    # 2. Creating 'Total_Children' feature
    df["Total_Children"] = df["Kidhome"] + df["Teenhome"]

    # 3. Creating 'Customer_Tenure' feature

    # CustomerTenureDays = latest Dt_Customer - Dt_Customer
    if df["Dt_Customer"].notna().any():
        ref_date = df["Dt_Customer"].max()
        df["CustomerTenureDays"] = (ref_date - df["Dt_Customer"]).dt.days
    else:
        df["CustomerTenureDays"] = np.nan

    # 4. Creating 'TotalSpend' feature

    # TotalSpend = sum of all product spends
    SPEND_COLUMNS: List[str] = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
    ]

    df["TotalSpend"] = df[SPEND_COLUMNS].sum(axis=1)

    # 5. Creating 'IsHighValue' feature

    # IsHighValue = top 20% by TotalSpend
    high_value_threshold = df["TotalSpend"].quantile(0.80)
    df["IsHighValue"] = df["TotalSpend"] >= high_value_threshold

    return df

def get_final_dataset() -> pd.DataFrame:
    return feature_engineering()

if __name__ == "__main__":

    print("Loading raw data...")
    df = load_raw_marketing_data()
    print(df.head())
    print(df.shape)

    print("\nCleaning data...")
    cleaned_df = clean_data()
    print(cleaned_df.head())
    print(cleaned_df.shape)

    print("\nPerforming feature engineering...")
    fe_df = feature_engineering()
    print(fe_df.head())
    print(fe_df.shape)
    print()

