import os
import sys
from colorama import init, Fore, Style

# Pour gérer les chemins des modules internes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.etudiant import Etudiant
from database.mongodb import BaseDeDonnees
from database.redis_cache import CacheRedis
from services.gestion_etudiants import GestionEtudiants
from utils.validators import Validators

# Initialiser colorama pour les couleurs dans le terminal
init()

class MenuApplication:
    def __init__(self):
        # Connexion aux bases de données
        self.db = BaseDeDonnees()
        self.cache = CacheRedis()
        
        # Services
        self.gestion_etudiants = GestionEtudiants(self.db, self.cache)
    
    def afficher_menu_principal(self):
        """Affiche le menu principal"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}=== SYSTÈME DE GESTION DES ÉTUDIANTS ==={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Menu principal:{Style.RESET_ALL}")
            print("1. Ajouter un étudiant")
            print("2. Afficher tous les étudiants")
            print("3. Rechercher un étudiant")
            print("4. Modifier les notes d'un étudiant")
            print("5. Supprimer un étudiant")
            print("0. Quitter")
            
            choix = input("\nVotre choix: ")
            
            if choix == "1":
                self.menu_ajouter_etudiant()
            elif choix == "2":
                self.menu_afficher_etudiants()
            elif choix == "3":
                self.menu_rechercher_etudiant()
            elif choix == "4":
                self.menu_modifier_notes()
            elif choix == "5":
                self.menu_supprimer_etudiant()
            elif choix == "0":
                print(f"{Fore.GREEN}Au revoir !{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Choix invalide. Veuillez réessayer.{Style.RESET_ALL}")
                input("Appuyez sur Entrée pour continuer...")
    
    def menu_ajouter_etudiant(self):
        """Menu pour ajouter un étudiant"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}=== AJOUTER UN ÉTUDIANT ==={Style.RESET_ALL}")
        
        # Saisie des informations
        nom = input("Nom: ")
        while not Validators.valider_nom(nom):
            print(f"{Fore.RED}Nom invalide. Veuillez entrer un nom valide.{Style.RESET_ALL}")
            nom = input("Nom: ")
        
        prenom = input("Prénom: ")
        while not Validators.valider_prenom(prenom):
            print(f"{Fore.RED}Prénom invalide. Veuillez entrer un prénom valide.{Style.RESET_ALL}")
            prenom = input("Prénom: ")
        
        telephone = input("Téléphone (9 chiffres): ")
        while not Validators.valider_telephone(telephone):
            print(f"{Fore.RED}Téléphone invalide. Veuillez entrer un numéro de 9 chiffres.{Style.RESET_ALL}")
            telephone = input("Téléphone (9 chiffres): ")
        
        classe = input("Classe: ")
        while not Validators.valider_classe(classe):
            print(f"{Fore.RED}Classe invalide. Veuillez entrer une classe valide.{Style.RESET_ALL}")
            classe = input("Classe: ")
        
        # Ajout de notes (optionnel)
        notes = {}
        ajouter_notes = input("Voulez-vous ajouter des notes maintenant ? (o/n): ").lower() == 'o'
        
        if ajouter_notes:
            while True:
                matiere = input("Matière (ou Entrée pour terminer): ")
                if not matiere:
                    break
                
                note_str = input(f"Note pour {matiere} (0-20): ")
                while not Validators.valider_note(note_str):
                    print(f"{Fore.RED}Note invalide. Veuillez entrer une note entre 0 et 20.{Style.RESET_ALL}")
                    note_str = input(f"Note pour {matiere} (0-20): ")
                
                notes[matiere] = float(note_str)
        
        # Ajout de l'étudiant
        etudiant = self.gestion_etudiants.ajouter_etudiant(nom, prenom, telephone, classe, notes)
        
        if etudiant:
            print(f"{Fore.GREEN}Étudiant ajouté avec succès !{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Erreur lors de l'ajout de l'étudiant.{Style.RESET_ALL}")
        
        input("Appuyez sur Entrée pour continuer...")
    
    def menu_afficher_etudiants(self):
        """Menu pour afficher tous les étudiants"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}=== LISTE DES ÉTUDIANTS ==={Style.RESET_ALL}")
        
        etudiants = self.db.obtenir_tous_etudiants()
        self.gestion_etudiants.afficher_etudiants(etudiants)
        
        input("Appuyez sur Entrée pour continuer...")
    
    def menu_rechercher_etudiant(self):
        """Menu pour rechercher un étudiant"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}=== RECHERCHER UN ÉTUDIANT ==={Style.RESET_ALL}")
        
        print("Critères de recherche:")
        print("1. Nom")
        print("2. Prénom")
        print("3. Téléphone")
        print("4. Classe")
        
        choix = input("\nVotre choix: ")
        
        critere = ""
        if choix == "1":
            critere = "nom"
        elif choix == "2":
            critere = "prenom"
        elif choix == "3":
            critere = "telephone"
        elif choix == "4":
            critere = "classe"
        else:
            print(f"{Fore.RED}Choix invalide.{Style.RESET_ALL}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        valeur = input(f"Rechercher {critere}: ")
        
        etudiants = self.gestion_etudiants.rechercher_etudiants(critere, valeur)
        self.gestion_etudiants.afficher_etudiants(etudiants)
        
        input("Appuyez sur Entrée pour continuer...")
    
    def menu_modifier_notes(self):
        """Menu pour modifier les notes d'un étudiant"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}=== MODIFIER LES NOTES D'UN ÉTUDIANT ==={Style.RESET_ALL}")
        
        # Recherche de l'étudiant
        telephone = input("Téléphone de l'étudiant: ")
        etudiants = self.gestion_etudiants.rechercher_etudiants("telephone", telephone)
        
        if not etudiants:
            print(f"{Fore.RED}Aucun étudiant trouvé avec ce numéro de téléphone.{Style.RESET_ALL}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        etudiant = etudiants[0]
        print(f"\nÉtudiant: {etudiant.prenom} {etudiant.nom} (Classe: {etudiant.classe})")
        
        # Affichage des notes actuelles
        print("\nNotes actuelles:")
        if etudiant.notes:
            for matiere, note in etudiant.notes.items():
                print(f"- {matiere}: {note}")
        else:
            print("Aucune note enregistrée.")
        
        # Modification des notes
        nouvelles_notes = {}
        
        while True:
            matiere = input("\nMatière à modifier (ou Entrée pour terminer): ")
            if not matiere:
                break
            
            note_str = input(f"Nouvelle note pour {matiere} (0-20): ")
            while not valider_note(note_str):
                print(f"{Fore.RED}Note invalide. Veuillez entrer une note entre 0 et 20.{Style.RESET_ALL}")
                note_str = input(f"Nouvelle note pour {matiere} (0-20): ")
            
            nouvelles_notes[matiere] = float(note_str)
        
        if nouvelles_notes:
            if self.gestion_etudiants.mettre_a_jour_notes(etudiant.id, nouvelles_notes):
                print(f"{Fore.GREEN}Notes mises à jour avec succès !{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Erreur lors de la mise à jour des notes.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Aucune note modifiée.{Style.RESET_ALL}")
        
        input("Appuyez sur Entrée pour continuer...")
    
    def menu_supprimer_etudiant(self):
        """Menu pour supprimer un étudiant"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}=== SUPPRIMER UN ÉTUDIANT ==={Style.RESET_ALL}")
        
        # Recherche de l'étudiant
        telephone = input("Téléphone de l'étudiant à supprimer: ")
        etudiants = self.gestion_etudiants.rechercher_etudiants("telephone", telephone)
        
        if not etudiants:
            print(f"{Fore.RED}Aucun étudiant trouvé avec ce numéro de téléphone.{Style.RESET_ALL}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        etudiant = etudiants[0]
        print(f"\nÉtudiant trouvé: {etudiant.prenom} {etudiant.nom} (Classe: {etudiant.classe})")
        
        confirmation = input(f"Êtes-vous sûr de vouloir supprimer cet étudiant ? (o/n): ").lower()
        
        if confirmation == 'o':
            if self.gestion_etudiants.supprimer_etudiant(etudiant.id):
                print(f"{Fore.GREEN}Étudiant supprimé avec succès !{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Erreur lors de la suppression de l'étudiant.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Suppression annulée.{Style.RESET_ALL}")
        
        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    app = MenuApplication()
    app.afficher_menu_principal()


