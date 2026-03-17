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

### `json2md.py` — Génération Markdown depuis JSON

Génère des fichiers Markdown lisibles à partir des fichiers `pcg_{année}.json`. Le plan des comptes est rendu sous forme de liste hiérarchique indentée, et les différences par rapport à la version précédente sont incluses le cas échéant.

```bash
# Générer le Markdown d'une année spécifique
uv run json2md.py --year 2026

# Générer le Markdown pour toutes les années
uv run json2md.py --all

# Spécifier un répertoire de sortie
uv run json2md.py --all --output-dir out
```

Par défaut, les fichiers Markdown sont créés dans le même répertoire que les fichiers JSON sources (`versions/{année}/`).
