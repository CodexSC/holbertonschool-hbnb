# On importe le module uuid pour générer des identifiants uniques
import uuid  
# On importe datetime et timezone pour gérer les dates avec fuseau horaire UTC
from datetime import datetime, timezone  


class BaseModel:
    """
    Classe de base pour toutes les entités HBnB.
    Fournit des attributs communs : id, created_at, updated_at.
    Toutes les autres classes héritent de cette classe.
    """

    def __init__(self):
        # Génère un identifiant unique pour l'objet sous forme de chaîne de caractères
        self.id = str(uuid.uuid4())        

        # Date/heure de création de l'objet (UTC)
        self.created_at = datetime.now(timezone.utc)   

        # Date/heure de dernière modification de l'objet (UTC)
        self.updated_at = datetime.now(timezone.utc)   

    def save(self):
        """
        Met à jour l'attribut updated_at.
        À appeler chaque fois qu'on modifie l'objet.
        """
        # On enregistre le moment exact où l'objet est modifié
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """
        Met à jour les attributs de l'objet depuis un dictionnaire.
        Ne modifie que les attributs existants.
        Actualise automatiquement updated_at.
        """
        # Parcourt toutes les paires clé/valeur du dictionnaire
        for key, value in data.items():
            # Vérifie que l'attribut existe sur l'objet pour éviter les erreurs
            if hasattr(self, key):
                # Modifie l'attribut correspondant à la clé avec la nouvelle valeur
                setattr(self, key, value)

        # Met à jour la date de dernière modification après toutes les modifications
        self.save()

    def to_dict(self):
        """
        Retourne une représentation de l'objet sous forme de dictionnaire.
        Utile pour convertir l'objet en JSON pour les API.
        """
        return {
            # ID unique de l'objet
            'id': self.id,

            # Date de création convertie en chaîne ISO standard
            'created_at': self.created_at.isoformat(),

            # Date de dernière modification convertie en chaîne ISO standard
            'updated_at': self.updated_at.isoformat()
        }