# from src.ingestion.file_discovery import discover_files
# from src.ingestion.redemption_reader import read_redemption_file

# from src.validation.data_quality import (
#     validate_redemption_mandatory,
#     validate_miles_redeemed
# )

# from src.validation.duplicate_validation import (
#     validate_redemption_duplicates
# )


# def test_redemption_validation():

#     _, redemption_files = discover_files()

#     for file in redemption_files:

#         df = read_redemption_file(file)

#         valid_df, rejected_df = validate_redemption_mandatory(df)

#         print("\nMandatory validation")
#         print("Valid:", len(valid_df))
#         print("Rejected:", len(rejected_df))

#         unique_df, duplicate_df = validate_redemption_duplicates(
#             valid_df
#         )

#         print("\nDuplicate validation")
#         print("Unique:", len(unique_df))
#         print("Duplicates:", len(duplicate_df))

#         valid_miles_df, invalid_miles_df = validate_miles_redeemed(
#             unique_df
#         )

#         print("\nMiles validation")
#         print("Valid:", len(valid_miles_df))
#         print("Invalid:", len(invalid_miles_df))


# if __name__ == "__main__":
#     test_redemption_validation()

from src.ingestion.file_discovery import discover_files
from src.ingestion.redemption_reader import read_redemption_file

from src.validation.redemption_validation import (
    validate_redemption_data
)


def test_redemption_validation():

    _, redemption_files = discover_files()

    for file in redemption_files:

        df = read_redemption_file(file)

        accepted_df, rejected_df = validate_redemption_data(df)

        print("\nRedemption Validation Summary")
        print("--------------------------------")

        print("Total records:", len(df))
        print("Accepted records:", len(accepted_df))
        print("Rejected records:", len(rejected_df))

        print("\nAccepted Records:")
        print(accepted_df)

        print("\nRejected Records:")
        print(rejected_df)


if __name__ == "__main__":
    test_redemption_validation()