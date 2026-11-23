import pandas as pd

def split_by_country(df):
    country_data = {}

    for country in df["COUNTRY"].dropna().unique():

        country_df = df[
            df["COUNTRY"] == country
        ].copy()

        country_data[country] = country_df
    return country_data

def keep_latest_member_record(df):
    if "UPDATED_AT" not in df.columns:
        raise ValueError("UPDATED_AT column is required")

    df = df.copy()

    df["UPDATED_AT"] = pd.to_datetime(
        df["UPDATED_AT"]
    )

    df = df.sort_values("UPDATED_AT")

    latest_df = df.drop_duplicates(
        subset=["MEMBER_ID"],
        keep="last"
    )

    return latest_df

    
def join_redemptions_with_members(
    member_df,
    redemption_df
):
    result_df = redemption_df.merge(
        member_df,
        on="MEMBER_ID",
        how="left",
        suffixes=("_REDEMPTION", "_MEMBER"),
        indicator=True
    )

    return result_df