from src.validation.mandatory_validation import (
    validate_mandatory_fields
)

from src.validation.duplicate_validation import (
    validate_duplicates
)

from src.validation.data_quality import (
    validate_field_lengths,
    validate_date_fields
)


def validate_member_profile(df):

    df = df.copy()

    rejection_reasons = {}

    # 1. Mandatory field validation
    valid_df, mandatory_rejected = validate_mandatory_fields(df)

    for index in mandatory_rejected.index:
        rejection_reasons[index] = ["Missing mandatory field"]

    # 2. Duplicate validation
    unique_df, duplicate_df = validate_duplicates(valid_df)

    for index in duplicate_df.index:
        rejection_reasons.setdefault(index, []).append(
            "Duplicate member key"
        )

    # 3. Field-length validation
    length_issues = validate_field_lengths(unique_df)

    for issue in length_issues:
        index = issue["ROW_INDEX"]

        rejection_reasons.setdefault(index, []).append(
            f'{issue["COLUMN"]}: {issue["ERROR"]}'
        )

    # 4. Date validation
    date_issues = validate_date_fields(unique_df)

    for issue in date_issues:
        index = issue["ROW_INDEX"]

        rejection_reasons.setdefault(index, []).append(
            f'{issue["COLUMN"]}: {issue["ERROR"]}'
        )

    # Separate accepted and rejected records
    rejected_indexes = list(rejection_reasons.keys())

    accepted_df = df.drop(index=rejected_indexes).copy()

    rejected_df = df.loc[rejected_indexes].copy()

    rejected_df["REJECTION_REASON"] = [
        "; ".join(rejection_reasons[index])
        for index in rejected_df.index
    ]

    return accepted_df, rejected_df