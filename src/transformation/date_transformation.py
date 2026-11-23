from datetime import datetime
import pandas as pd

DATE_FORMATS = {
    "ENROLLMENT_DATE": ["%Y%m%d"],
    "LAST_FLIGHT_DATE": ["%Y%m%d"],
    "DOB": ["%d%m%Y", "%Y%m%d"]
}


def transform_date_fields(df):
    df = df.copy()

    for column, formats in DATE_FORMATS.items():

        def convert_date(value):

            value = str(value).strip()

            if value == "" or value.lower() == "nan":
                return None

            for date_format in formats:
                try:
                    return datetime.strptime(
                        value, date_format
                    ).date()

                except ValueError:
                    continue

            raise ValueError(
                f"Invalid date in {column}: {value}"
            )

        df[column] = df[column].apply(convert_date)

    return df
def transform_redemption_dates(df):
    df = df.copy()

    date_columns = {
        "FEED_DATE": "%Y%m%d",
        "TXN_DATE": "%Y%m%d"
    }

    for column, date_format in date_columns.items():

        df[column] = df[column].apply(
            lambda value: (
                datetime.strptime(str(value), date_format).date()
                if pd.notna(value) and str(value).strip() != ""
                else None
            )
        )

    return df