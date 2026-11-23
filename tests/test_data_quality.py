from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns

from src.validation.data_quality import (
    validate_field_lengths,
    validate_date_fields
)


def test_data_quality():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)
        standardized_df = standardize_columns(df)

        length_issues = validate_field_lengths(standardized_df)
        date_issues = validate_date_fields(standardized_df)

        print("\nField length issues:", len(length_issues))
        print("Date validation issues:", len(date_issues))

        print("\nDate issues:")

        for issue in date_issues:
            print(issue)


if __name__ == "__main__":
    test_data_quality()