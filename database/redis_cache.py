import redis
import json
from models.etudiant import Etudiant

class CacheRedis:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialise la connexion à Redis"""
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.expiration = 3600  
    
    def mettre_en_cache_etudiant(self, etudiant):
        """Met en cache les informations d'un étudiant"""
        key = f"etudiant:{etudiant.id}"
        self.redis.hmset(key, {
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "telephone": etudiant.telephone,
            "classe": etudiant.classe,
            "moyenne": str(etudiant.moyenne),
            "notes": json.dumps(etudiant.notes)
        })
        self.redis.expire(key, self.expiration)
        
        # Mise à jour du cache de la classe
        self.redis.sadd(f"classe:{etudiant.classe}", etudiant.id)
    
    def obtenir_etudiant_cache(self, etudiant_id):
        """Récupère un étudiant depuis le cache"""
        key = f"etudiant:{etudiant_id}"
        if not self.redis.exists(key):
            return None
        
        data = self.redis.hgetall(key)
        etudiant = Etudiant(
            data["nom"],
            data["prenom"],
            data["telephone"],
            data["classe"],
            json.loads(data.get("notes", "{}"))
        )
        etudiant.id = etudiant_id
        etudiant.moyenne = float(data.get("moyenne", 0))
        return etudiant
    
    def supprimer_etudiant_cache(self, etudiant_id, classe=None):
        """Supprime un étudiant du cache"""
        key = f"etudiant:{etudiant_id}"
        if classe:
            self.redis.srem(f"classe:{classe}", etudiant_id)
        self.redis.delete(key)