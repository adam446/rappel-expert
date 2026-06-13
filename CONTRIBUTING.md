# Contribuer a Rappel Expert

Merci de contribuer au projet.

## Installation

```bash
cp .env.example .env
docker compose up --build
```

## Organisation du code

- `frontend/` : interface React et calendrier.
- `backend/` : API FastAPI, services et regles expertes.
- `database/` : schema PostgreSQL et donnees de demonstration.
- `screenshots/` : captures utilisees dans la documentation.

## Proposer une modification

1. Creer une branche avec un nom explicite.
2. Limiter la modification a un objectif precis.
3. Verifier que `docker compose config` est valide.
4. Verifier que le frontend construit avec `npm run build`.
5. Decrire le comportement modifie dans la pull request.

## Conventions

- Conserver la logique de decision dans le backend.
- Ne pas recalculer les couleurs ou les etats experts dans React.
- Utiliser les services existants pour les operations metier.
- Documenter toute nouvelle route API dans le README.
