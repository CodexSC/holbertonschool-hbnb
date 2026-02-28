from app.models.base_model import BaseModel


class Amenity(BaseModel):
    # Représente un équipement (Wi-Fi, Parking…)
    # Relation : liée à plusieurs Places (many-to-many)

    def __init__(self, name, description="", **kwargs):
        """Initialise une amenity avec un nom et une description validés."""
        super().__init__(**kwargs)
        self.name = name              # passe par le setter (validation)
        self.description = description

    # ------------------------------------------------------------------ #
    #  name                                                                #
    # ------------------------------------------------------------------ #
    @property
    def name(self):
        """Retourne le nom de l'amenity."""
        return self._name

    @name.setter
    def name(self, value):
        """Valide que le nom est une chaîne non vide, max 50 caractères."""
        if not value or not isinstance(value, str):
            raise ValueError("name is required.")
        value = value.strip()           # strip AVANT la vérification de longueur
        if not value:                   # attrape les chaînes tout-blancs ex: "   "
            raise ValueError("name is required.")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or fewer.")
        self._name = value

    # ------------------------------------------------------------------ #
    #  description                                                         #
    # ------------------------------------------------------------------ #
    @property
    def description(self):
        """Retourne la description de l'amenity."""
        return self._description

    @description.setter
    def description(self, value):
        """Valide que la description est une chaîne (ou vide par défaut)."""
        if value is not None and not isinstance(value, str):
            raise TypeError("description must be a string.")
        self._description = value.strip() if value else ""

    # ------------------------------------------------------------------ #
    #  update                                                              #
    # ------------------------------------------------------------------ #
    def update(self, data: dict):
        """Applique les modifications et rafraîchit updated_at."""
        if "name" in data:
            self.name = data["name"]           # setter → validation automatique
        if "description" in data:
            self.description = data["description"]
        self.save()                            # rafraîchit updated_at (BaseModel)

    # ------------------------------------------------------------------ #
    #  sérialisation                                                       #
    # ------------------------------------------------------------------ #
    def to_dict(self):
        """Retourne un dict avec le nom et la description."""
        d = super().to_dict()
        d.update({"name": self.name, "description": self.description})
        return d
