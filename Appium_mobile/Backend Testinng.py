import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_posts():
    """
    Test the GET /posts endpoint.
    """
    response = requests.get(f"{BASE_URL}/posts")

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate response type
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", \
        f"Unexpected Content-Type: {response.headers['Content-Type']}"

    # Validate response data structure
    data = response.json()
    assert isinstance(data, list), "Response is not a list"
    assert len(data) > 0, "Response data is empty"

    # Check the first item structure
    first_post = data[0]
    expected_keys = {"userId", "id", "title", "body"}
    assert expected_keys.issubset(first_post.keys()), "Missing keys in response data"

    print("GET /posts test passed!")


def test_get_post_by_id(post_id):
    """
    Test the GET /posts/{id} endpoint.
    """
    response = requests.get(f"{BASE_URL}/posts/{post_id}")

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate response data
    data = response.json()
    assert isinstance(data, dict), "Response is not a dictionary"
    assert data["id"] == post_id, f"Expected post ID {post_id}, got {data['id']}"

    print(f"GET /posts/{post_id} test passed!")


def test_post_create_post():
    """
    Test the POST /posts endpoint.
    """
    post_data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=post_data)

    # Validate status code
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Validate response data
    data = response.json()
    assert data["title"] == post_data["title"], f"Expected title {post_data['title']}, got {data['title']}"
    assert data["body"] == post_data["body"], f"Expected body {post_data['body']}, got {data['body']}"
    assert data["userId"] == post_data["userId"], f"Expected userId {post_data['userId']}, got {data['userId']}"

    print("POST /posts test passed!")


def test_put_update_post(post_id):
    """
    Test the PUT /posts/{id} endpoint.
    """
    updated_data = {
        "id": post_id,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1
    }

    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_data)

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate response data
    data = response.json()
    assert data["title"] == updated_data["title"], f"Expected title {updated_data['title']}, got {data['title']}"
    assert data["body"] == updated_data["body"], f"Expected body {updated_data['body']}, got {data['body']}"

    print(f"PUT /posts/{post_id} test passed!")




if __name__ == "__main__":
    print("Running backend tests...")
    test_get_posts()
    test_get_post_by_id(1)
    test_post_create_post()
    test_put_update_post(1)

