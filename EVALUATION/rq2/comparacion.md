| configuración | ejecuta | error dim. (mediana) | dims ≤20% | F1 categorías | piezas flotando |
|---|---|---|---|---|---|
| v3_estimada | 10/20 | 26% | 4/20 | 0.23 (n=14) | 4 |
| v3_estimada_saneado | 12/20 | 26% | 5/20 | 0.29 (n=14) | 8 |
| v3_estimada_rag | 12/20 | 19% | 7/20 | 0.23 (n=16) | 16 |
| v3_estimada_reparar | 15/20 | 27% | 6/20 | 0.41 (n=14) | 10 |
| v3_estimada_rag_reparar | 13/20 | 19% | 7/20 | 0.26 (n=16) | 16 |
| v3_estimada_reparar_saneado | 17/20 | 27% | 7/20 | 0.47 (n=14) | 14 |

Pareado (las 8 escenas que ejecutan en todas las configuraciones):

| configuración | error dim. (mediana) | F1 categorías |
|---|---|---|
| v3_estimada | 26% | 0.80 (n=4) |
| v3_estimada_saneado | 26% | 0.80 (n=4) |
| v3_estimada_rag | 19% | 0.33 (n=6) |
| v3_estimada_reparar | 26% | 0.80 (n=4) |
| v3_estimada_rag_reparar | 19% | 0.33 (n=6) |
| v3_estimada_reparar_saneado | 26% | 0.80 (n=4) |

Detalle por escena (error dimensional; ✗ = no ejecuta):

| escena | v3_estimada | v3_estimada_saneado | v3_estimada_rag | v3_estimada_reparar | v3_estimada_rag_reparar | v3_estimada_reparar_saneado |
|---|---|---|---|---|---|---|
| test_p0016 | 27% | 27% | 2% | 27% | 2% | 27% |
| test_p0023 | 42% | 42% | ✗ | 42% | ✗ | 42% |
| test_p0048 | 608% | 608% | 1666% | 608% | 1666% | 608% |
| test_p0053 | 0% | 0% | ✗ | 0% | ✗ | 0% |
| test_p0091 | 1% | 1% | 0% / F1 0.00 | 1% | 0% / F1 0.00 | 1% |
| test_p0128 | 49% | 49% | 49% / F1 0.00 | 49% | 49% / F1 0.00 | 49% |
| test_p0944 | 18% / F1 0.97 | 18% / F1 0.97 | 19% / F1 0.97 | 18% / F1 0.97 | 19% / F1 0.97 | 18% / F1 0.97 |
| test_p1926 | 3% / F1 0.84 | 3% / F1 0.84 | 25% / F1 0.17 | 3% / F1 0.84 | 25% / F1 0.17 | 3% / F1 0.84 |
| test_p3052 | 25% / F1 0.61 | 25% / F1 0.61 | 19% / F1 0.44 | 25% / F1 0.61 | 19% / F1 0.44 | 25% / F1 0.61 |
| test_p3247 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| test_p3248 | ✗ | 3% / F1 0.52 | ✗ | ✗ | ✗ | 3% / F1 0.52 |
| test_p3321 | ✗ | ✗ | 30% / F1 0.56 | 18% / F1 0.57 | 30% / F1 0.56 | 18% / F1 0.57 |
| test_p3378 | ✗ | ✗ | 15% / F1 0.36 | 35% / F1 0.60 | 15% / F1 0.36 | 35% / F1 0.60 |
| test_p3385 | ✗ | ✗ | ✗ | 27% / F1 0.37 | ✗ | 27% / F1 0.37 |
| test_p3431 | ✗ | ✗ | 10% / F1 0.50 | ✗ | 10% / F1 0.50 | ✗ |
| test_p3498 | ✗ | ✗ | 184% / F1 0.32 | 113% / F1 0.74 | 184% / F1 0.32 | 113% / F1 0.74 |
| test_p3516 | ✗ | 143% / F1 0.31 | ✗ | ✗ | ✗ | 143% / F1 0.31 |
| test_p3523 | 29% / F1 0.80 | 29% / F1 0.80 | 19% / F1 0.40 | 29% / F1 0.80 | 19% / F1 0.40 | 29% / F1 0.80 |
| test_p3541 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| test_p3551 | ✗ | ✗ | ✗ | 11% / F1 0.29 | 47% / F1 0.46 | 11% / F1 0.29 |
