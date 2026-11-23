from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns
from src.validation.mandatory_validation import validate_mandatory_fields


def test_mandatory_validation():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)

        standardized_df = standardize_columns(df)

        valid_df, rejected_df = validate_mandatory_fields(
            standardized_df
        )

        print("\nTotal records:", len(df))
        print("Valid records:", len(valid_df))
        print("Rejected records:", len(rejected_df))

        print("\nRejected records:")
        print(rejected_df)


if __name__ == "__main__":
    test_mandatory_validation()