from app.auth.base import get_google_oauth_client

# Initializes the Google OAuth client by calling the `get_google_oauth_client` function
# from `app.auth.base`. This function encapsulates the logic for creating and configuring
# the Google OAuth client instance using settings from `app.core.config`.
google_oauth_client = get_google_oauth_client()
