import pandas as pd

from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.ingestion.redemption_reader import read_redemption_file

from src.standardization.standardize import standardize_columns

from src.validation.profile_validation import validate_member_profile
from src.validation.redemption_validation import validate_redemption_data

from src.transformation.date_transformation import (
    transform_date_fields,
    transform_redemption_dates
)

from src.transformation.derived_columns import add_derived_columns

from src.transformation.country_routing import (
    split_by_country,
    join_redemptions_with_members
)

from src.pipeline.output_writer import (
    save_country_data,
    save_rejected_data,
    save_redemption_data,
    save_joined_data
)


def run_pipeline():

    print("\n========== PIPELINE STARTED ==========\n")

    # STEP 1: Discover files
    profile_files, redemption_files = discover_files()

    print("Profile files found:", len(profile_files))
    print("Redemption files found:", len(redemption_files))

    # STEP 2: Process member profiles
    all_accepted_members = []
    all_rejected_members = []

    for file in profile_files:

        print(f"\nProcessing profile file: {file.name}")

        df = read_profile_file(file)
        df = standardize_columns(df)

        accepted_df, rejected_df = validate_member_profile(df)

        print("Accepted members:", len(accepted_df))
        print("Rejected members:", len(rejected_df))

        # Transform accepted records
        transformed_df = transform_date_fields(accepted_df)
        transformed_df = add_derived_columns(transformed_df)

        all_accepted_members.append(transformed_df)
        all_rejected_members.append(rejected_df)

    # STEP 3: Combine member records

    if all_accepted_members:
        member_df = pd.concat(
            all_accepted_members,
            ignore_index=True
        )
    else:
        member_df = pd.DataFrame()

    if all_rejected_members:
        rejected_members_df = pd.concat(
            all_rejected_members,
            ignore_index=True
        )
    else:
        rejected_members_df = pd.DataFrame()

    # Save rejected member records
    save_rejected_data(
        rejected_members_df,
        "rejected_members.csv"
    )

    # STEP 4: Country routing

    if not member_df.empty:

        country_data = split_by_country(member_df)

        print("\n========== COUNTRY SUMMARY ==========")

        for country, country_df in country_data.items():
            print(f"{country}: {len(country_df)} members")

        # Save country-specific member files
        save_country_data(country_data)

    # STEP 5: Process redemption JSON

    all_accepted_redemptions = []
    all_rejected_redemptions = []

    for file in redemption_files:

        print(f"\nProcessing redemption file: {file.name}")

        redemption_df = read_redemption_file(file)

        accepted_redemptions, rejected_redemptions = (
            validate_redemption_data(redemption_df)
        )

        print("Accepted transactions:", len(accepted_redemptions))
        print("Rejected transactions:", len(rejected_redemptions))

        # Transform accepted redemption records
        transformed_redemptions = transform_redemption_dates(
            accepted_redemptions
        )

        all_accepted_redemptions.append(transformed_redemptions)
        all_rejected_redemptions.append(rejected_redemptions)

    # STEP 6: Combine redemption records

    if all_accepted_redemptions:
        redemption_df = pd.concat(
            all_accepted_redemptions,
            ignore_index=True
        )
    else:
        redemption_df = pd.DataFrame()

    if all_rejected_redemptions:
        rejected_redemptions_df = pd.concat(
            all_rejected_redemptions,
            ignore_index=True
        )
    else:
        rejected_redemptions_df = pd.DataFrame()

    # Save accepted and rejected redemption records
    save_redemption_data(
        redemption_df,
        "accepted_redemptions.csv"
    )

    save_redemption_data(
        rejected_redemptions_df,
        "rejected_redemptions.csv"
    )

    # STEP 7: Join redemption with member profiles

    if not member_df.empty and not redemption_df.empty:

        joined_df = join_redemptions_with_members(
            member_df,
            redemption_df
        )

        print("\n========== REDEMPTION JOIN SUMMARY ==========")

        print(joined_df["_merge"].value_counts())

        # Save joined records
        save_joined_data(joined_df)

    else:
        print("\nNo records available for joining.")
    #return member_df, redemption_df

    print("\n========== PIPELINE COMPLETED ==========\n")


if __name__ == "__main__":
    run_pipeline()