import json

from src.database.snowflake_connection import get_snowflake_connection
from src.ingestion.file_discovery import discover_files


def load_redemptions():

    _, redemption_files = discover_files()

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:

        insert_query = """
            INSERT INTO SKYPOINTS_DB.LANDING.REDEMPTION_RAW (
                RAW_DATA,
                SOURCE_FILE_NAME
            )
            SELECT PARSE_JSON(%s), %s
        """

        for file in redemption_files:

            print(f"Processing file: {file.name}")

            with open(file, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

            # Support both a single JSON object and a list of objects
            if isinstance(data, dict):
                data = [data]

            for record in data:

                json_string = json.dumps(record)

                cursor.execute(
                    insert_query,
                    (json_string, file.name)
                )

            print(f"Loaded {len(data)} JSON documents")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_redemptions()