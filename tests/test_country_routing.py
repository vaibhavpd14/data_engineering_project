from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns
from src.transformation.country_routing import split_by_country


def test_country_routing():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)
        df = standardize_columns(df)

        country_data = split_by_country(df)

        for country, country_df in country_data.items():

            print(f"\nCountry: {country}")
            print(f"Total members: {len(country_df)}")

            print(
                country_df[
                    ["MEMBER_NAME", "MEMBER_ID", "COUNTRY"]
                ]
            )


if __name__ == "__main__":
    test_country_routing()