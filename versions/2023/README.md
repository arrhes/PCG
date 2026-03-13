# Version 2023

## Structure

Deux formats sont disponibles :

- **`nested.json`** — Version hiérarchique avec sous-comptes imbriqués.
- **`flat.json`** — Version à plat avec référence au compte parent.

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
        "label": "Capitaux",
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
                    },
                    ...
                ]
            },
            ...
        ]
    },
    ...
]
```

### `flat.json`
```js
[
    {
        "number": 1,
        "label": "Capitaux",
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
