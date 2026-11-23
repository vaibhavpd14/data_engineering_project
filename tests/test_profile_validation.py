import pandas as pd

from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file

from src.standardization.standardize import standardize_columns

from src.validation.profile_validation import (
    validate_member_profile
)


def test_profile_validation():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)

        df = standardize_columns(df)

        accepted_df, rejected_df = validate_member_profile(df)

        print("\nValidation Summary")
        print("------------------")

        print("Total records:", len(df))
        print("Accepted records:", len(accepted_df))
        print("Rejected records:", len(rejected_df))

        print("\nAccepted Records:")
        print(accepted_df[["MEMBER_NAME", "MEMBER_ID", "COUNTRY"]])

        print("\nRejected Records:")
        print(
            rejected_df[
                ["MEMBER_NAME", "MEMBER_ID", "COUNTRY",
                 "REJECTION_REASON"]
            ]
        )



# from src.validation.profile_validation import validate_member_profile


def get_sample_data():
    return pd.DataFrame({
        "MEMBER_NAME": [
            "Elena",
            "Ravi",
            "",
            "Jacob",
            "Mia",
            "Nora"
        ],
        "MEMBER_ID": [
            "1001",
            "1002",
            "1003",
            "1004",
            "1005",
            "1006"
        ],
        "ENROLLMENT_DATE": [
            "20200101",
            "20210101",
            "20220101",
            "",
            "20230101",
            "20240101"
        ],
        "LAST_FLIGHT_DATE": [
            "20261115",
            "20260101",
            "20260101",
            "20260101",
            "20260101",
            "20260101"
        ],
        "TIER_CODE": [
            "GLD",
            "SLV",
            "GLD",
            "SLV",
            "TOOLONG",
            "PLT"
        ],
        "AGENT_NAME": [
            "Sam",
            "Alex",
            "Sam",
            "Sam",
            "Sam",
            "Sam"
        ],
        "STATE": [
            "CA",
            "TN",
            "CA",
            "VIC",
            "CA",
            "ONT"
        ],
        "COUNTRY": [
            "USA",
            "IND",
            "USA",
            "AU",
            "USA",
            "CAN"
        ],
        "DOB": [
            "03051985",
            "15081990",
            "01011990",
            "31121980",
            "01011995",
            "01011995"
        ],
        "IS_ACTIVE": [
            "A",
            "A",
            "A",
            "A",
            "A",
            "A"
        ]
    })


# Test 1: Valid records should be accepted
def test_valid_records():
    df = get_sample_data()

    accepted_df, rejected_df = validate_member_profile(df)

    assert len(accepted_df) == 3
    assert len(rejected_df) == 3

    assert list(accepted_df.index) == [0, 1, 5]
    assert list(rejected_df.index) == [2, 3, 4]


# Test 2: Missing mandatory fields
def test_missing_mandatory_fields():
    df = get_sample_data()

    accepted_df, rejected_df = validate_member_profile(df)

    assert 2 in rejected_df.index
    assert "Missing mandatory field" in rejected_df.loc[2, "REJECTION_REASON"]


# Test 3: Duplicate member ID
def test_duplicate_member_id():
    df = get_sample_data()

    df.loc[1, "MEMBER_ID"] = "1001"

    accepted_df, rejected_df = validate_member_profile(df)

    assert 0 in rejected_df.index
    assert 1 in rejected_df.index


# Test 4: Invalid field length
def test_invalid_field_length():
    df = get_sample_data()

    accepted_df, rejected_df = validate_member_profile(df)

    assert 4 in rejected_df.index
    assert "TIER_CODE" in rejected_df.loc[4, "REJECTION_REASON"]


# Test 5: Invalid date
def test_invalid_date():
    df = get_sample_data()

    df.loc[5, "ENROLLMENT_DATE"] = "20261340"

    accepted_df, rejected_df = validate_member_profile(df)

    assert 5 in rejected_df.index
    assert "ENROLLMENT_DATE" in rejected_df.loc[5, "REJECTION_REASON"]

if __name__ == "__main__":
    test_profile_validation()