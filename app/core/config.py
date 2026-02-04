from pydantic_settings import BaseSettings, SettingsConfigDict

# Define a Settings class that inherits from Pydantic's BaseSettings.
# This class is used to manage application settings, loading them from environment variables or a .env file.
class Settings(BaseSettings):
    # Database connection URL.
    DATABASE_URL: str

    # Google OAuth client ID, client secret, and redirect URI.
    # These are used for authenticating users via Google.
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Microsoft OAuth client ID, client secret, and redirect URI.
    # These are used for authenticating users via Microsoft.
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    MICROSOFT_REDIRECT_URI: str

    # Secret key for signing session cookies and other security-related operations.
    SECRET_KEY: str

    # Pydantic model configuration.
    # This specifies that settings should be loaded from a `.env` file if present.
    model_config = SettingsConfigDict(env_file=".env")

# Create an instance of the Settings class.
# This instance will automatically load the configured environment variables.
settings = Settings()