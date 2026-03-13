# Version 2025

## Structure

Trois fichiers sont disponibles :

- **`nested.json`** — Version hiérarchique avec sous-comptes imbriqués.
- **`flat.json`** — Version à plat avec référence au compte parent.
- **`diff.json`** — Différences par rapport à la version précédente (2024).

### Format hiérarchique (`nested.json`)
| Clé        | Type                           | Description                                                                                                                                                                                                                                     |
| ---------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `number`   | `int`                          | Le numéro du compte.                                                                                                                                                                                                                            |
| `label`    | `string`                       | Le libellé du compte.                                                                                                                                                                                                                           |
| `system`   | `"minimal"` `"facultatif"`     | Le système dans lequel s'inscrit le compte. <br/> `minimal` si le compte fait partie du plan de comptes minimal. <br/> `facultatif` si le compte est facultatif (présenté en italique dans le recueil). Le plan minimal contient tous les comptes minimaux ; l'ensemble complet contient les comptes minimaux et facultatifs. |
| `accounts` | `array`                        | La liste des sous-comptes, reprenant la même structure de manière récursive.                                                                                                                                                                    |

### Format à plat (`flat.json`)
| Clé        | Type                           | Description                                                                                                                                                                                                                                     |
| ---------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `number`   | `int`                          | Le numéro du compte.                                                                                                                                                                                                                            |
| `label`    | `string`                       | Le libellé du compte.                                                                                                                                                                                                                           |
| `system`   | `"minimal"` `"facultatif"`     | Le système dans lequel s'inscrit le compte. <br/> `minimal` si le compte fait partie du plan de comptes minimal. <br/> `facultatif` si le compte est facultatif (présenté en italique dans le recueil). Le plan minimal contient tous les comptes minimaux ; l'ensemble complet contient les comptes minimaux et facultatifs. |
| `parent`   | `int` \| `null`                | Le numéro du compte parent, ou `null` pour les comptes racines (classes).                                                                                                                                                                       |

## Extraits

### `nested.json`
```js
[
    {
        "number": 1,
        "label": "Comptes de capitaux",
        "system": "minimal",
        "accounts": [
            {
                "number": 10,
                "label": "Capital et réserves",
                "system": "minimal",
                "accounts": [
                    {
                        "number": 101,
                        "label": "Capital",
                        "system": "minimal",
                        "accounts": [
                            {
                                "number": 1011,
                                "label": "Capital souscrit - non appelé",
                                "system": "facultatif",
                                "accounts": []
                            },
    ...
]
```

### Différences (`diff.json`)

| Clé        | Type    | Description                                                                                                                                                 |
| ---------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `from`     | `int`   | L'année de la version précédente.                                                                                                                           |
| `to`       | `int`   | L'année de la version courante.                                                                                                                             |
| `added`    | `array` | Les comptes ajoutés. Chaque élément contient `number`, `label` et `system`.                                                                                 |
| `removed`  | `array` | Les comptes supprimés. Chaque élément contient `number`, `label` et `system` (tels qu'ils étaient dans la version précédente).                               |
| `modified` | `array` | Les comptes dont le libellé et/ou le système a changé. Chaque élément contient `number` et un objet `label` et/ou `system` avec les clés `from` et `to`.    |

### `flat.json`
```js
[
    {
        "number": 1,
        "label": "Comptes de capitaux",
        "system": "minimal",
        "parent": null
    },
    {
        "number": 10,
        "label": "Capital et réserves",
        "system": "minimal",
        "parent": 1
    },
    {
        "number": 101,
        "label": "Capital",
        "system": "minimal",
        "parent": 10
    },
    {
        "number": 1011,
        "label": "Capital souscrit - non appelé",
        "system": "facultatif",
        "parent": 101
    },
    ...
]
```
