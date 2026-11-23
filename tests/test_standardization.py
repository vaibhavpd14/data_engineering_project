from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns


def test_standardization():

    profile_files, _ = discover_files()

    for file in profile_files:

        print(f"\nProcessing: {file.name}")

        df = read_profile_file(file)

        standardized_df = standardize_columns(df)

        print("\nStandardized columns:")
        print(standardized_df.columns.tolist())

        print("\nStandardized data:")
        print(standardized_df.head())


if __name__ == "__main__":
    test_standardization()