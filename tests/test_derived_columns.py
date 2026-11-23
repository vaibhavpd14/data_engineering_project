from datetime import date

from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns
from src.validation.data_quality import validate_date_fields
from src.transformation.date_transformation import transform_date_fields
from src.transformation.derived_columns import add_derived_columns


def test_derived_columns():

    profile_files, _ = discover_files()

    for file in profile_files:

        df = read_profile_file(file)
        df = standardize_columns(df)

        date_issues = validate_date_fields(df)

        invalid_indexes = {
            issue["ROW_INDEX"] for issue in date_issues
        }

        valid_df = df.drop(index=invalid_indexes).copy()

        transformed_df = transform_date_fields(valid_df)

        final_df = add_derived_columns(
            transformed_df,
            as_of_date=date(2026, 11, 22)
        )

        print("\nDerived columns:")
        print(
            final_df[
                [
                    "MEMBER_NAME",
                    "DOB",
                    "AGE",
                    "LAST_FLIGHT_DATE",
                    "STALE_MEMBER"
                ]
            ]
        )

# Unit Test 1: Age calculation
def test_calculate_age():
    from src.transformation.derived_columns import calculate_age

    dob = date(2000, 11, 21)
    as_of_date = date(2026, 11, 22)

    assert calculate_age(dob, as_of_date) == 26


# Unit Test 2: Birthday has not occurred
def test_calculate_age_before_birthday():
    from src.transformation.derived_columns import calculate_age

    dob = date(2000, 11, 23)
    as_of_date = date(2026, 11, 22)

    assert calculate_age(dob, as_of_date) == 25


# Unit Test 3: More than 90 days
def test_stale_member():
    from src.transformation.derived_columns import calculate_stale_member

    last_flight = date(2026, 8, 23)
    as_of_date = date(2026, 11, 22)

    assert calculate_stale_member(last_flight, as_of_date) == "Y"


# Unit Test 4: Exactly 90 days
def test_not_stale_at_90_days():
    from src.transformation.derived_columns import calculate_stale_member

    last_flight = date(2026, 8, 24)
    as_of_date = date(2026, 11, 22)

    assert calculate_stale_member(last_flight, as_of_date) == "N"


# Unit Test 5: Missing flight date
def test_missing_last_flight():
    from src.transformation.derived_columns import calculate_stale_member

    assert calculate_stale_member(
        None,
        date(2026, 11, 22)
    ) is None

    
if __name__ == "__main__":
    test_derived_columns()