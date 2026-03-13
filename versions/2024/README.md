# Version 2024

## Structure

Trois fichiers sont disponibles :

- **`nested.json`** — Version hiérarchique avec sous-comptes imbriqués.
- **`flat.json`** — Version à plat avec référence au compte parent.
- **`diff.json`** — Différences par rapport à la version précédente (2023).

### Format hiérarchique (`nested.json`)
| Clé        | Type                                 | Description                                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `number`   | `int`                                | Le numéro du compte.                                                                                                                                                                                                                                                                                                                                                           |
| `label`    | `string`                             | Le libellé du compte.                                                                                                                                                                                                                                                                                                                                                          |
| `system`   | `"condensed"` `"base"` `"developed"` | Le système minimal dans lequel s'inscrit le compte. Notez bien que le système développé contient tous les comptes du système de base qui contient lui-même tous les comptes du système abrégé. <br/> `condensed` si le compte est dans le système abrégé. <br/> `base` si le compte est dans le système de base. <br/> `developed` si le compte est dans le système développé. |
| `accounts` | `array`                              | La liste des sous-comptes, reprenant la même structure de manière récursive.                                                                                                                                                                                                                                                                                                   |

### Format à plat (`flat.json`)
| Clé        | Type                                 | Description                                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `number`   | `int`                                | Le numéro du compte.                                                                                                                                                                                                                                                                                                                                                           |
| `label`    | `string`                             | Le libellé du compte.                                                                                                                                                                                                                                                                                                                                                          |
| `system`   | `"condensed"` `"base"` `"developed"` | Le système minimal dans lequel s'inscrit le compte. Notez bien que le système développé contient tous les comptes du système de base qui contient lui-même tous les comptes du système abrégé. <br/> `condensed` si le compte est dans le système abrégé. <br/> `base` si le compte est dans le système de base. <br/> `developed` si le compte est dans le système développé. |
| `parent`   | `int` \| `null`                      | Le numéro du compte parent, ou `null` pour les comptes racines (classes).                                                                                                                                                                                                                                                                                                      |

## Extraits

### `nested.json`
```js
[
    {
        "number": 1,
        "label": "Comptes de capitaux",
        "system": "condensed",
        "accounts": [
            {
                "number": 10,
                "label": "Capital et réserves",
                "system": "base",
                "accounts": [
                    {
                        "number": 101,
                        "label": "Capital",
                        "system": "condensed",
                        "accounts": [
                            {
                                "number": 1011,
                                "label": "Capital souscrit - non appelé",
                                "system": "developed",
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
        "system": "condensed",
        "parent": null
    },
    {
        "number": 10,
        "label": "Capital et réserves",
        "system": "base",
        "parent": 1
    },
    {
        "number": 101,
        "label": "Capital",
        "system": "condensed",
        "parent": 10
    },
    {
        "number": 1011,
        "label": "Capital souscrit - non appelé",
        "system": "developed",
        "parent": 101
    },
    ...
]
```
