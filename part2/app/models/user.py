# Import du module regex pour valider les emails
import re  
# Import du module hashlib pour hasher les mots de passe
import hashlib  
# Import de la classe parent BaseModel pour hériter des attributs communs
from part2.app.models.base_model import BaseModel


class User(BaseModel):
    # Chaque User peut avoir des Places et écrire des Reviews

    def __init__(self, first_name=None, last_name=None, email=None,
                 password=None, is_admin=False, **kwargs):
        """Initialise un utilisateur avec validation et hash du mot de passe.

        Cette signature accepte les champs explicites pour les créations
        normales ainsi que ``**kwargs`` lorsqu'on reconstruit un objet à
        partir de la persistence (id, created_at, updated_at, etc.).
        """
        super().__init__(**kwargs)  # Appelle le constructeur de BaseModel

        # Affectations passant par les setters qui valident
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email

        # Le mot de passe peut arriver en clair lors de la création;
        # on ne stocke que le hash. Ne pas remplacer s'il existe déjà via
        # kwargs (reconstruction depuis le stockage).
        if password is not None:
            self.password_hash = self._hash_password(password)
        elif "password_hash" in kwargs:
            # si le hash était fourni par kwargs, on le conserve
            self.password_hash = kwargs.get("password_hash")

        self.is_admin = is_admin

    # ── Helpers de validation

    @staticmethod
    def _validate_name(value, field):
        """Vérifie que le nom est une string non vide de max 50 caractères."""
        if not value or not isinstance(value, str):  # Vérifie qu’il existe et est une string
            raise ValueError(f"{field} is required.")  
        if len(value) > 50:  # Vérifie la longueur max
            raise ValueError(f"{field} must be 50 characters or fewer.")
        return value.strip()  # Supprime les espaces inutiles en début/fin

    @staticmethod
    def _validate_email(email):
        """Vérifie le format email avec une regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"  # Regex simple pour email
        if not re.match(pattern, email):  # Vérifie si ça correspond
            raise ValueError(f"Invalid email format: {email}")
        return email.lower()  # Retourne l’email en minuscules

    @staticmethod
    def _hash_password(password):
        """Retourne le hash SHA-256 du mot de passe."""
        if not password:  # Vérifie que le mot de passe existe
            raise ValueError("Password is required.")
        # Encode la string en bytes puis calcule le hash SHA-256 et retourne en hexadécimal
        return hashlib.sha256(password.encode()).hexdigest()

    # ── Setters avec validation (pattern @property)

    @property
    def first_name(self):
        """Retourne le prénom de l'utilisateur."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Valide et assigne le prénom via _validate_name."""
        self._first_name = self._validate_name(value, "first_name")

    @property
    def last_name(self):
        """Retourne le nom de famille."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Valide et assigne le nom via _validate_name."""
        self._last_name = self._validate_name(value, "last_name")

    @property
    def email(self):
        """Retourne l'email de l'utilisateur."""
        return self._email

    @email.setter
    def email(self, value):
        """Valide et assigne l'email via _validate_email."""
        self._email = self._validate_email(value)

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def update_profile(self, data):
        """Autorise uniquement la mise à jour des champs autorisés du profil."""
        allowed = {"first_name", "last_name", "email"}  # Champs modifiables
        # Appelle update() de BaseModel seulement sur les champs autorisés
        self.update({k: v for k, v in data.items() if k in allowed})

    def change_password(self, new_password):
        """Hash le nouveau mot de passe et remplace l'ancien."""
        self.password_hash = self._hash_password(new_password)  # Hash
        self.save()  # Met à jour updated_at

    def authenticate(self, password):
        """Compare le hash du mot de passe fourni avec celui stocké."""
        return self.password_hash == self._hash_password(password)  # True/False

    def to_dict(self):
        """Retourne un dictionnaire avec les infos publiques de l'utilisateur."""
        d = super().to_dict()  # Appelle BaseModel.to_dict() → id, created_at, updated_at
        d.update({
            "first_name": self.first_name,  # Ajoute prénom
            "last_name": self.last_name,    # Ajoute nom
            "email": self.email,            # Ajoute email
            "is_admin": self.is_admin,      # Ajoute info admin
        })
        return d  # Retourne le dictionnaire prêt pour JSON/API
