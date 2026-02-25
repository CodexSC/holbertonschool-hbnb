from app.models.base_model import BaseModel


class Review(BaseModel):
    # Hérite de BaseModel
    # Relation : écrite par un User, associée à un Place

    def __init__(self, text, rating, place, user):
        """Initialise une review avec son contenu, sa note et ses relations."""
        super().__init__()
        self.text = text        # passe par le setter (validation)
        self.rating = rating    # passe par le setter (validation 1-5)
        self.place = place      # instance Place
        self.user = user        # instance User

    # ── Setters avec validation ──────────────────────────────────────────────

    @property
    def text(self):
        """Retourne le contenu de la review."""
        return self._text

    @text.setter
    def text(self, value):
        """Valide que le texte est non vide."""
        if not value or not isinstance(value, str):
            raise ValueError("text is required.")
        self._text = value

    @property
    def rating(self):
        """Retourne la note."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Valide que la note est entre 1 et 5."""
        if value is None or not (1 <= int(value) <= 5):
            raise ValueError("rating must be between 1 and 5.")
        self._rating = int(value)

    def to_dict(self):
        """Retourne un dict avec le texte, la note et les ids liés."""
        d = super().to_dict()
        d.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None,
        })
        return d