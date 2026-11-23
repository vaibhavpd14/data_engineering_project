from pathlib import Path


def discover_files(raw_folder="data/raw"):

    raw_path = Path(raw_folder)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Source folder not found: {raw_path}"
        )

    profile_files = []
    redemption_files = []

    for file_path in raw_path.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() in [".txt", ".dat", ".psv"]:
            profile_files.append(file_path)

        elif file_path.suffix.lower() == ".json":
            redemption_files.append(file_path)

    return profile_files, redemption_files