def fetch_user_for_billing(user_id: str) -> dict:
    """Fetch billing-relevant user data."""
    endpoint = "/users/{id}"
    return {
        "endpoint": endpoint,
        "payload": {
            "id": user_id,
            "email": "user@example.com"
        }
    }
