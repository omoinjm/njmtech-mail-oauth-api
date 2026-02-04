from enum import Enum


# Defines an enumeration for OAuth providers.
# This helps in standardizing the names of providers used throughout the application
# and provides a type-safe way to reference them.
class Provider(Enum):
    # Represents Google as an OAuth provider.
    GOOGLE = 0
    # Represents Microsoft as an OAuth provider.
    MICROSOFT = 1

