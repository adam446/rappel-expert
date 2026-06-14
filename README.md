# Rappel Expert

> Systeme expert web pour generer, suivre et classifier automatiquement des taches recurrentes.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## 1. Description du projet

Application web qui cree des series de taches, genere leurs rappels dans le backend, les persiste dans PostgreSQL et calcule automatiquement leur etat avec des regles `IF / ELSE`.

L'exemple livre est le paiement mensuel d'une facture d'electricite de 120 $, du 15 juin 2026 au 15 juin 2027. Le jeu de donnees cree 13 rappels.

## 2. Fonctionnalites principales

- Creation, consultation et modification d'une tache recurrente.
- Archivage d'une serie et de ses rappels.
- Generation mensuelle et hebdomadaire dans FastAPI.
- Modification, completion et suppression d'un rappel individuel.
- Calendrier mensuel avec titre, montant, etat et couleur fournis par l'API.
- Listes separees des rappels urgents et en retard.
- Reapplication manuelle ou automatique des regles expertes.
- Persistance PostgreSQL dans un volume Docker.
- Connexion par nom d'utilisateur ou email avec routes API protegees.
- Inscription utilisateur avec nom complet, email, nom d'utilisateur et mot de passe.
- Isolation des taches par utilisateur; l'administrateur peut superviser toutes les donnees.
- Reinitialisation de mot de passe par lien temporaire envoye par courriel SMTP.
- Tableau de bord administrateur avec statistiques globales et liste des utilisateurs.

## 3. Architecture de l'application

```text
React / Vite (port 5173)
        |
        | HTTP / JSON
        v
FastAPI / SQLAlchemy (port 8000)
        |
        | SQL
        v
PostgreSQL (port 5432)
```

Le frontend affiche les valeurs `expert_state` et `color` retournees par l'API. Il ne determine pas lui-meme si un rappel est urgent ou en retard.

## 4. Technologies utilisees

- Frontend : React 19, Vite 6, CSS.
- Backend : Python 3.12, FastAPI, SQLAlchemy, Pydantic.
- Base de donnees : PostgreSQL 17.
- Execution : Docker Compose.

## 5. Modele de base de donnees

Le schema se trouve dans `database/schema.sql` et les donnees de demonstration dans `database/seed.sql`.

```text
users 1 ---- N recurring_tasks 1 ---- N reminders
```

`recurring_tasks` contient la definition de la serie. `reminders` contient chaque occurrence, son statut utilisateur, son etat expert et sa couleur. La contrainte unique `(recurring_task_id, due_date)` empeche les doublons dans une meme serie.

Lors de la modification d'une serie, l'approche choisie est la regeneration partielle : les rappels completes sont conserves; les autres sont regeneres selon la nouvelle definition. Une serie archivee archive tous ses rappels. Une serie annulee conserve les rappels completes et annule les autres.

## 6. Regles du systeme expert

Les regles sont dans `backend/app/services/expert_rules_service.py` et sont appliquees dans cet ordre :

1. `status == completed` donne `completed` et `green`.
2. `status == cancelled` donne `cancelled` et `gray`.
3. `status == archived` donne `archived` et `gray`.
4. Une date passee donne `overdue` et `red`.
5. Une date comprise entre aujourd'hui et aujourd'hui + 7 jours donne `urgent` et `orange`.
6. Toute autre date donne `normal` et `blue`.

L'ordre garantit qu'un rappel complete, annule ou archive n'est jamais reclasse en retard.

## 7. Routes API

| Methode | Route | Action |
|---|---|---|
| POST | `/auth/login` | Ouvrir une session utilisateur ou administrateur |
| POST | `/auth/signup` | Creer un compte utilisateur et ouvrir une session |
| POST | `/auth/forgot-password` | Envoyer un lien de reinitialisation par courriel |
| POST | `/auth/reset-password` | Definir un nouveau mot de passe avec le jeton recu |
| GET | `/admin/dashboard` | Afficher les statistiques et utilisateurs, admin uniquement |
| GET | `/auth/me` | Lire l'utilisateur connecte |
| GET | `/recurring-tasks` | Lister les series |
| GET | `/recurring-tasks/{id}` | Lire une serie |
| POST | `/recurring-tasks` | Creer une serie et ses rappels |
| PUT | `/recurring-tasks/{id}` | Modifier et regenerer une serie |
| DELETE | `/recurring-tasks/{id}` | Archiver une serie |
| GET | `/reminders` | Lister les rappels apres calcul des regles |
| GET | `/reminders/{id}` | Lire un rappel |
| GET | `/reminders/overdue` | Lister les rappels en retard |
| GET | `/reminders/upcoming` | Lister les rappels urgents sur 7 jours |
| PUT | `/reminders/{id}` | Modifier un rappel et recalculer son etat |
| PUT | `/reminders/{id}/complete` | Completer un rappel |
| DELETE | `/reminders/{id}` | Supprimer un rappel |
| POST | `/expert-rules/apply` | Recalculer tous les rappels |

La documentation interactive est disponible sur `http://localhost:8000/docs`.

## 8. Installation du projet

Prerequis : Docker avec le module Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Au premier demarrage, PostgreSQL execute le schema et insere l'exemple de facture. Les executions suivantes reutilisent le volume `postgres_data`.

Le compte administrateur initial est configure dans `.env` avec `ADMIN_FULL_NAME`, `ADMIN_USERNAME`, `ADMIN_EMAIL` et `ADMIN_PASSWORD`. Les valeurs de developpement par defaut sont `Administrateur`, `admin`, `admin@example.com` et `admin123`. Modifiez egalement `SECRET_KEY` avant tout deploiement.

Les courriels de reinitialisation utilisent `SMTP_FROM_EMAIL` comme expediteur. Configurez aussi `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_USE_TLS` et `FRONTEND_URL`. Pour Gmail, utilisez un mot de passe d'application plutot que le mot de passe normal du compte.

## 9. Execution du projet

- Application : `http://localhost:5173`
- API : `http://localhost:8000`
- Documentation API : `http://localhost:8000/docs`
- Verification API : `http://localhost:8000/health`

```bash
docker compose down
```

Pour reinitialiser completement les donnees de demonstration :

```bash
docker compose down -v
docker compose up --build
```

## 10. Captures d'ecran

Le dossier `screenshots/` est reserve aux captures de la page calendrier, du formulaire, du detail d'un rappel et de la documentation Swagger. Elles doivent etre produites depuis l'environnement execute avant la remise.

## 11. Difficultes rencontrees

- Les mois n'ont pas tous le meme nombre de jours. Un jour 29, 30 ou 31 est ramene au dernier jour valide du mois.
- Une modification de serie ne doit pas effacer l'historique complete. Le service preserve ces occurrences et regenere uniquement les autres.
- Les statuts utilisateur ont priorite sur les regles de date afin qu'une tache completee reste verte.

## 12. Ameliorations futures

- Separation des donnees par utilisateur et gestion de plusieurs comptes.
- Notifications par courriel ou navigateur.
- Filtres, recherche, export CSV et statistiques.
- Migrations de base de donnees avec Alembic.
- Tests d'integration navigateur et deploiement automatise.

## Contribution

Les consignes de contribution sont disponibles dans [CONTRIBUTING.md](CONTRIBUTING.md).
