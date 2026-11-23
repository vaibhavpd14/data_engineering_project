from src.database.snowflake_connection import get_snowflake_connection


def test_connection():

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA()
        """)

        result = cursor.fetchone()

        print("Snowflake connection successful!")
        print("User:", result[0])
        print("Role:", result[1])
        print("Warehouse:", result[2])
        print("Database:", result[3])
        print("Schema:", result[4])

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    test_connection()