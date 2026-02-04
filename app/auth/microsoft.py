from app.auth.base import get_microsoft_oauth_client

# Initializes the Microsoft OAuth client by calling the `get_microsoft_oauth_client` function
# from `app.auth.base`. This function encapsulates the logic for creating and configuring
# the Microsoft OAuth client instance using settings from `app.core.config`.
microsoft_oauth_client = get_microsoft_oauth_client()
