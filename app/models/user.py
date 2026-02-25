import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    # Hérite de BaseModel (id, created_at, updated_at)
    # Relation : possède des Places, écrit des Reviews

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialise un utilisateur avec validation des champs et hash du mot de passe."""
        super().__init__()
        self.first_name = first_name    # passe par le setter (validation)
        self.last_name = last_name
        self.email = email
        self.password_hash = self._hash_password(password)  # jamais stocké en clair
        self.is_admin = is_admin

    # ── Helpers de validation ────────────────────────────────────────────────

    @staticmethod
    def _validate_name(value, field):
        """Vérifie que le nom est une string non vide de max 50 caractères."""
        if not value or not isinstance(value, str):
            raise ValueError(f"{field} is required.")
        if len(value) > 50:
            raise ValueError(f"{field} must be 50 characters or fewer.")
        return value.strip()

    @staticmethod
    def _validate_email(email):
        """Vérifie le format email avec une regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email format: {email}")
        return email.lower()

    @staticmethod
    def _hash_password(password):
        """Retourne le hash SHA-256 du mot de passe."""
        if not password:
            raise ValueError("Password is required.")
        return hashlib.sha256(password.encode()).hexdigest()

    # ── Setters avec validation (pattern @property) ──────────────────────────

    @property
    def first_name(self):
        """Retourne le prénom."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Valide et assigne le prénom."""
        self._first_name = self._validate_name(value, "first_name")

    @property
    def last_name(self):
        """Retourne le nom."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Valide et assigne le nom."""
        self._last_name = self._validate_name(value, "last_name")

    @property
    def email(self):
        """Retourne l'email."""
        return self._email

    @email.setter
    def email(self, value):
        """Valide et assigne l'email."""
        self._email = self._validate_email(value)

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def update_profile(self, data):
        """Autorise uniquement la mise à jour des champs profil autorisés."""
        allowed = {"first_name", "last_name", "email"}
        self.update({k: v for k, v in data.items() if k in allowed})

    def change_password(self, new_password):
        """Hash et remplace le mot de passe actuel."""
        self.password_hash = self._hash_password(new_password)
        self.save()

    def authenticate(self, password):
        """Compare le hash du mdp fourni avec celui stocké."""
        return self.password_hash == self._hash_password(password)

    def to_dict(self):
        """Retourne un dict avec les infos publiques de l'utilisateur."""
        d = super().to_dict()
        d.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
        return d
