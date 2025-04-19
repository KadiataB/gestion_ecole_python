import re

class Validators:
    """Classe pour gérer la validation des données d'élèves"""
    
    @staticmethod
    def valider_telephone(numero):
        """Valide le numéro d'étudiant"""
        return bool(re.match(r'^\d{9}$', numero))
    
    @staticmethod
    def valider_prenom(prenom):
        """Valide le prénom d'étudiant"""
        return bool(re.match(r'^[A-Za-zÀ-ÿ\s-]{3,}$', prenom))
    
    @staticmethod
    def valider_nom(nom):
        """Valide le nom d'étudiant"""
        return bool(re.match(r'^[A-Za-zÀ-ÿ\s-]{2,}$', nom))
    
    @staticmethod
    def valider_classe(classe):
        """Valide le niveau universitaire"""
        return bool(re.match(r'^(Licence|Master|Doctorat) [1-3]$', classe))
    
    @staticmethod
    def valider_note(notes):
        """Valide le format des notes"""
        pattern = r'^[A-Za-z]+(\[[0-9,|:.]+\])+(#[A-Za-z]+\[[0-9,|:.]+\])*#?$'
        return bool(re.match(pattern, notes))
