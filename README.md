# Plan Comptable Général (JSON)

## Informations
Le plan des comptes complet au format **JSON**.

Les données sont répliquées depuis le Plan Comptable Général (PCG) français émis chaque année par l'[Autorité des Normes Comptables](https://www.anc.gouv.fr) (ANC).


## Liens
| Version | Consolidée (Source ANC) | Consolidée (Source PDF) | Recueil (Source ANC) | Recueil (Source PDF) | Structure |
| ------- | -------------- | -------------- | ----------- | ----------- | --------- |
| 2026    | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/PCG_janvier2026/PCG--1er-janvier-2026.pdf) | [Lien](Liens/pcg_20260101.pdf) | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/PCG_janvier2026/Recueil-PCG-Janvier-2026.pdf) | [Lien](Liens/recueil_20260101.pdf) | [Lien](versions/2026/README.md) |
| 2025    | Non disponible | Non disponible | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/PCG_Janvier2025/Recueil-NF-Janvier-2025.pdf) | [Lien](Liens/recueil_20250101.pdf) | [Lien](versions/2025/README.md) |
| 2024    | Non disponible | [Lien](Liens/pcg_20240101.pdf) | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/Recueil%20comptable%20entreprises/2024/Recueil_normes-comptables2024.pdf) | [Lien](Liens/recueil_20240101.pdf) | [Lien](versions/2024/README.md) |
| 2023    | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/PCG_Janvier2023/PCG_1er-janvier-2023.pdf) | [Lien](Liens/pcg_20230101.pdf) | [Lien](https://www.anc.gouv.fr/files/anc/files/1_Normes_fran%C3%A7aises/Reglements/Recueils/Recueil%20comptable%20entreprises/2023/Recueil-normes-comptables_2023.pdf) | [Lien](Liens/recueil_20230101.pdf) | [Lien](versions/2023/README.md) |


## Structure
Les différentes versions sont à retrouver dans le dossier [*versions*](versions), organisées par année. Chaque dossier contient les fichiers suivants ainsi qu'un `README.md` décrivant la structure des données :

- **`nested.json`** — Version hiérarchique avec sous-comptes imbriqués.
- **`flat.json`** — Version à plat avec référence au compte parent.
- **`diff.json`** — Différences par rapport à la version précédente (absent pour la première version).

```
versions/
├── 2023/
│   ├── nested.json
│   ├── flat.json
│   └── README.md
├── 2024/
│   ├── nested.json
│   ├── flat.json
│   ├── diff.json
│   └── README.md
├── 2025/
│   ├── nested.json
│   ├── flat.json
│   ├── diff.json
│   └── README.md
└── 2026/
    ├── nested.json
    ├── flat.json
    ├── diff.json
    └── README.md
```

