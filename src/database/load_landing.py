from src.database.snowflake_connection import get_snowflake_connection
from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file
from src.standardization.standardize import standardize_columns


def load_member_profiles():

    profile_files, _ = discover_files()

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:

        for file in profile_files:

            print(f"Processing file: {file.name}")

            df = read_profile_file(file)
            df = standardize_columns(df)

            insert_query = """
                INSERT INTO SKYPOINTS_DB.LANDING.MEMBER_PROFILE_RAW (
                    MEMBER_NAME,
                    MEMBER_ID,
                    ENROLLMENT_DATE,
                    LAST_FLIGHT_DATE,
                    TIER_CODE,
                    AGENT_NAME,
                    STATE,
                    COUNTRY,
                    DOB,
                    IS_ACTIVE,
                    SOURCE_FILE_NAME
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            records = [
                tuple(row) + (file.name,)
                for row in df.itertuples(index=False, name=None)
            ]

            cursor.executemany(insert_query, records)

            print(f"Loaded {len(records)} member records")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_member_profiles()