import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    # Chaque User peut avoir des Places et écrire des Reviews

    def __init__(self, first_name=None, last_name=None, email=None,
                 password=None, is_admin=False, **kwargs):
        """Initialise un utilisateur avec validation et hash du mot de passe.

        Cette signature accepte les champs explicites pour les créations
        normales ainsi que ``**kwargs`` lorsqu'on reconstruit un objet à
        partir de la persistence (id, created_at, updated_at, etc.).
        """
        super().__init__(**kwargs)

        self._first_name = None
        self._last_name = None
        self._email = None
        self._password_hash = kwargs.get('password_hash')

        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email

        # Le mot de passe peut arriver en clair lors de la création;
        # on ne stocke que le hash sous un attribut privé.
        # Ne pas remplacer s'il existe déjà via kwargs (reconstruction).
        if password is not None:
            self._password_hash = self._hash_password(password)

        self.is_admin = is_admin

    # ── Helpers de validation ────────────────────────────────────────────────

    @staticmethod
    def _validate_name(value, field):
        """Vérifie que le nom est une string non vide de max 50 caractères."""
        if not value or not isinstance(value, str):
            raise ValueError(f"{field} is required.")
        value = value.strip()           # strip AVANT la vérification de longueur
        if not value:                   # attrape les chaînes tout-blancs ex: "   "
            raise ValueError(f"{field} is required.")
        if len(value) > 50:
            raise ValueError(f"{field} must be 50 characters or fewer.")
        return value

    @staticmethod
    def _validate_email(email):
        """Vérifie le format email avec une regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email format: {email}")
        return email.lower()

    @staticmethod
    def _hash_password(password):
        """Retourne le hash SHA-256 du mot de passe.

        Note: SHA-256 est suffisant pour la partie 2. En partie 3,
        remplacer par bcrypt ou argon2 avant toute mise en production.
        """
        if not password:
            raise ValueError("Password is required.")
        return hashlib.sha256(password.encode()).hexdigest()

    # ── Setters avec validation (pattern @property) ──────────────────────────

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_name(value, "first_name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_name(value, "last_name")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def update_profile(self, data):
        """Autorise uniquement la mise à jour de first_name et last_name.

        L'email est intentionnellement exclu : sa mise à jour implique
        une vérification d'unicité qui ne peut se faire qu'au niveau
        du facade (accès au repo nécessaire).
        """
        allowed = {'first_name', 'last_name'}
        self.update({k: v for k, v in data.items() if k in allowed})

    def change_password(self, new_password):
        """Hash le nouveau mot de passe et remplace l'ancien."""
        self._password_hash = self._hash_password(new_password)
        self.save()

    def authenticate(self, password):
        """Compare le hash du mot de passe fourni avec celui stocké."""
        return self._password_hash == self._hash_password(password)

    def to_dict(self):
        """Retourne un dictionnaire avec les infos publiques de l'utilisateur.

        Le hash du mot de passe est explicitement exclu — il ne doit
        jamais être exposé dans une réponse API.
        """
        d = super().to_dict()
        d.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        })
        return d   # password_hash absent : attribut privé (_) ignoré par BaseModel
