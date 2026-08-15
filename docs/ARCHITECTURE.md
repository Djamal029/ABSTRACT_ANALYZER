# Architecture — Plateforme de soumission & tri d'abstracts scientifiques

Solution générique : utilisable par n'importe quel organisateur de conférence/colloque,
pas liée à un événement particulier. Chaque "édition" définit son propre thème, sa
fenêtre de soumission et ses critères — le moteur (embedding, scoring, clustering,
détection de doublons) est indépendant du domaine scientifique.

## Principes directeurs

- **Découplage strict par interfaces (DAO + Provider pattern)** : le code métier ne
  dépend jamais d'une techno concrète (MySQL, Postgres, ChromaDB, SPECTER2...).
  Chaque dépendance externe est masquée derrière une interface (`Protocol`/ABC), avec
  une implémentation injectée via la config (`app/core/config.py`).
  - Permet de migrer MySQL → PostgreSQL/pgvector sans toucher `services/` ni `api/`.
  - Permet de changer de modèle d'embedding (SPECTER2 → autre) par simple changement
    de config, sans toucher le code appelant.
- **Architecture en couches** : `api` → `services` → `dao` → stockage. Une couche ne
  parle jamais directement à la couche n-2 (l'API n'appelle jamais un DAO directement).
- **Validation humaine obligatoire** : aucune action automatique (fusion de doublons,
  exclusion d'abstract) n'est appliquée sans confirmation d'un organisateur. Les
  services de détection de doublons et de clustering ne font que *proposer*.

## Couches backend (FastAPI)

```
api/          → HTTP only : validation d'entrée (schemas Pydantic), appel des services,
                 sérialisation de sortie. Zéro logique métier.
services/     → Logique métier pure. Orchestre les DAO et les providers. C'est ici que
                 vivent : scoring de pertinence, détection de doublons, clustering.
dao/          → Accès aux données, deux familles :
                 - relational/  (métadonnées abstracts, users, éditions — MySQL puis
                   PostgreSQL au déploiement)
                 - vector/      (embeddings — ChromaDB aujourd'hui, pgvector au
                   déploiement une fois migré sur PostgreSQL)
domain/       → Entités métier (dataclasses), indépendantes de tout framework/ORM.
schemas/      → Contrats API (Pydantic), séparés des entités domaine.
jobs/         → Traitements asynchrones planifiés (clustering post-clôture).
core/         → Config, sécurité, logging transverses.
```

## Flux clés

### 1. Soumission d'un abstract
`POST /abstracts` → `AbstractService.submit()` :
1. Persistance des métadonnées via `AbstractDAO` (relationnel).
2. Vectorisation via `EmbeddingService` (délègue au provider configuré, ex. SPECTER2).
3. Stockage du vecteur via `VectorStoreDAO`.
4. Calcul de pertinence thème via `RelevanceService` (cosinus contre le vecteur du
   thème de l'édition) → alimente le classement live.
5. Détection de doublons potentiels via `DuplicateDetectionService` (similarité
   sémantique + lexicale combinée) → si score au-dessus du seuil, crée une
   `DuplicateFlag` **en attente de validation humaine**, ne bloque jamais la
   soumission.

### 2. Classement live
`GET /editions/{id}/ranking` → `RankingService` interroge les scores de pertinence
déjà calculés (pas de recalcul à la volée) et retourne le classement trié.

### 3. Clustering post-clôture (job automatisé)
Déclenché 1h après la clôture des soumissions (`jobs/clustering_job.py`, planifié par
`jobs/scheduler.py`) :
1. `HyperparamOptimizer` (Optuna, recherche bayésienne) réoptimise les hyperparamètres
   UMAP + HDBSCAN **pour cette édition précise** (le thème change à chaque événement,
   donc les hyperparamètres optimaux aussi).
2. `ClusteringService` applique UMAP (réduction de dimension) puis HDBSCAN (clustering
   density-based, pas besoin de fixer le nombre de clusters à l'avance) sur les
   embeddings de l'édition.
3. `TopicLabeling` extrait une étiquette lisible par cluster (mots-clés représentatifs).
4. Résultats persistés via `ClusterDAO`, consommés par `DashboardService`.

### 4. Dashboard organisateur
`GET /editions/{id}/dashboard` → `DashboardService` agrège : statistiques globales,
distribution des scores de pertinence, couverture du thème, top abstracts, axes
thématiques issus du clustering.

## Remplacer un composant sans casser le reste

| Vouloir changer...                  | Fichier à toucher                                   |
|--------------------------------------|-------------------------------------------------------|
| Base relationnelle (MySQL→Postgres)  | Nouvelle impl. de `dao/interfaces/*_dao.py` dans `dao/relational/`, switch dans `core/config.py` |
| Base vectorielle (Chroma→pgvector)   | Nouvelle impl. de `VectorStoreDAO` dans `dao/vector/`, switch dans `core/config.py` |
| Modèle d'embedding (SPECTER2→autre)  | Nouvelle impl. de `EmbeddingProvider` dans `services/embedding/`, switch dans `core/config.py` |
| Algo de clustering                   | `services/clustering/clustering_service.py` uniquement |

## Frontend (React)

```
pages/SubmissionForm/     → formulaire de soumission chercheur
pages/LiveRanking/        → classement live public/restreint
pages/OrganizerDashboard/ → dashboard organisateur (stats, clusters, validation doublons)
components/                → composants réutilisables par domaine fonctionnel
api/                        → client HTTP typé vers le backend
```

## Ce que ce dépôt contient à ce stade

Architecture + interfaces + squelettes de fichiers (signatures, docstrings, schémas de
données). La logique métier (calculs, appels modèles, requêtes DB réelles) reste à
implémenter derrière ces interfaces.
