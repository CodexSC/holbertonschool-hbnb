from app.models.base_model import BaseModel


class Place(BaseModel):
    # Hérite de BaseModel
    # Relation : appartient à un User (owner), reçoit des Reviews, propose des Amenities

    def __init__(self, title, description, price_per_night,
                 latitude, longitude, owner, max_guests=1, **kwargs):
        """Initialise un lieu avec ses coordonnées, son prix et son propriétaire."""
        super().__init__(**kwargs)      # forwarde kwargs pour la reconstruction depuis la persistence
        self.title = title
        self.description = description
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner              # instance User (relation one-to-many)
        self.max_guests = max_guests
        self.is_available = True
        self.reviews = []               # liste de Review (one-to-many)
        self.amenities = []             # liste d'Amenity (many-to-many)

    # ── Setters avec validation ──────────────────────────────────────────────

    @property
    def title(self):
        """Retourne le titre."""
        return self._title

    @title.setter
    def title(self, value):
        """Valide que le titre est non vide et max 100 caractères."""
        if not value or not isinstance(value, str):
            raise ValueError("title is required.")
        value = value.strip()           # strip AVANT la vérification de longueur
        if not value:                   # attrape les chaînes tout-blancs ex: "   "
            raise ValueError("title is required.")
        if len(value) > 100:
            raise ValueError("title must be 100 characters or fewer.")
        self._title = value

    @property
    def price_per_night(self):
        """Retourne le prix par nuit."""
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Valide que le prix est un nombre positif."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("price_per_night must be a positive number.")
        if value <= 0:
            raise ValueError("price_per_night must be a positive number.")
        self._price_per_night = value

    @property
    def latitude(self):
        """Retourne la latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Valide que la latitude est entre -90 et 90."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("latitude must be a number between -90 and 90.")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be between -90 and 90.")
        self._latitude = value

    @property
    def longitude(self):
        """Retourne la longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Valide que la longitude est entre -180 et 180."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("longitude must be a number between -180 and 180.")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180 and 180.")
        self._longitude = value

    # ── Gestion des relations ────────────────────────────────────────────────

    def add_review(self, review):
        """Attache une Review à ce lieu."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Attache une Amenity à ce lieu (sans doublons)."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Retire une Amenity de ce lieu."""
        self.amenities = [a for a in self.amenities if a.id != amenity.id]

    def list_amenities(self):
        """Retourne la liste des noms des amenities."""
        return [a.name for a in self.amenities]

    def get_average_rating(self):
        """Calcule la moyenne des ratings de toutes les reviews liées."""
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    def set_availability(self, available: bool):
        """Met à jour la disponibilité du lieu."""
        self.is_available = available
        self.save()

    # ── Sérialisation ────────────────────────────────────────────────────────

    def to_dict(self):
        """Retourne un dict complet du lieu avec owner et amenities embarqués."""
        d = super().to_dict()
        d.update({
            "title": self.title,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "max_guests": self.max_guests,
            "is_available": self.is_available,
            # Owner embarqué avec les champs publics (spec projet)
            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email,
            } if self.owner else None,
            # Amenities : id + name uniquement (pas le to_dict() complet)
            "amenities": [
                {"id": a.id, "name": a.name} for a in self.amenities
            ],
        })
        return d
