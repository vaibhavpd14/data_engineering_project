import pandas as pd


COLUMN_MAPPING = {
    "Member_Name": "MEMBER_NAME",
    "Member_Id": "MEMBER_ID",
    "Enrollment_Date": "ENROLLMENT_DATE",
    "Last_Flight_Date": "LAST_FLIGHT_DATE",
    "Tier_Code": "TIER_CODE",
    "Agent_Name": "AGENT_NAME",
    "State": "STATE",
    "Country": "COUNTRY",
    "DOB": "DOB",
    "Is_Active": "IS_ACTIVE"
}


EXPECTED_COLUMNS = list(COLUMN_MAPPING.values())


def standardize_columns(df):

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Remove leading and trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Rename source columns into standard column names
    df = df.rename(columns=COLUMN_MAPPING)

    # Check whether expected columns are available
    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}"
        )

    # Keep columns in a consistent order
    df = df[EXPECTED_COLUMNS]

    return df