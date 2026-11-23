from datetime import date
import pandas as pd

def calculate_age(dob, as_of_date):
    if dob is None:
        return None

    age = as_of_date.year - dob.year

    # Check whether the birthday has occurred this year
    if (as_of_date.month, as_of_date.day) < (dob.month, dob.day):
        age -= 1

    return age


def calculate_stale_member(last_flight_date, as_of_date):
    if last_flight_date is None:
        return None

    days_since_flight = (as_of_date - last_flight_date).days

    if days_since_flight > 90:
        return "Y"

    return "N"


def add_derived_columns(df, as_of_date=None):
    df = df.copy()

    if as_of_date is None:
        as_of_date = date.today()

    df["AGE"] = pd.array(df["DOB"].apply(lambda dob: calculate_age(dob, as_of_date)),dtype="Int64"
    )

    df["STALE_MEMBER"] = df["LAST_FLIGHT_DATE"].apply(
        lambda flight_date: calculate_stale_member(
            flight_date, as_of_date
        )
    )

    return df