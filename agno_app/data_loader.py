import os
import kagglehub
import pandas as pd

def load_raw_marketing_data() -> pd.DataFrame:

    DATA_PATH = kagglehub.dataset_download("imakash3011/customer-personality-analysis")

    # Adjust filename if needed based on actual listing above
    csv_path = os.path.join(DATA_PATH, "marketing_campaign.csv")

    df = pd.read_csv(csv_path, sep="\t", encoding="utf-8")

    return df

'''
This block ensures that
- When imported: this part doesn’t run
- When executed from terminal: this part runs
'''
if __name__ == "__main__":
    df = load_raw_marketing_data()
    print(df.info())
    print(df.head())

 

    '''
    # Parse Dt_Customer to datetime (dataset uses day-first formats)
    df["Dt_Customer"] = pd.to_datetime(
        df["Dt_Customer"],
        dayfirst=True,
        errors="coerce",
    )

    return df
    '''