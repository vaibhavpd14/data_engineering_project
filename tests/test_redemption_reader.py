from src.ingestion.file_discovery import discover_files
from src.ingestion.redemption_reader import read_redemption_file


def test_redemption_reader():

    _, redemption_files = discover_files()

    for file in redemption_files:

        print(f"\nReading: {file.name}")

        df = read_redemption_file(file)

        print("\nFlattened redemption data:")
        print(df)

        print("\nTotal transactions:", len(df))


if __name__ == "__main__":
    test_redemption_reader()
    