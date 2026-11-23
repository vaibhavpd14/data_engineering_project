from src.ingestion.file_discovery import discover_files
from src.ingestion.redemption_reader import read_redemption_file
from src.transformation.date_transformation import transform_redemption_dates


def test_redemption_date_transformation():

    _, redemption_files = discover_files()

    for file in redemption_files:

        df = read_redemption_file(file)

        transformed_df = transform_redemption_dates(df)

        print("\nTransformed redemption dates:")
        print(
            transformed_df[
                ["MEMBER_ID", "FEED_DATE", "TXN_DATE"]
            ]
        )

        print("\nData types:")
        print(
            transformed_df[
                ["FEED_DATE", "TXN_DATE"]
            ].dtypes
        )


if __name__ == "__main__":
    test_redemption_date_transformation()