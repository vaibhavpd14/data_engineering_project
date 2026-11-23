from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.ingestion.redemption_reader import read_redemption_file

from src.standardization.standardize import standardize_columns
from src.transformation.country_routing import join_redemptions_with_members


def test_redemption_join():

    profile_files, redemption_files = discover_files()

    member_df = standardize_columns(
        read_profile_file(profile_files[0])
    )

    redemption_df = read_redemption_file(redemption_files[0])

    result_df = join_redemptions_with_members(
        member_df,
        redemption_df
    )

    print("\nJoined data:")
    print(
        result_df[
            [
                "MEMBER_ID",
                "MEMBER_NAME",
                "COUNTRY",
                "TXN_ID",
                "MILES_REDEEMED",
                "_merge"
            ]
        ]
    )

    print("\nJoin summary:")
    print(result_df["_merge"].value_counts())


if __name__ == "__main__":
    test_redemption_join()