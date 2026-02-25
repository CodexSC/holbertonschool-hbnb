from app.models.base_model import BaseModel


class Amenity(BaseModel):
    # Représente un équipement (Wi-Fi, Parking…)
    # Relation : liée à plusieurs Places (many-to-many)

    def __init__(self, name, description=""):
        """Initialise une amenity avec un nom validé."""
        super().__init__()
        self.name = name    # passe par le setter (validation)
        self.description = description

    @property
    def name(self):
        """Retourne le nom de l'amenity."""
        return self._name

    @name.setter
    def name(self, value):
        """Valide que le nom est non vide et max 50 caractères."""
        if not value or not isinstance(value, str):
            raise ValueError("name is required.")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or fewer.")
        self._name = value.strip()

    def to_dict(self):
        """Retourne un dict avec le nom et la description."""
        d = super().to_dict()
        d.update({"name": self.name, "description": self.description})
        return d
