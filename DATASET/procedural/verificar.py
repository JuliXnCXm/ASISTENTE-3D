#!/usr/bin/env python3
"""
verificar.py — Ejecuta cada candidato del generador en Blender y aplica sus chequeos geométricos
(los mismos del benchmark espacial). Solo pasan los ejemplos que ejecutan Y cumplen todo.

  python3 verificar.py <out_del_generador> [-j 6] [--blender /snap/bin/blender]

Salida: <out>/verificados.jsonl (formato de TRAINING/data: id, task_type, messages + checks/meta)
        <out>/rechazados.jsonl (con el motivo)
"""
import argparse, json, os, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "EVALUATION", "benchmark_espacial"))
from evaluar import Escena, chequear, ejecutar  # noqa: E402
from generador import mensajes  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("-j", type=int, default=6)
    ap.add_argument("--blender", default="/snap/bin/blender")
    a = ap.parse_args()
    cands = [json.loads(l) for l in open(os.path.join(a.dir, "candidatos.jsonl"))]

    def run(c):
        py = os.path.join(a.dir, "py", c["id"] + ".py")
        r = ejecutar(py, a.blender, timeout=300)
        esc = Escena(r)
        if not esc.ok:
            return c, False, f"no ejecuta: {r.get('error')}"
        for ch in c["checks"]:
            ok, msg = chequear(ch, esc, c)
            if not ok:
                return c, False, f"{ch['tipo']}: {msg}"
        return c, True, ""

    with ThreadPoolExecutor(a.j) as ex:
        res = list(ex.map(run, cands))
    motivos = Counter()
    with open(os.path.join(a.dir, "verificados.jsonl"), "w") as fv, \
            open(os.path.join(a.dir, "rechazados.jsonl"), "w") as fr:
        for c, ok, msg in res:
            if ok:
                fv.write(json.dumps(dict(id=c["id"], task_type=c["task_type"], fuente="procedural",
                                         messages=mensajes(c["pedido"], c["codigo"]),
                                         checks=c["checks"], meta=c["meta"]), ensure_ascii=False) + "\n")
            else:
                motivos[msg.split(":")[0]] += 1
                fr.write(json.dumps(dict(id=c["id"], motivo=msg, pedido=c["pedido"][-300:]), ensure_ascii=False) + "\n")
    n_ok = sum(ok for _, ok, _ in res)
    print(f"verificados {n_ok}/{len(res)}  rechazos: {dict(motivos)}")


if __name__ == "__main__":
    main()
