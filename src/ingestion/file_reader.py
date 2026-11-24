
import pandas as pd


def read_profile_file(file_path):

    columns = None
    records = []

    with open(file_path, "r", encoding="utf-8-sig") as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue
            # split input with delimeter |
            fields = line.split("|")

            # Remove only the leading empty field
            if fields[0] == "":
                fields = fields[1:]

            # Remove trailing empty field if present
            if fields[-1] == "":
                fields = fields[:-1]

            record_type = fields[0].strip()

            # Process header
            if record_type == "H":

                if columns is not None:
                    raise ValueError("Multiple header records found")

                columns = [col.strip() for col in fields[1:]]

            # Process detail records
            elif record_type == "D":

                if columns is None:
                    raise ValueError(
                        f"Header record missing before line {line_number}"
                    )

                values = fields[1:]

                if len(values) != len(columns):
                    raise ValueError(
                        f"Column mismatch at line {line_number}: "
                        f"Expected {len(columns)}, got {len(values)}"
                    )

                records.append(values)

            else:
                raise ValueError(
                    f"Unknown record type '{record_type}' "
                    f"at line {line_number}"
                )

    if columns is None:
        raise ValueError("Header record not found in file")

    return pd.DataFrame(records, columns=columns)
