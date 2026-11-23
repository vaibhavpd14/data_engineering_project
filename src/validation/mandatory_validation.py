MANDATORY_COLUMNS = [
    "MEMBER_NAME",
    "MEMBER_ID",
    "ENROLLMENT_DATE"
]


def validate_mandatory_fields(df):

    df = df.copy()

    # Identify records with missing mandatory values
    invalid_mask = (
        df[MANDATORY_COLUMNS]
        .apply(lambda column: column.astype(str).str.strip().eq(""))
        .any(axis=1)
    )

    # Separate valid and rejected records
    valid_df = df.loc[~invalid_mask].copy()
    rejected_df = df.loc[invalid_mask].copy()

    return valid_df, rejected_df