from src.ingestion.file_discovery import discover_files


def test_discover_files():

    profile_files, redemption_files = discover_files()

    print("Profile files:")

    for file in profile_files:
        print(file.name)

    print("\nRedemption files:")

    for file in redemption_files:
        print(file.name)


if __name__ == "__main__":
    test_discover_files()