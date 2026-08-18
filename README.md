# Abstract Analyzer

Plateforme de soumission et de tri d'abstracts scientifiques, générique pour n'importe quel organisateur
de conférence, colloque ou journée thématique : soumission, score de pertinence en temps réel contre le
thème de l'édition, détection de doublons (toujours validée par un humain), clustering thématique
automatisé post-clôture (UMAP + HDBSCAN, hyperparamètres réoptimisés par édition via Optuna), et dashboard
organisateur.

> **Statut actuel : single-tenant.** Le projet deviendra un SaaS multi-tenant (plusieurs organisateurs sur
> la même instance, isolation par `organizationId`) mais cette phase est **délibérément reportée** — on
> construit et valide le produit single-tenant d'abord. Ne réintroduisez pas `organizationId`/
> `Organization` de votre propre initiative.

Pour comprendre en profondeur le rôle de chaque classe, ses relations et le *pourquoi* de chaque choix de
conception, voir [`docs/PROJECT_EXPLAINED.qmd`](docs/PROJECT_EXPLAINED.qmd) (rendu :
`docs/PROJECT_EXPLAINED.html`, via `quarto render`). Ce README couvre l'essentiel pour démarrer.

## Stack

- **Backend** : FastAPI, architecture en couches strictes — `domain/` → `dao/` (interfaces + implémentations)
  → `services/` → `api/`. Une couche ne parle jamais directement à la couche n-2 (l'API n'appelle jamais un
  DAO). Toute dépendance externe (base de données, base vectorielle, modèle d'embedding) est masquée
  derrière une interface, remplaçable par config sans toucher au code métier.
- **Base relationnelle** : MySQL en local, PostgreSQL + pgvector visé au déploiement.
- **Base vectorielle** : ChromaDB en local, pgvector au déploiement (fusionné avec PostgreSQL).
- **Embedding** : SPECTER2 par défaut (modèle entraîné pour la similarité entre documents scientifiques),
  remplaçable par un autre provider sans changer le code appelant.
- **Frontend** : React (squelette pas encore développé).
- **Gestionnaire de paquets Python** : [`uv`](https://docs.astral.sh/uv/).

## Prérequis

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- Une instance MySQL locale accessible (par défaut `mysql+pymysql://root:@localhost:3306/abstract_analyzer`)
- [Quarto](https://quarto.org/) uniquement si vous voulez re-générer `docs/PROJECT_EXPLAINED.html`

## Setup

```bash
cd backend
uv sync                 # installe les dépendances depuis pyproject.toml / uv.lock
cp .env.example .env    # puis ajustez la connexion DB si besoin
```

`core/config.py` lit la configuration via Pydantic Settings (`databaseUrl` notamment) — c'est le seul
endroit où la base relationnelle active est choisie.

> **État du serveur** : `app/main.py` est encore un stub (pas d'instance FastAPI créée). Le point d'entrée
> `uvicorn app.main:app --reload` fonctionnera une fois cette étape codée — voir la section *Où en est le
> code* ci-dessous pour savoir quoi écrire en premier.

## Structure du projet

```text
backend/app/
  domain/       → entités métier pures (aucune dépendance framework/ORM)
  dao/
    interfaces/ → contrats DAO/Provider (AbstractDAO, VectorStoreDAO, EmbeddingProvider...)
    relational/ → implémentations SQLAlchemy (MySQLAbstractDAO...) + modèles ORM
  services/     → logique métier, orchestre les DAO/providers via leurs interfaces
  api/          → endpoints FastAPI, validation d'entrée, appel des services — zéro logique métier
  jobs/         → traitements planifiés (ex. clustering post-clôture)
  schemas/      → contrats API (Pydantic), distincts des entités domaine
  core/         → config, sécurité (hash mot de passe, JWT), logging
docs/           → documentation architecture (voir plus bas)
frontend/       → squelette React
```

## Conventions de code

- **Commentaires en anglais**, même si les échanges/discussions du projet se font en français.
- **Une couche ne dépend jamais d'une implémentation concrète**, seulement d'une interface. Si vous ajoutez
  un service, il doit prendre `AbstractDAO`/`VectorStoreDAO`/etc. (l'interface), jamais `MySQLAbstractDAO`
  directement.
- **Transactions** : les DAO ne font jamais `db.commit()` (seulement `add()`/`flush()`). C'est
  `api/deps.py::get_db()` qui commite si la requête HTTP entière réussit, et fait `rollback()` sinon — pour
  qu'un endpoint qui enchaîne plusieurs appels DAO reste atomique.
- **Pas de suppression physique de `User`** : `deactivate()` (soft delete via `isActive`), jamais de
  `delete`, parce que `Abstract.authorId` et `AuditLog.actorId` le référencent.
- **`DuplicateFlag`** ne change jamais de statut automatiquement — uniquement via une action explicite d'un
  organisateur côté API.

## Où en est le code

Le domaine, les interfaces DAO/Provider et les modèles ORM sont codés. Une seule implémentation concrète
existe à ce jour (`MySQLAbstractDAO`) ; le reste (`EditionDAOImpl`, `UserDAOImpl`, `ClusterDAOImpl`,
`ChromaVectorStore`, `Specter2Provider`...), les services et la couche API sont encore des stubs à écrire
sur ce même patron. Le statut réel (codé vs stub) de chaque classe est visible dans
[`docs/class_diagram.html`](docs/class_diagram.html).

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — principes, flux clés, tableau "que changer pour migrer X".
- [`docs/PROJECT_EXPLAINED.qmd`](docs/PROJECT_EXPLAINED.qmd) — explication classe par classe : rôle,
  relations, pourquoi chaque choix de conception a été fait.
- [`docs/CLASS_DIAGRAM.md`](docs/CLASS_DIAGRAM.md) / [`docs/class_diagram.html`](docs/class_diagram.html) —
  diagramme de classes avec toutes les connexions intra- et inter-couches.

## Tests

```bash
cd backend
uv run pytest
```
