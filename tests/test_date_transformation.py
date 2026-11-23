from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns
from src.validation.data_quality import validate_date_fields
from src.transformation.date_transformation import transform_date_fields


def test_date_transformation():

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

        print("\nTransformed dates:")
        print(
            transformed_df[
                ["MEMBER_NAME", "ENROLLMENT_DATE",
                 "LAST_FLIGHT_DATE", "DOB"]
            ].head()
        )

        print("\nData types:")
        print(transformed_df[
            ["ENROLLMENT_DATE", "LAST_FLIGHT_DATE", "DOB"]
        ].dtypes)


if __name__ == "__main__":
    test_date_transformation()