| configuración | ejecuta | error dim. (mediana) | dims ≤20% | F1 categorías | piezas flotando |
|---|---|---|---|---|---|
| v2_rgb_cam | 9/20 | 31% | 3/20 | 0.16 (n=15) | 7 |
| v3_sin_prof | 12/20 | 29% | 5/20 | 0.33 (n=14) | 6 |
| v3_estimada | 10/20 | 26% | 4/20 | 0.23 (n=14) | 4 |
| v3_gt | 11/20 | 34% | 4/20 | 0.26 (n=14) | 3 |

Pareado (las 7 escenas que ejecutan en todas las configuraciones):

| configuración | error dim. (mediana) | F1 categorías |
|---|---|---|
| v2_rgb_cam | 30% | 0.94 (n=2) |
| v3_sin_prof | 18% | 0.88 (n=2) |
| v3_estimada | 27% | 0.88 (n=2) |
| v3_gt | 27% | 0.88 (n=2) |

Detalle por escena (error dimensional; ✗ = no ejecuta):

| escena | v2_rgb_cam | v3_sin_prof | v3_estimada | v3_gt |
|---|---|---|---|---|
| test_p0016 | 0% | 3% | 27% | 0% |
| test_p0023 | 55% | 33% | 42% | 50% |
| test_p0048 | 46% / F1 0.00 | ✗ | 608% | 401% |
| test_p0053 | 0% | 1% | 0% | 4% |
| test_p0091 | 31% | 1% | 1% | 50% |
| test_p0128 | 49% | 49% | 49% | 43% |
| test_p0944 | 19% / F1 0.97 | 18% / F1 0.97 | 18% / F1 0.97 | 18% / F1 0.97 |
| test_p1926 | ✗ | 7% / F1 0.89 | 3% / F1 0.84 | 3% / F1 0.84 |
| test_p3052 | 31% / F1 0.51 | ✗ | 25% / F1 0.61 | ✗ |
| test_p3247 | ✗ | ✗ | ✗ | ✗ |
| test_p3248 | ✗ | ✗ | ✗ | ✗ |
| test_p3321 | ✗ | ✗ | ✗ | ✗ |
| test_p3378 | ✗ | ✗ | ✗ | ✗ |
| test_p3385 | ✗ | ✗ | ✗ | 36% / F1 0.59 |
| test_p3431 | ✗ | 54% / F1 0.62 | ✗ | ✗ |
| test_p3498 | ✗ | 216% / F1 0.55 | ✗ | 34% / F1 0.40 |
| test_p3516 | ✗ | 235% / F1 0.11 | ✗ | ✗ |
| test_p3523 | 30% / F1 0.91 | 26% / F1 0.80 | 29% / F1 0.80 | 27% / F1 0.80 |
| test_p3541 | ✗ | ✗ | ✗ | ✗ |
| test_p3551 | ✗ | 31% / F1 0.64 | ✗ | ✗ |
