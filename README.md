# Système de Gestion des Étudiants — Python, MongoDB & Redis

Cette application en ligne de commande, développée en Python (POO), permet la gestion complète des étudiants. Elle combine **MongoDB** pour le stockage persistant et **Redis** pour la mise en cache, assurant performance et fiabilité.

---

## Table des matières

- [Technologies utilisées](#-technologies-utilisées)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture des données](#-architecture-des-données)
- [Rôle de MongoDB et Redis](#-rôle-de-mongodb-et-redis)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [Conclusion](#-conclusion)

---

## Technologies utilisées

- **Python 3.x** – Langage principal (POO)
- **MongoDB** – Base de données NoSQL
- **Redis** – Cache en mémoire pour améliorer la vitesse
- **Pymongo** – Client MongoDB pour Python
- **Redis-py** – Client Redis
- **bcrypt** – Hachage des mots de passe
- **pandas / openpyxl** – Import/export CSV/Excel
- **fpdf** – Génération de rapports PDF

---

## Fonctionnalités

### Étudiants

- Ajout avec validation (notes 0-20, téléphone unique)
- Affichage avec tri par moyenne
- Recherche par nom, prénom, téléphone ou classe
- Modification des notes
- Suppression d’étudiants
- Exportation (CSV, Excel, PDF, JSON)

### Utilisateurs & Authentification

- Connexion avec rôles :
  - **Admin** : contrôle total
  - **Enseignant** : gestion des notes
  - **Étudiant** : accès restreint à ses données
- Mots de passe sécurisés (bcrypt)
- Sessions gérées via Redis

### Statistiques

- Moyenne par classe
- Classement Top 10
- Export des résultats en PDF

---

## Architecture des données

Le système adopte une architecture **hybride MongoDB + Redis** pour allier durabilité et performance.

### MongoDB — Stockage principal

| Collection | Description                     | Champs clés                                                |
| ---------- | ------------------------------- | ---------------------------------------------------------- |
| `students` | Données complètes des étudiants | `first_name`, `last_name`, `phone`, `class_name`, `grades` |
| `users`    | Comptes utilisateurs            | `username`, `password_hash`, `role`, `student_phone`       |

### ⚡ Redis — Cache rapide

| Type de données           | Clé Redis             | TTL    | Utilité principale              |
| ------------------------- | --------------------- | ------ | ------------------------------- |
| Étudiant consulté souvent | `student:{phone}`     | 1h     | Lecture rapide                  |
| Sessions utilisateur      | `session:{user_id}`   | 1h     | Authentification rapide         |
| Statistiques par classe   | `class:stats:{class}` | 1h     | Évite les recalculs             |
| Classement top 10         | `rankings:top10`      | 30 min | Optimisation des tris fréquents |

---

## Rôle de MongoDB et Redis

### MongoDB (stockage permanent)

- Données des étudiants
- Comptes utilisateurs
- Notes et historique

### Redis (cache temporaire)
Redis est utilisé comme mémoire cache pour accélérer les opérations fréquentes dans l’application. Voici les principaux types de données qu’on y stocke :

-- Sessions utilisateurs (session:{id_utilisateur})
Lorsqu’un utilisateur se connecte, une session est créée dans Redis.

Elle contient des informations comme le nom d'utilisateur, le rôle (admin, enseignant...), la dernière activité, etc.

Ces données sont temporaires et supprimées automatiquement après une période d’inactivité (ex : 1 heure).

Cela permet une authentification rapide sans surcharge de MongoDB.

-- Étudiants fréquemment consultés (student:{telephone})
Lorsqu’un étudiant est consulté, l’application vérifie d’abord s’il est déjà dans Redis.

Si oui, on récupère les données directement depuis Redis, ce qui est plus rapide qu'un accès à MongoDB.

Si non, l’étudiant est récupéré depuis MongoDB et ajouté dans Redis pour les prochaines consultations.

Le cache est mis à jour en cas de modification ou après expiration.

-- Données statistiques temporaires (class:stats:{classe})
Les calculs comme les moyennes par classe ou la distribution des notes sont effectués une seule fois, puis mis en cache dans Redis.

Le cache est actualisé périodiquement (par exemple, après 1h) ou lorsque des modifications sont effectuées sur les notes de la classe.

### Stratégie d’invalidation du cache

Le cache est rafraîchi automatiquement lors de :

- Modifications d’un étudiant ou de ses notes
- Expiration TTL
- Déconnexion

| Donnée                | MongoDB | Redis  | Justification                             |
| --------------------- | ------- | ------ | ----------------------------------------- |
| Profils étudiants     | ✅ Oui  | ✅ Oui | Persistant + rapide                       |
| Notes                 | ✅ Oui  | ✅ Oui | Calculs fréquents, besoin de performance  |
| Utilisateurs          | ✅ Oui  | ❌ Non | Données sensibles, pas mises en cache     |
| Sessions              | ❌ Non  | ✅ Oui | Temporaires, stockées uniquement en cache |
| Moyennes / Classement | ❌ Non  | ✅ Oui | Données calculées et mises en cache       |
