from src.ingestion.file_discovery import discover_files
from src.ingestion.file_reader import read_profile_file


def test_file_reader():

    profile_files, redemption_files = discover_files()

    for file in profile_files:

        print(f"\nReading: {file.name}")

        df = read_profile_file(file)

        #print(df.head())
        #print(df.info())


if __name__ == "__main__":
    test_file_reader()