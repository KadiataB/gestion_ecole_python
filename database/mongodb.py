from pymongo import MongoClient
from models.etudiant import Etudiant
from models.utilisateur import Utilisateur

class BaseDeDonnees:
    def __init__(self, host='localhost', port=27017, db_name='gestion_etudiants'):
        """Initialise la connexion à MongoDB"""
        self.client = MongoClient(host, port)
        self.db = self.client["gestion_etudiants"]
        self.etudiants = self.db.etudiants
        self.utilisateurs = self.db.utilisateurs
        
        # Création d'un index unique pour le téléphone des étudiants
        self.etudiants.create_index([("telephone", 1)], unique=True)
        # Création d'un index unique pour les usernames
        self.utilisateurs.create_index([("username", 1)], unique=True)
    
    def ajouter_etudiant(self, etudiant):
        """Ajoute un étudiant à la base de données"""
        try:
            return str(self.etudiants.insert_one(etudiant.to_dict()).inserted_id)
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'étudiant: {e}")
            return None
    
    def obtenir_etudiant(self, etudiant_id):
        """Récupère un étudiant par son ID"""
        data = self.etudiants.find_one({"_id": etudiant_id})
        return Etudiant.from_dict(data) if data else None
    
    def rechercher_etudiants(self, critere, valeur):
        """Recherche des étudiants selon un critère (nom, prénom, téléphone, classe)"""
        query = {critere: {"$regex": valeur, "$options": "i"}}
        resultats = self.etudiants.find(query)
        return [Etudiant.from_dict(data) for data in resultats]
    
    def obtenir_tous_etudiants(self):
        """Récupère tous les étudiants"""
        resultats = self.etudiants.find()
        return [Etudiant.from_dict(data) for data in resultats]
    
    def mettre_a_jour_etudiant(self, etudiant):
        """Met à jour un étudiant dans la base de données"""
        try:
            return self.etudiants.update_one(
                {"_id": etudiant.id},
                {"$set": etudiant.to_dict()}
            ).modified_count > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'étudiant: {e}")
            return False
    
    def supprimer_etudiant(self, etudiant_id):
        """Supprime un étudiant de la base de données"""
        try:
            return self.etudiants.delete_one({"_id": etudiant_id}).deleted_count > 0
        except Exception as e:
            print(f"Erreur lors de la suppression de l'étudiant: {e}")
            return False