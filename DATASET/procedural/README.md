# Generador procedural (v4, Fase 2)

Este generador produce ejemplos `(pedido, código)` con diversidad espacial. Todos se verifican en Blender antes de entrar al dataset.

- **Código híbrido.** Se usa el DSL `blender_arch` para lo estándar y `bpy`/`bmesh` para lo que el DSL no tiene: techo de una pendiente, planta en L, cilindro, masas en bpy y pivote de rotación.
- **Posiciones razonadas.** Las posiciones se escriben como variables (`x0`, `y0`, `ancho`, `fondo`) y llevan comentarios con la convención de ejes, por ejemplo `fachada norte (+Y, y = y0 + fondo)`. Así el modelo aprende a razonar la posición en vez de copiar números.
- **Verificación.** Cada ejemplo trae chequeos geométricos, los mismos que usa `EVALUATION/benchmark_espacial/evaluar.py`. Solo se conserva si se ejecuta y pasa todos los chequeos.
- **Sin contaminación del benchmark.** Las redacciones son distintas a las del benchmark, y se descarta cualquier pedido demasiado parecido a una tarea del benchmark.
- **Tareas de edición.** Usan el mismo formato `edit_single` del dataset: `Código base` más `Instrucción`.

```bash
python3 generador.py --n 3000 --seed 2 --out muestras_v1   # candidatos.jsonl + py/
python3 verificar.py muestras_v1 -j 4                       # verificados.jsonl / rechazados.jsonl
```

## Contenido

- **Escenas compuestas:** un edificio principal (DSL, casa o masa en bpy) con 1 a 3 modificadores, cada uno en una cara distinta. Los modificadores posibles son: balcones (en un piso, en todos o alternos, centrados o hacia una esquina), anexo, marquesina, escalera exterior, ático sobre la cubierta, fila de árboles y un segundo edificio en una dirección cardinal con distancia de fachada a fachada. El 15 % de estas escenas se gira completo.
- **Formas fuera del DSL:** techo de una pendiente con dirección de caída, planta en L con la esquina libre indicada, torre cilíndrica y volúmenes escalonados.
