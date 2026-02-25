from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity that can be offered in a Place.
    Examples: Wi-Fi, Parking, Pool, Air conditioning.

    Attributes:
        name (str): Required, max 50 characters.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name   # uses the setter -> validates

    # ----------------------------------------------------------------
    # name: required, string, max 50 characters
    # ----------------------------------------------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Amenity name is required and must be a string.")
        if len(value) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")
        self._name = value

    # ----------------------------------------------------------------
    # to_dict: include amenity-specific fields
    # ----------------------------------------------------------------
    def to_dict(self):
        data = super().to_dict()
        data['name'] = self.name
        return data
