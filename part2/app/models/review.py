# Import de la classe parent BaseModel pour hériter des attributs communs
from part2.app.models.base_model import BaseModel  


class Review(BaseModel):
    # Hérite de BaseModel : id, created_at, updated_at
    # Relation : écrite par un User, associée à un Place

    def __init__(self, text, rating, place, user):
        """Initialise une review avec son contenu, sa note et ses relations."""
        super().__init__()  # Initialise id, created_at, updated_at
        self.text = text        # Passe par le setter pour validation
        self.rating = rating    # Passe par le setter pour validation (1-5)
        self.place = place      # Instance de Place associée
        self.user = user        # Instance de User qui écrit la review

    # ── Setters et getters avec validation ──────────────────────────────────

    @property
    def text(self):
        """Retourne le contenu de la review."""
        return self._text

    @text.setter
    def text(self, value):
        """Valide que le texte est non vide et est une string."""
        if not value or not isinstance(value, str):
            raise ValueError("text is required.")
        self._text = value

    @property
    def rating(self):
        """Retourne la note."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Valide que la note est un entier entre 1 et 5."""
        if value is None or not (1 <= int(value) <= 5):
            raise ValueError("rating must be between 1 and 5.")
        self._rating = int(value)

    # ── Sérialisation pour API ──────────────────────────────────────────────

    def to_dict(self):
        """
        Retourne un dictionnaire avec :
        - texte de la review
        - note
        - id du Place associé
        - id du User qui a écrit la review
        """
        d = super().to_dict()  # id, created_at, updated_at
        d.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,  # id du lieu
            "user_id": self.user.id if self.user else None,    # id de l’auteur
        })
        return d