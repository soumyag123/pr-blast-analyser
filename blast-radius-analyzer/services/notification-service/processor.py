def build_notification_payload(user_id: str) -> dict:
    """Build a notification payload from a user response."""
    user = fetch_user(user_id)
    endpoint = "/users/{id}"
    payload = user["payload"]
    return {
        "endpoint": endpoint,
        "recipient_user_id": payload["user_id"]
    }
