import uuid # genere id unique 
from datetime import datetime, timezone # gère date et heure


class BaseModel:
    """
    Base class for all HBnB entities
    Provides common attributes: id, created_at, updated_at
    All other models inherit from this class
    """

    def __init__(self):
        self.id = str(uuid.uuid4()) # Unique identifier as string
        self.created_at = datetime.now(timezone.utc)   # Set once at creation
        self.updated_at = datetime.now(timezone.utc)   # Updated every time the object changes

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """
        Update object attributes from a dictionary
        Only updates attributes that already exist on the object
        Automatically refreshes updated_at
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
