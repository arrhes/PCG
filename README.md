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

Certains liens du site de l'ANC ne fonctionnent pas. Nous les avons contactés à ce sujet, sans réponse pour le moment.


## Structure
Les différentes versions sont à retrouver dans le dossier [*versions*](versions), organisées par année. Chaque dossier contient les fichiers suivants ainsi qu'un `README.md` décrivant la structure des données :

- **`pcg_{année}.json`** — Fichier unique contenant le plan des comptes en formats hiérarchique et à plat, ainsi que les différences par rapport à la version précédente (absent pour la première version).
- **`pcg_{année}.schema.json`** — Schéma JSON ([json-schema.org](https://json-schema.org/)) décrivant la structure du fichier.

```
versions/
├── 2023/
│   ├── pcg_2023.json
│   ├── pcg_2023.schema.json
│   └── README.md
├── 2024/
│   ├── pcg_2024.json
│   ├── pcg_2024.schema.json
│   └── README.md
├── 2025/
│   ├── pcg_2025.json
│   ├── pcg_2025.schema.json
│   └── README.md
└── 2026/
    ├── pcg_2026.json
    ├── pcg_2026.schema.json
    └── README.md
```
