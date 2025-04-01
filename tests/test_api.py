import pytest
import requests

BASE_URL = "http://localhost:8000/records"  # Update with your API's base URL
record_ids = []  # List to keep track of inserted record IDs


def test_insert_100_records():
  # List to keep track of inserted record IDs
    for i in range(100):  # Loop to insert 100 records
        payload = {"text": f"Record {i}"}
        response = requests.post(BASE_URL, json=payload)

        # Verify response status code
        assert response.status_code == 200, f"Failed for record {i}, status_code: {response.status_code}"

        # Verify response body structure
        response_json = response.json()
        assert "status" in response_json and response_json["status"] == "success", f"Unexpected response for record {i}: {response_json}"
        assert "record_id" in response_json, f"Missing 'record_id' for record {i}"

        # Track the record ID for further validation or cleanup
        record_ids.append(response_json["record_id"])

        print(f"Record {i} successfully inserted with ID: {response_json['record_id']}")

    print(f"Successfully inserted 100 records. IDs: {record_ids}")

# Test 2: Retrieve the last 100 records
def test_retrieve_last_100_records():
    response = requests.get(BASE_URL, params={"records": 100})

    # Verify response status and structure
    assert response.status_code == 200
    data = response.json()
    assert "status" in data and data["status"] == "success"
    assert "data" in data

    # Verify record list
    records = data["data"]
    assert len(records) <= 100  # Should return at most 100 records

# Test 3: Retrieve a single record
def test_retrieve_single_record():
    # Insert a record to retrieve
    payload = {"text": "Single record"}
    insert_response = requests.post(BASE_URL, json=payload)
    print(f"Insert response: {insert_response.json()}")
    assert insert_response.status_code == 200
    record_id = insert_response.json()['record_id']['id']
    record_ids.append(insert_response.json()['record_id'])  # Track the inserted record ID

    # Retrieve the inserted record
    response = requests.get(BASE_URL, params={"record_id": record_id})

    # Verify response status and structure
    assert response.status_code == 200
    data = response.json()
    assert "status" in data and data["status"] == "success"
    assert "data" in data

    # Verify retrieved record data
    retrieved_record = data["data"]
    assert "id" in retrieved_record and retrieved_record["id"] == record_id
    assert "text_field" in retrieved_record and retrieved_record["text_field"] == "Single record"


# Test 4: Retrieve summary grouped by `updated_by`
def test_retrieve_summary():
    response = requests.get(BASE_URL)

    # Verify response status and structure
    assert response.status_code == 200
    data = response.json()
    assert "status" in data and data["status"] == "success"
    assert "data" in data

    # Verify summary structure
    summary = data["data"]
    for item in summary:
        assert "updated_by" in item
        assert "count" in item

# Test 5: Update 10 records with unique values
def test_update_10_records():
    record_list = []

    # Insert 10 records
    for i in range(10):
        payload = {"text": f"Original Record {i}"}
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 200
        record_ids.append(response.json()["record_id"])

    # Update the 10 records with unique values
    for i, record_id in enumerate(record_list):
        updated_text = f"Updated Record {i}"
        response = requests.put(
            f"{BASE_URL}/{record_id}",
            params={"updated_text": updated_text}
        )

        # Verify response status and structure
        assert response.status_code == 200
        data = response.json()
        assert "status" in data and data["status"] == "success"
        assert "data" in data

        # Verify updated record data
        updated_record = data["data"]
        assert "text_field" in updated_record and updated_record["text_field"] == updated_text
        

# Test 6: Verify `updated_by` and `updated_at` fields
def test_verify_updated_by_and_updated_at():
    # Insert a record and verify `updated_by`
    payload = {"text": "Record for testing updated_by"}
    insert_response = requests.post(BASE_URL, json=payload)
    assert insert_response.status_code == 200
    record_id = insert_response.json()["record_id"]["id"]
    record_ids.append(insert_response.json()["record_id"])  # Track the inserted record ID

    # Update the record and verify `updated_by` and `updated_at`
    updated_text = "Updated text field"
    update_response = requests.put(f"{BASE_URL}/{record_id}", params={"updated_text": updated_text})
    assert update_response.status_code == 200
    data = update_response.json()
    assert "data" in data
    updated_record = data["data"]

    # Verify `updated_by` and `updated_at` fields
    assert updated_record.get("updated_by") is not None
    assert updated_record.get("updated_at") is not None


# Test 7: Delete records and cleanup
def test_delete_records():

    for record in record_ids:
        record_id = record["id"]  # Extract the `id` to delete
        response = requests.delete(f"{BASE_URL}/delete/{record_id}")
        
        # Print statements for debugging (optional)
        print(f"Deleting record with ID: {record_id}")
        print(f"Response: {response.json()}")

        # Verify response status and structure
        assert response.status_code == 200
        data = response.json()
        assert "status" in data and data["status"] == "success"
        assert "data" in data

        # Verify deleted record data
        deleted_record = data["data"]
        assert "id" in deleted_record  # Ensure the `id` key exists
        assert deleted_record["id"] == record_id  # Match the returned `id` with `record_id`

