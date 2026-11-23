from pathlib import Path

OUTPUT_DIR = Path("data/processed")


def save_country_data(country_data):

    output_folder = OUTPUT_DIR / "members"
    output_folder.mkdir(parents=True, exist_ok=True)

    for country, country_df in country_data.items():

        file_path = output_folder / f"{country.lower()}_members.csv"

        country_df.to_csv(file_path, index=False)

        print(f"Saved: {file_path}")


def save_rejected_data(df, file_name):

    output_folder = OUTPUT_DIR / "rejected"
    output_folder.mkdir(parents=True, exist_ok=True)

    file_path = output_folder / file_name

    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path}")


def save_redemption_data(df, file_name):

    output_folder = OUTPUT_DIR / "redemptions"
    output_folder.mkdir(parents=True, exist_ok=True)

    file_path = output_folder / file_name

    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path}")


def save_joined_data(df):

    output_folder = OUTPUT_DIR / "joined"
    output_folder.mkdir(parents=True, exist_ok=True)

    file_path = output_folder / "redemption_member_details.csv"

    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path}")