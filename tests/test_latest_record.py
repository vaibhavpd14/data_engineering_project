import pandas as pd

from src.transformation.country_routing import (
    keep_latest_member_record
)


def test_latest_record():

    data = {
        "MEMBER_ID": ["223457", "223457", "223458"],
        "MEMBER_NAME": ["Elena", "Elena", "Ravi"],
        "COUNTRY": ["IND", "USA", "IND"],
        "UPDATED_AT": [
            "2026-10-10",
            "2026-11-15",
            "2026-10-20"
        ]
    }

    df = pd.DataFrame(data)

    latest_df = keep_latest_member_record(df)

    print("\nLatest member records:")
    print(latest_df)


if __name__ == "__main__":
    test_latest_record()