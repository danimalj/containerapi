import pytest
import requests

BASE_URL = "http://localhost:8000/containers"  # Update with your API's base URL

def test_get_container_success():
    """
    Test the successful retrieval of container details for a specific container.
    """
    container_name = "fastapi_one_container"  # Provide a valid container name
    response = requests.get(BASE_URL, params={"container_name": container_name})

    # Verify response status code
    assert response.status_code == 200, f"Failed for container {container_name}, status_code: {response.status_code}"

    # Verify response body structure
    response_json = response.json()
    assert "status" in response_json and response_json["status"] == "success", f"Unexpected response for container {container_name}: {response_json}"
    assert "data" in response_json, f"Missing 'data' key in response for container {container_name}"

    # Verify container details
    container_data = response_json["data"]
    assert "container_name" in container_data and container_data["container_name"] == container_name
    assert "operating_system" in container_data
    assert "external_volumes" in container_data
    assert "ip_address" in container_data
    assert "ports" in container_data

    print(f"Container {container_name} details successfully retrieved.")

def test_get_container_not_found():
    """
    Test retrieval of container details for a non-existent container.
    """
    container_name = "non_existent_container"  # Provide a fake container name
    response = requests.get(BASE_URL, params={"container_name": container_name})

    # Verify response status code
    assert response.status_code == 404, f"Expected 404 for container {container_name}, but got {response.status_code}"

    # Verify response body structure
    response_json = response.json()
    assert "detail" in response_json, f"Missing 'detail' key in response for container {container_name}"
    assert response_json["detail"] == f"Container '{container_name}' not found.", f"Unexpected response for container {container_name}: {response_json}"

    print(f"Container {container_name} not found as expected.")

def test_get_container_server_error():
    """
    Test retrieval of container details in case of server-side error.
    Simulate the error by misconfiguring Docker or calling with invalid settings.
    """
    container_name = ""  # Provide an invalid container name or scenario
    response = requests.get(BASE_URL, params={"container_name": container_name})

    # Verify response status code
    assert response.status_code == 500, f"Expected 500 for server error, but got {response.status_code}"

    # Verify response body structure
    response_json = response.json()
    assert "detail" in response_json, f"Missing 'detail' key in response for server error"

    print("Server error successfully simulated.")