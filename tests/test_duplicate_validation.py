from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns
from src.validation.duplicate_validation import validate_duplicates


def test_duplicate_validation():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)

        standardized_df = standardize_columns(df)

        unique_df, duplicate_df = validate_duplicates(
            standardized_df
        )

        print("\nTotal records:", len(df))
        print("Unique records:", len(unique_df))
        print("Duplicate records:", len(duplicate_df))

        print("\nDuplicate records:")
        print(duplicate_df[["MEMBER_NAME", "MEMBER_ID"]])


if __name__ == "__main__":
    test_duplicate_validation()