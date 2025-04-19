import uuid
import bcrypt

class Utilisateur:
    def __init__(self, username, password, role, etudiant_id=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = self._hash_password(password)
        self.role = role 
        self.etudiant_id = etudiant_id
    
    def _hash_password(self, password):
        """Hash le mot de passe avec bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash stocké"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Convertit l'objet Utilisateur en dictionnaire"""
        return {
            "_id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "etudiant_id": self.etudiant_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crée un objet Utilisateur à partir d'un dictionnaire"""
        utilisateur = cls(
            data["username"],
            "",  
            data["role"],
            data.get("etudiant_id", None)
        )
        utilisateur.id = data.get("_id", str(uuid.uuid4()))
        utilisateur.password = data["password"]  
        return utilisateur