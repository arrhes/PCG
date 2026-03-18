# Scripts

Outils pour traiter les fichiers PDF sources du PCG.

## Prérequis

- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets Python)

## Installation

```bash
cd scripts
uv sync
```

## Utilisation

### `pdf2html.py` — Conversion PDF vers HTML

Convertit les PDF sources en HTML à l'aide de [PyMuPDF](https://pymupdf.readthedocs.io/). La mise en forme (polices, couleurs), les images et la structure du document sont préservées.

```bash
# Convertir les PDF d'une année spécifique
uv run pdf2html.py --year 2026

# Convertir tous les PDF
uv run pdf2html.py --all

# Spécifier un répertoire de sortie
uv run pdf2html.py --all --output-dir out
```

Par défaut, les fichiers HTML sont créés dans le même répertoire que les PDF sources.

### `pdf2md.py` — Conversion PDF vers Markdown

Convertit les PDF sources en Markdown à l'aide de [PyMuPDF](https://pymupdf.readthedocs.io/). Préserve le gras/italique, détecte les niveaux de titre à partir de la taille des polices, conserve les liens internes et gère l'italique synthétique (texte en cisaillement utilisé pour les comptes facultatifs).

```bash
# Convertir les PDF d'une année spécifique
uv run pdf2md.py --year 2026

# Convertir tous les PDF
uv run pdf2md.py --all

# Spécifier un répertoire de sortie
uv run pdf2md.py --all --output-dir out
```

Par défaut, les fichiers Markdown sont créés dans le même répertoire que les PDF sources.

### `html2md.py` — Conversion HTML vers Markdown

Convertit les fichiers HTML sources (générés par `pdf2html.py`) en Markdown à l'aide de [html-to-markdown](https://github.com/kreuzberg-dev/html-to-markdown). Les images embarquées sont ignorées.

```bash
# Convertir les HTML d'une année spécifique
uv run html2md.py --year 2026

# Convertir tous les HTML
uv run html2md.py --all

# Spécifier un répertoire de sortie
uv run html2md.py --all --output-dir out
```

Par défaut, les fichiers Markdown sont créés dans le même répertoire que les HTML sources.

> **Note :** les fichiers HTML sources utilisent un positionnement CSS absolu (réplique visuelle du PDF), sans structure sémantique (`<h1>`–`<h6>`, `<em>`, etc.). Le résultat est donc moins structuré que celui de `pdf2md.py`, qui extrait les métadonnées directement du PDF.
