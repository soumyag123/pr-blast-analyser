def fetch_user(user_id: str) -> dict:
    """Fetch a user payload from user-service."""
    endpoint = "/users/{id}"
    response = {
        "id": user_id,
        "email": "user@example.com",
        "user_id": user_id,
        "preferences": {"channel": "email"}
    }
    return {"endpoint": endpoint, "payload": response}
