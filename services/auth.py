import bcrypt
from db.mongodb import MongoDB

class AuthService:
    def __init__(self):
        self.mongo = MongoDB().utilisateurs

    def login(self):
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        user = self.mongo.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            print(f"✅ Connecté en tant que {user['role']}")
            return user
        print("Identifiants incorrects.")
        return None
