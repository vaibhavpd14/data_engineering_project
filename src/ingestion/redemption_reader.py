
import json
import pandas as pd


def read_redemption_file(file_path):
    """
    Reads a JSON redemption file and converts its nested transaction
    records into a flat Pandas DataFrame.
    
    Supports both a single JSON object and a list of JSON objects.
    """

    # load json content 
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # If the JSON contains a single object, convert it into a list
    # so that the remaining code can handle both formats uniformly
    if isinstance(data, dict):
        data = [data]

    # Validate that the JSON contains either an object or a list
    if not isinstance(data, list):
        raise ValueError("JSON must contain an object or a list of objects")

    # Store the extracted redemption transaction records
    records = []

    # Iterate through each member record in the JSON data
    for member in data:

        # Ensure each member record is a JSON object (dictionary)
        if not isinstance(member, dict):
            raise ValueError("Each member record must be a JSON object")

        # Extract member-level information
        # These values are common to all transactions of this member
        member_id = member.get("member_id")
        feed_date = member.get("feed_date")

        # Extract the list of redemption transactions
        # If the key is missing, use an empty list by default
        redemptions = member.get("redemptions", [])

        # Handle cases where redemptions is explicitly null in JSON
        if redemptions is None:
            redemptions = []

        # Validate that redemptions is a list before iterating
        if not isinstance(redemptions, list):
            raise ValueError(
                f"Redemptions must be a list for member {member_id}"
            )

        # Process each redemption transaction for the current member
        for transaction in redemptions:

            # Ensure each transaction is a JSON object
            if not isinstance(transaction, dict):
                raise ValueError(
                    f"Invalid transaction for member {member_id}"
                )

            # Combine member-level information with transaction-level
            # information to create one flat record per transaction
            records.append({
                "MEMBER_ID": member_id,
                "FEED_DATE": feed_date,
                "TXN_ID": transaction.get("txn_id"),
                "TXN_DATE": transaction.get("txn_date"),
                "PARTNER": transaction.get("partner"),
                "MILES_REDEEMED": transaction.get("miles_redeemed"),
                "STATUS": transaction.get("status")
            })

    
    return pd.DataFrame(records)
