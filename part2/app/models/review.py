from app.models.base_model import BaseModel


class Review(BaseModel):
    # Hérite de BaseModel : id, created_at, updated_at
    # Relation : écrite par un User, associée à un Place

    def __init__(self, text, rating, place, user, **kwargs):
        """Initialise une review avec son contenu, sa note et ses relations."""
        super().__init__(**kwargs)      # forwarde kwargs pour la reconstruction depuis la persistence
        self.text = text                # passe par le setter pour validation
        self.rating = rating            # passe par le setter pour validation (1-5)
        self.place = place              # instance de Place associée
        self.user = user                # instance de User qui écrit la review

    # ── Setters avec validation ──────────────────────────────────────────────

    @property
    def text(self):
        """Retourne le contenu de la review."""
        return self._text

    @text.setter
    def text(self, value):
        """Valide que le texte est une string non vide."""
        if not value or not isinstance(value, str):
            raise ValueError("text is required.")
        value = value.strip()           # strip AVANT la vérification de contenu
        if not value:                   # attrape les chaînes tout-blancs ex: "   "
            raise ValueError("text is required.")
        self._text = value

    @property
    def rating(self):
        """Retourne la note."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Valide que la note est un entier entre 1 et 5."""
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("rating must be between 1 and 5.")
        if not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5.")
        self._rating = value

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def update(self, data: dict):
        """Met à jour text et/ou rating via les setters, puis rafraîchit updated_at.

        Surcharge nécessaire pour que les setters (et leur validation)
        soient appelés plutôt que le setattr brut de BaseModel.update().
        place et user sont immuables après création.
        """
        if "text" in data:
            self.text = data["text"]
        if "rating" in data:
            self.rating = data["rating"]
        self.save()

    # ── Sérialisation pour API ───────────────────────────────────────────────

    def to_dict(self):
        """Retourne un dictionnaire avec le texte, la note et les ids liés."""
        d = super().to_dict()           # id, created_at, updated_at
        d.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None,
        })
        return d
