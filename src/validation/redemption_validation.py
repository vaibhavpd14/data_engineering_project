import pandas as pd
from datetime import datetime


MANDATORY_COLUMNS = [
    "MEMBER_ID",
    "TXN_ID",
    "TXN_DATE",
    "MILES_REDEEMED"
]


def validate_redemption_data(df):

    df = df.copy()

    rejection_reasons = {}

    # Helper function to collect rejection reasons
    def add_rejection(index, reason):
        rejection_reasons.setdefault(index, []).append(reason)

    # 1. Mandatory field validation
    for column in MANDATORY_COLUMNS:

        invalid_mask = (
            df[column].isna()
            | df[column].astype(str).str.strip().eq("")
        )

        for index in df[invalid_mask].index:
            add_rejection(index, f"Missing mandatory field: {column}")

    # 2. Duplicate transaction validation
    valid_txn_ids = df["TXN_ID"].notna() & (
        df["TXN_ID"].astype(str).str.strip() != ""
    )

    duplicate_mask = (
        df.loc[valid_txn_ids]
        .duplicated(subset=["TXN_ID"], keep=False)
    )

    duplicate_indexes = df.loc[valid_txn_ids].index[duplicate_mask]

    for index in duplicate_indexes:
        add_rejection(index, "Duplicate transaction ID")

    # 3. Mileage validation
    numeric_miles = pd.to_numeric(
        df["MILES_REDEEMED"],
        errors="coerce"
    )

    invalid_miles = numeric_miles.isna() | (numeric_miles < 0)

    for index in df[invalid_miles].index:
        add_rejection(index, "Invalid miles redeemed")

    # 4. Date validation
    date_columns = ["TXN_DATE", "FEED_DATE"]

    for column in date_columns:

        for index, value in df[column].items():

            if pd.isna(value) or str(value).strip() == "":
                if column == "TXN_DATE":
                    continue  # Already handled by mandatory validation
                continue

            try:
                datetime.strptime(str(value).strip(), "%Y%m%d")

            except ValueError:
                add_rejection(
                    index,
                    f"Invalid date in {column}"
                )

    # 5. Separate accepted and rejected records
    rejected_indexes = list(rejection_reasons.keys())

    accepted_df = df.drop(index=rejected_indexes).copy()

    rejected_df = df.loc[rejected_indexes].copy()

    rejected_df["REJECTION_REASON"] = [
        "; ".join(rejection_reasons[index])
        for index in rejected_df.index
    ]

    return accepted_df, rejected_df