from sqlalchemy.orm import DeclarativeBase


# Base class for SQLAlchemy declarative models.
# All SQLAlchemy models in the application will inherit from this `Base` class.
# This allows SQLAlchemy to map Python classes to database tables automatically.
class Base(DeclarativeBase):
    pass

