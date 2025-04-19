from colorama import Fore, Style
from models.etudiant import Etudiant

class GestionEtudiants:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    def ajouter_etudiant(self, nom, prenom, telephone, classe, notes=None):
        """Ajoute un nouvel étudiant"""
        # Vérification que le téléphone n'existe pas déjà
        resultats = self.db.rechercher_etudiants("telephone", telephone)
        if resultats:
            print(f"{Fore.RED}Un étudiant avec ce numéro de téléphone existe déjà.{Style.RESET_ALL}")
            return None
        
        # Création de l'étudiant
        etudiant = Etudiant(nom, prenom, telephone, classe, notes)
        
        # Ajout dans MongoDB
        id_etudiant = self.db.ajouter_etudiant(etudiant)
        
        if id_etudiant:
            # Mise en cache dans Redis
            self.cache.mettre_en_cache_etudiant(etudiant)
            print(f"{Fore.GREEN}Étudiant ajouté avec succès !{Style.RESET_ALL}")
            return etudiant
        
        print(f"{Fore.RED}Erreur lors de l'ajout de l'étudiant.{Style.RESET_ALL}")
        return None
    
    def obtenir_etudiant(self, etudiant_id):
        """Obtient un étudiant depuis le cache ou la base de données"""
        # Tentative de récupération depuis le cache
        etudiant = self.cache.obtenir_etudiant_cache(etudiant_id)
        
        # Si pas dans le cache, récupération depuis MongoDB et mise en cache
        if not etudiant:
            etudiant = self.db.obtenir_etudiant(etudiant_id)
            if etudiant:
                self.cache.mettre_en_cache_etudiant(etudiant)
        
        return etudiant
    
    def rechercher_etudiants(self, critere, valeur):
        """Recherche des étudiants selon un critère"""
        return self.db.rechercher_etudiants(critere, valeur)
    
    def mettre_a_jour_notes(self, etudiant_id, notes):
        """Met à jour les notes d'un étudiant"""
        etudiant = self.obtenir_etudiant(etudiant_id)
        if not etudiant:
            print(f"{Fore.RED}Étudiant non trouvé.{Style.RESET_ALL}")
            return False
        
        # Mise à jour des notes
        for matiere, note in notes.items():
            if not etudiant.ajouter_note(matiere, note):
                print(f"{Fore.RED}Note invalide pour {matiere}: {note}. Les notes doivent être entre 0 et 20.{Style.RESET_ALL}")
                return False
        
        # Mise à jour dans MongoDB
        if self.db.mettre_a_jour_etudiant(etudiant):
            # Mise à jour du cache
            self.cache.mettre_en_cache_etudiant(etudiant)
            print(f"{Fore.GREEN}Notes mises à jour avec succès !{Style.RESET_ALL}")
            return True
        
        print(f"{Fore.RED}Erreur lors de la mise à jour des notes.{Style.RESET_ALL}")
        return False
    
    def supprimer_etudiant(self, etudiant_id):
        """Supprime un étudiant"""
        etudiant = self.obtenir_etudiant(etudiant_id)
        if not etudiant:
            print(f"{Fore.RED}Étudiant non trouvé.{Style.RESET_ALL}")
            return False
        
        # Suppression de MongoDB
        if self.db.supprimer_etudiant(etudiant_id):
            # Suppression du cache
            self.cache.supprimer_etudiant_cache(etudiant_id, etudiant.classe)
            print(f"{Fore.GREEN}Étudiant supprimé avec succès !{Style.RESET_ALL}")
            return True
        
        print(f"{Fore.RED}Erreur lors de la suppression de l'étudiant.{Style.RESET_ALL}")
        return False
    
    def afficher_etudiants(self, etudiants):
        """Affiche une liste d'étudiants sous forme de tableau"""
        if not etudiants:
            print(f"{Fore.YELLOW}Aucun étudiant trouvé.{Style.RESET_ALL}")
            return
        
        # En-tête du tableau
        print(f"\n{Fore.CYAN}{'ID':<10} {'Nom':<15} {'Prénom':<15} {'Téléphone':<15} {'Classe':<10} {'Moyenne':<8}{Style.RESET_ALL}")
        print("-" * 80)
        
        # Données
        for e in etudiants:
            print(f"{e.id[:8]:<10} {e.nom:<15} {e.prenom:<15} {e.telephone:<15} {e.classe:<10} {e.moyenne:<8.2f}")
        
        print("-" * 80)
        print(f"Total: {len(etudiants)} étudiant(s)")