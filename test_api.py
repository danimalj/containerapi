import pytest
import requests

BASE_URL = "http://localhost:8000/records/"  # Update with your API's base URL

# Keep track of record IDs for cleanup
record_ids_for_cleanup = []

# Test 1: Insert 1000 records
def test_insert_1000_records():
    global record_ids_for_cleanup
    for i in range(1000):
        payload = {"text_field": f"Record {i}"}
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["text_field"] == f"Record {i}"
        record_ids_for_cleanup.append(data["data"]["id"])

# Test 2: Retrieve last 100 records
def test_retrieve_last_100_records():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    records = data["data"]
    assert len(records) <= 100  # Should return at most 100 records

# Test 3: Retrieve a single record
def test_retrieve_single_record():
    # Insert a record to retrieve
    payload = {"text_field": "Single record"}
    insert_response = requests.post(BASE_URL, json=payload)
    assert insert_response.status_code == 200
    record_id = insert_response.json()["data"]["id"]

    # Retrieve the inserted record
    response = requests.get(f"{BASE_URL}{record_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["text_field"] == "Single record"

    # Add to cleanup list
    global record_ids_for_cleanup
    record_ids_for_cleanup.append(record_id)

# Test 4: Update 10 records with unique values
def test_update_10_records():
    record_ids = []

    # Insert 10 records
    for i in range(10):
        payload = {"text_field": f"Original Record {i}"}
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 200
        record_ids.append(response.json()["data"]["id"])

    # Update the 10 records with unique values
    for i, record_id in enumerate(record_ids):
        updated_text = f"Updated Record {i}"
        response = requests.put(f"{BASE_URL}{record_id}?updated_text={updated_text}")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["text_field"] == updated_text

    # Add to cleanup list
    global record_ids_for_cleanup
    record_ids_for_cleanup.extend(record_ids)

# Test 5: Verify `updated_by` and `updated_at` fields
def test_verify_updated_by_and_updated_at():
    # Insert a record and verify `updated_by`
    payload = {"text_field": "Record for testing updated_by"}
    insert_response = requests.post(BASE_URL, json=payload)
    assert insert_response.status_code == 200
    data = insert_response.json()["data"]

    # Update the record and verify `updated_by` and `updated_at`
    record_id = data["id"]
    updated_text = "Updated text field"
    update_response = requests.put(f"{BASE_URL}{record_id}?updated_text={updated_text}")
    assert update_response.status_code == 200
    updated_data = update_response.json()["data"]
    assert updated_data.get("updated_by") is not None  # Ensure `updated_by` is set on update
    assert updated_data.get("updated_at") is not None  # Ensure `updated_at` is set on update

    # Add to cleanup list
    global record_ids_for_cleanup
    record_ids_for_cleanup.append(record_id)

# Test 6: Delete records and cleanup
def test_delete_records():
    global record_ids_for_cleanup
    for record_id in record_ids_for_cleanup:
        response = requests.delete(f"{BASE_URL}{record_id}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == record_id
    record_ids_for_cleanup = []  # Clear cleanup list after deletion