from datetime import datetime
import pandas as pd

FIELD_LENGTHS = {
    "MEMBER_NAME": 255,
    "MEMBER_ID": 18,
    "TIER_CODE": 5,
    "AGENT_NAME": 255,
    "STATE": 5,
    "COUNTRY": 5,
    "IS_ACTIVE": 1
}


def validate_field_lengths(df):

    df = df.copy()

    issues = []

    for column, max_length in FIELD_LENGTHS.items():

        invalid_mask = (
            df[column]
            .fillna("")
            .astype(str)
            .str.len() > max_length
        )

        for index in df[invalid_mask].index:

            issues.append({
                "ROW_INDEX": index,
                "COLUMN": column,
                "VALUE": df.loc[index, column],
                "ERROR": f"Exceeds maximum length of {max_length}"
            })
    return issues
from datetime import datetime

DATE_FORMATS = {
    "ENROLLMENT_DATE": ["%Y%m%d"],
    "LAST_FLIGHT_DATE": ["%Y%m%d"],
    "DOB": ["%d%m%Y", "%Y%m%d"]
}


def validate_date_fields(df):
    issues = []

    for column, formats in DATE_FORMATS.items():

        for index, value in df[column].items():

            value = str(value).strip()

            if value == "" or value.lower() == "nan":
                continue

            is_valid = False

            for date_format in formats:
                try:
                    datetime.strptime(value, date_format)
                    is_valid = True
                    break

                except ValueError:
                    continue

            if not is_valid:
                issues.append({
                    "ROW_INDEX": index,
                    "COLUMN": column,
                    "VALUE": value,
                    "ERROR": f"Invalid date. Expected one of {formats}"
                })

    return issues

REDEMPTION_MANDATORY_COLUMNS = [
    "MEMBER_ID",
    "TXN_ID",
    "TXN_DATE",
    "MILES_REDEEMED"
]


def validate_redemption_mandatory(df):
    df = df.copy()

    invalid_mask = (
        df[REDEMPTION_MANDATORY_COLUMNS]
        .apply(
            lambda column:
            column.isna()
            | column.astype(str).str.strip().eq("")
        )
        .any(axis=1)
    )

    valid_df = df.loc[~invalid_mask].copy()
    rejected_df = df.loc[invalid_mask].copy()

    return valid_df, rejected_df


def validate_miles_redeemed(df):

    df = df.copy()

    df["MILES_REDEEMED"] = pd.to_numeric(
        df["MILES_REDEEMED"],
        errors="coerce"
    )

    invalid_mask = (
        df["MILES_REDEEMED"].isna()
        | (df["MILES_REDEEMED"] < 0)
    )

    valid_df = df.loc[~invalid_mask].copy()
    rejected_df = df.loc[invalid_mask].copy()

    return valid_df, rejected_df