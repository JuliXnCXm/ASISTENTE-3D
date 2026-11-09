# Benchmark de razonamiento espacial (v4, Fase 1)

150 tareas. Cada una tiene un pedido en español y una lista de chequeos geométricos sobre la escena que resulta en Blender. No se compara el código: cualquier forma de construir la escena es válida si la geometría cumple.

## Convención de ejes

Es la misma del DSL `blender_arch`:

| cara | eje |
|---|---|
| frontal / principal / sur | −Y |
| trasera / posterior / norte | +Y |
| izquierda / oeste | −X |
| derecha / este | +X |

Izquierda y derecha se entienden mirando el edificio desde el frente.

## Categorías

| categoría | n | qué mide |
|---|---|---|
| cara | 40 | Un balcón, anexo, marquesina o escalera exterior en una fachada concreta. Además se exige que la fachada opuesta quede libre. |
| cada_piso | 15 | Un balcón repetido en cada piso de una fachada. Se cuentan los niveles distintos. |
| encima | 15 | Un volumen centrado sobre la cubierta, con dimensiones dentro de ±40 %. |
| rotacion | 15 | Un edificio girado θ°, en sentido horario o antihorario. El giro se mide con el rectángulo de área mínima, módulo 90°, con tolerancia de ±5°. |
| separacion | 15 | Un segundo edificio al norte, sur, este u oeste, a g m medidos de fachada a fachada (tolerancia de ±15 % o 1 m) y alineado. |
| forma | 25 | Geometría que el DSL no tiene: techo de una pendiente (dirección y ángulo), planta en L (esquina vacía), torre cilíndrica y volúmenes escalonados con retranqueo. |
| edicion | 25 | Agregar, rotar o mover un elemento partiendo de un código base, con el formato `edit_single` del dataset. |

## Validación del verificador

- **Oráculo:** para cada tarea, `tareas.py` escribe un código que la cumple, en `oraculo/<id>__oraculo.py`. Pasa **150/150**.
- **Control negativo:** también escribe un código casi correcto que viola la relación pedida, en `oraculo/<id>__negativo.py`: la cara opuesta, sin giro, el doble de separación, la pendiente invertida, un rectángulo en vez de la L, un prisma en vez del cilindro o volúmenes sin retranqueo. Pasa **0/150**.

## Uso

```bash
python3 tareas.py                                   # tareas.jsonl + oraculo/
python3 evaluar.py oraculo -j 6                     # validar el verificador
python EVALUATION/generar_con_modelo.py --lora julianG99/qwen2.5-vl-aec-lora-v3 --solo_lora \
   --n_test 0 --sin_generalizacion --tareas EVALUATION/benchmark_espacial/tareas.jsonl \
   --sanear --reparar 2 --out EVALUATION/benchmark_espacial/resultados/v3_sistema
python3 evaluar.py resultados/v3_sistema -j 4       # espacial.md / espacial.json
```

Cuando se usa `--reparar`, el primer intento también se guarda como `<id>__inicial.py`. Así se puede comparar el modelo solo contra el sistema completo con reparación.
