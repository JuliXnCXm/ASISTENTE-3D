#!/usr/bin/env python3
"""
sanear_resultados.py
Aplica dsl_api.sanear (quitar argumentos inexistentes del DSL, sin modelo) a todos los
*__lora.py de una carpeta de resultados y escribe una carpeta nueva con las referencias
copiadas, lista para ejecutar_en_blender.py + comparar_rq2.py.

Uso: python3 EVALUATION/sanear_resultados.py EVALUATION/rq2/v3_estimada [salida]
"""
import os, sys, glob, shutil, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsl_api import sanear

src = sys.argv[1].rstrip("/")
dst = sys.argv[2] if len(sys.argv) > 2 else src + "_saneado"
os.makedirs(dst, exist_ok=True)
log = {}
for f in sorted(glob.glob(os.path.join(src, "*.py"))):
    n = os.path.basename(f)
    if n.startswith("_"):
        continue
    code = open(f).read()
    if n.endswith("__lora.py"):
        code, cambios = sanear(code)
        if cambios:
            log[n] = cambios
    open(os.path.join(dst, n), "w").write(code)
json.dump(log, open(os.path.join(dst, "saneado.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(log)} archivos modificados -> {dst}")
for k, v in log.items():
    print(f"  {k}: {v}")
