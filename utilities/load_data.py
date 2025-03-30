import requests
import argparse

BASE_URL = "http://localhost:8080/records"  # Replace with your actual API endpoint

def load_data(records: int =100):
    """
    Load a specified number of records into the database.
    """
    for i in range(records):
        payload = {"text": f"Record {i}"}
        response = requests.post(BASE_URL, json=payload)

        # Verify response status code
        if response.status_code != 200:
            print(f"Failed to insert record {i}, status_code: {response.status_code}")
            continue

        # Verify response body structure
        response_json = response.json()
        if "status" not in response_json or response_json["status"] != "success":
            print(f"Unexpected response for record {i}: {response_json}")
            continue

        if "record_id" not in response_json:
            print(f"Missing 'record_id' for record {i}")
            continue

        # Track the record ID for further validation or cleanup
        print(f"Record {i} successfully inserted with ID: {response_json['record_id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data into the database.")
    parser.add_argument("--records", type=int, default=100, help="Number of records to insert")
    args = parser.parse_args()

    load_data(args.records)