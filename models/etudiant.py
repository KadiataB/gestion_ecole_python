import uuid

class Etudiant:
    def __init__(self, nom, prenom, telephone, classe, notes=None):
        self.id = str(uuid.uuid4())
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.classe = classe
        self.notes = notes if notes else {}
        self.moyenne = self.calculer_moyenne()
    
    def calculer_moyenne(self):
        """Calcule la moyenne des notes de l'étudiant"""
        if not self.notes:
            return 0
        total = sum(self.notes.values())
        return round(total / len(self.notes), 2) if len(self.notes) > 0 else 0
    
    def ajouter_note(self, matiere, note):
        """Ajoute ou modifie une note pour une matière"""
        if 0 <= note <= 20:
            self.notes[matiere] = note
            self.moyenne = self.calculer_moyenne()
            return True
        return False
    
    def to_dict(self):
        """Convertit l'objet Etudiant en dictionnaire"""
        return {
            "_id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "telephone": self.telephone,
            "classe": self.classe,
            "notes": self.notes,
            "moyenne": self.moyenne
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crée un objet Etudiant à partir d'un dictionnaire"""
        etudiant = cls(
            data["nom"],
            data["prenom"],
            data["telephone"],
            data["classe"],
            data.get("notes", {})
        )
        etudiant.id = data.get("_id", str(uuid.uuid4()))
        etudiant.moyenne = data.get("moyenne", etudiant.calculer_moyenne())
        return etudiant