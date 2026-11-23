KEY_COLUMN = "MEMBER_ID"


def validate_duplicates(df):

    df = df.copy()

    # Identify all occurrences of duplicate member names
    duplicate_mask = df.duplicated(
        subset=[KEY_COLUMN],
        keep=False
    )

    # Separate duplicate and unique records
    duplicate_df = df.loc[duplicate_mask].copy()

    unique_df = df.loc[~duplicate_mask].copy()

    return unique_df, duplicate_df

def validate_redemption_duplicates(df):

    df = df.copy()

    duplicate_mask = df.duplicated(
        subset=["TXN_ID"],
        keep=False
    )

    unique_df = df.loc[~duplicate_mask].copy()
    duplicate_df = df.loc[duplicate_mask].copy()

    return unique_df, duplicate_df