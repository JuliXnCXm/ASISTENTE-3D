#!/usr/bin/env python3
"""
evaluar.py — Ejecuta código generado en Blender (headless), extrae la escena y aplica los
chequeos geométricos del benchmark espacial (tareas.jsonl).

  python3 evaluar.py <dir_con_py> [--tareas tareas.jsonl] [--blender /snap/bin/blender] [-j 4]

Los archivos se llaman <id_tarea>__<variante>.py (p.ej. esp_001__lora.py, esp_001__oraculo.py).
Salida: <dir>/espacial.json (detalle) y <dir>/espacial.md (tabla por categoría y variante).
"""
import argparse, glob, json, math, os, subprocess, sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DSL = os.path.join(os.path.dirname(os.path.dirname(HERE)), "DSL", "blender")
H = 3.0

RUNNER = r'''
import sys, json, math, random, traceback
sys.path.insert(0, DSL_PATH)
import bpy
from mathutils import Vector
res = {"ok": False, "error": None}
try:
    code = open(CODE_PATH, encoding="utf-8").read()
    exec(compile(code, CODE_PATH, "exec"), {"__name__": "__main__"})
    res["ok"] = True
except BaseException as e:
    tb = traceback.format_exc().strip().splitlines()
    res["error"] = (tb[-1] if tb else repr(e))[:300]
try:
    bpy.context.view_layer.update()
    def top(o):
        # sube por la jerarquía, pero se detiene ante un Empty sin categoría (pivote del usuario
        # que agrupa varios objetos): así un giro de 'todo el conjunto' no fusiona los edificios
        while o.parent and (o.parent.type == 'MESH' or o.parent.get("arch_categoria")):
            o = o.parent
        return o
    def cat(o):
        while o:
            c = o.get("arch_categoria")
            if c: return str(c)
            o = o.parent
        return None
    meshes, grupos = [], {}
    for o in bpy.context.scene.objects:
        if o.type != 'MESH' or not o.visible_get():
            continue
        M = o.matrix_world
        vs = [M @ v.co for v in o.data.vertices]
        if not vs:
            continue
        bb = [min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs),
              max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)]
        c = cat(o)
        terreno = c == "terreno" or ((bb[5]-bb[2]) < 0.6 and bb[5] <= 0.15 and (bb[3]-bb[0])*(bb[4]-bb[1]) >= 100)
        # caras superiores inclinadas (para techos): área por orientación de caída
        incl, hz = {}, []
        N = M.to_3x3().inverted_safe().transposed()
        for p in o.data.polygons:
            n = (N @ p.normal).normalized()
            if n.z > 0.95 and len(hz) < 40 and p.area > 0.05:  # huella real (caras horizontales)
                hz.append([(round((M @ o.data.vertices[i].co).x, 3), round((M @ o.data.vertices[i].co).y, 3)) for i in p.vertices])
            if n.z <= 0.05: continue
            pts = [M @ o.data.vertices[i].co for i in p.vertices]
            a = 0.0
            for i in range(1, len(pts) - 1):
                a += ((pts[i] - pts[0]).cross(pts[i+1] - pts[0])).length / 2
            if a < 0.5: continue
            s = math.degrees(math.acos(max(-1, min(1, n.z))))
            if 3 < s < 75:
                k = ("derecha" if n.x > 0 else "izquierda") if abs(n.x) > abs(n.y) else ("trasera" if n.y > 0 else "frontal")
                d = incl.setdefault(k, [0.0, 0.0]); d[0] += a; d[1] += a * s
        g = top(o).name
        meshes.append(dict(n=o.name, g=g, c=c, bb=[round(x, 3) for x in bb], t=terreno, hz=hz,
                           incl={k: [round(v[0], 2), round(v[1] / v[0], 2)] for k, v in incl.items()}))
        if not terreno:
            gp = grupos.setdefault(g, [])
            gp.extend((v.x, v.y) for v in (vs if len(vs) <= 400 else random.sample(vs, 400)))
    def hull(p):
        p = sorted(set((round(x, 3), round(y, 3)) for x, y in p))
        if len(p) < 3: return p
        def cr(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        lo, up = [], []
        for q in p:
            while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0: lo.pop()
            lo.append(q)
        for q in reversed(p):
            while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0: up.pop()
            up.append(q)
        return lo[:-1] + up[:-1]
    def area(h):
        return abs(sum(h[i][0]*h[(i+1)%len(h)][1] - h[(i+1)%len(h)][0]*h[i][1] for i in range(len(h)))) / 2
    def rect(h):
        """Rectángulo de área mínima (orientado) sobre el casco convexo: (yaw en [0,90), lado_a, lado_b)."""
        best = None
        for d in range(0, 90):
            a = math.radians(d); c, s = math.cos(a), math.sin(a)
            xs = [x*c + y*s for x, y in h]; ys = [-x*s + y*c for x, y in h]
            w, l = max(xs)-min(xs), max(ys)-min(ys)
            if best is None or w*l < best[1]*best[2] - 1e-9:
                best = (d, w, l)
        return best
    gout = {}
    todos = []
    for g, pts in grupos.items():
        todos.extend(pts)
        h = hull(pts)
        if len(h) < 3: continue
        yaw, a, b = rect(h)
        gout[g] = dict(yaw=yaw, a=round(a, 3), b=round(b, 3), hull=round(area(h), 2))
    h = hull(todos) if len(todos) >= 3 else []
    res.update(meshes=meshes, grupos=gout, hull_total=round(area(h), 2) if len(h) >= 3 else 0)
except BaseException as e:
    res["error_escena"] = repr(e)[:300]
open(JSON_PATH, "w").write(json.dumps(res))
'''


def ejecutar(py, blender, timeout=240):
    py = os.path.abspath(py)
    base = py[:-3]
    out = base + ".escena.json"
    runner = base + ".runner_tmp.py"
    with open(runner, "w") as f:
        f.write(f"DSL_PATH={DSL!r}\nCODE_PATH={os.path.abspath(py)!r}\nJSON_PATH={os.path.abspath(out)!r}\n" + RUNNER)
    if os.path.exists(out):
        os.remove(out)
    try:
        subprocess.run([blender, "-b", "--factory-startup", "-P", runner], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=timeout, cwd=os.path.dirname(os.path.abspath(py)))
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout {timeout}s"}
    finally:
        if os.path.exists(runner):
            os.remove(runner)
    if not os.path.exists(out):
        return {"ok": False, "error": "Blender terminó sin reporte (crash)"}
    return json.load(open(out))


# ====================================================================== chequeos
def union(bbs):
    return [min(b[0] for b in bbs), min(b[1] for b in bbs), min(b[2] for b in bbs),
            max(b[3] for b in bbs), max(b[4] for b in bbs), max(b[5] for b in bbs)]


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-6)


class Escena:
    def __init__(self, r):
        self.ok = r.get("ok", False)
        self.meshes = [m for m in r.get("meshes", []) if not m["t"]]
        self.grupos = r.get("grupos", {})
        self.hull_total = r.get("hull_total", 0)
        self.por_grupo = defaultdict(list)
        for m in self.meshes:
            self.por_grupo[m["g"]].append(m)

    def grupo_bb(self, g):
        ms = self.por_grupo[g]
        muros = [m["bb"] for m in ms if m["c"] == "muro"]
        return union(muros or [m["bb"] for m in ms])

    def buscar(self, spec, excluir=()):
        """Grupo cuyo rectángulo orientado y altura se parecen a spec (ancho, fondo, alto)."""
        mejor = None
        for g, info in self.grupos.items():
            if g in excluir or g not in self.por_grupo:
                continue
            a, b = sorted([info["a"], info["b"]])
            A_, B_ = sorted([spec["ancho"], spec["fondo"]])
            e = max(rel(a, A_), rel(b, B_))
            if spec.get("alto"):
                bb = union([m["bb"] for m in self.por_grupo[g]])
                e = max(e, rel(bb[5] - bb[2], spec["alto"]))
            if mejor is None or e < mejor[0]:
                mejor = (e, g)
        return mejor[1] if mejor and mejor[0] <= 0.35 else None

    def total_bb(self):
        return union([m["bb"] for m in self.meshes]) if self.meshes else None


def lado(m, core, cara, vuelo_min, z_min, z_max):
    b, c = m["bb"], core
    if not (z_min <= b[2] <= z_max):
        return False
    if cara in ("frontal", "trasera"):
        if not (b[3] > c[0] + 0.1 and b[0] < c[3] - 0.1):
            return False
        if cara == "frontal":
            return c[1] - b[1] >= vuelo_min and b[4] >= c[1] - 0.6 and b[1] >= c[1] - 8
        return b[4] - c[4] >= vuelo_min and b[1] <= c[4] + 0.6 and b[4] <= c[4] + 8
    if not (b[4] > c[1] + 0.1 and b[1] < c[4] - 0.1):
        return False
    if cara == "izquierda":
        return c[0] - b[0] >= vuelo_min and b[3] >= c[0] - 0.6 and b[0] >= c[0] - 8
    return b[3] - c[3] >= vuelo_min and b[0] <= c[3] + 0.6 and b[3] <= c[3] + 8


def chequear(ch, esc, t):
    tipo = ch["tipo"]
    spec = t.get("edificio")
    core_g = esc.buscar(spec) if spec else None
    core = esc.grupo_bb(core_g) if core_g else None
    if tipo in ("dims", "cara", "no_cara", "encima", "rotacion", "separacion", "pendiente") and core is None:
        return False, "edificio principal no encontrado (dimensiones)"
    if tipo == "dims":
        return True, f"grupo '{core_g}'"
    if tipo in ("cara", "no_cara"):
        ms = [m for m in esc.meshes if lado(m, core, ch["cara"], ch["vuelo_min"], ch["z_min"], ch["z_max"])]
        if tipo == "no_cara":
            return (not ms), f"{len(ms)} piezas en la cara {ch['cara']}"
        if not ms:
            return False, f"nada sobresale de la cara {ch['cara']}"
        zs = sorted(m["bb"][2] for m in ms)  # niveles = alturas de apoyo distintas (separadas > 1 m)
        niveles = [z for i, z in enumerate(zs) if i == 0 or z - zs[i - 1] > 1.0]
        if len(niveles) < ch.get("niveles_min", 1):
            return False, f"{len(niveles)} niveles < {ch['niveles_min']}"
        return True, f"{len(ms)} piezas, {len(niveles)} niveles"
    if tipo == "encima":
        zc = core[5]
        cx, cy = (core[0] + core[3]) / 2, (core[1] + core[4]) / 2
        ms = [m for m in esc.meshes if m["bb"][2] >= zc - 0.1 and m["bb"][5] - m["bb"][2] >= 0.5
              and core[0] < (m["bb"][0] + m["bb"][3]) / 2 < core[3] and core[1] < (m["bb"][1] + m["bb"][4]) / 2 < core[4]]
        if not ms:
            return False, "nada sobre la cubierta"
        u = union([m["bb"] for m in ms])
        a, b = sorted([u[3] - u[0], u[4] - u[1]])
        A_, B_ = sorted([ch["ancho"], ch["fondo"]])
        okd = rel(a, A_) <= 0.4 and rel(b, B_) <= 0.4 and rel(u[5] - u[2], ch["alto"]) <= 0.4
        cen = abs((u[0] + u[3]) / 2 - cx) <= 0.2 * (core[3] - core[0]) and abs((u[1] + u[4]) / 2 - cy) <= 0.2 * (core[4] - core[1])
        return okd and cen, f"volumen {a:.1f}x{b:.1f}x{u[5] - u[2]:.1f} centrado={cen}"
    if tipo == "rotacion":
        yaw = esc.grupos[core_g]["yaw"]
        d = (yaw - ch["grados"]) % 90
        d = min(d, 90 - d)
        return d <= ch["tol"], f"giro medido {yaw}° (esperado {ch['grados'] % 90}° mód 90)"
    if tipo == "separacion":
        og = esc.buscar(ch["otro"], excluir=(core_g,))
        if not og:
            return False, "segundo edificio no encontrado"
        o = esc.grupo_bb(og)
        c = ch["cara"]
        gap = {"derecha": o[0] - core[3], "izquierda": core[0] - o[3],
               "trasera": o[1] - core[4], "frontal": core[1] - o[4]}[c]
        if c in ("derecha", "izquierda"):
            al = core[1] - 1 <= (o[1] + o[4]) / 2 <= core[4] + 1
        else:
            al = core[0] - 1 <= (o[0] + o[3]) / 2 <= core[3] + 1
        okg = abs(gap - ch["gap"]) <= max(1.0, 0.15 * ch["gap"])
        return okg and al, f"separación medida {gap:.1f} m (esperada {ch['gap']}), alineado={al}"
    if tipo == "pendiente":
        area_min = 0.4 * spec["ancho"] * spec["fondo"]
        for m in esc.meshes:
            tot = sum(v[0] for v in m["incl"].values())
            if tot < area_min:
                continue
            dom = max(m["incl"], key=lambda k: m["incl"][k][0])
            frac = m["incl"][dom][0] / tot
            ang = m["incl"][dom][1]
            if ch["aguas"] == 1 and frac < 0.85:
                continue
            return (dom == ch["cae"] and abs(ang - ch["grados"]) <= ch["tol"],
                    f"techo cae hacia {dom} ({frac:.0%}) a {ang:.0f}°")
        return False, "no hay techo inclinado de una pendiente"
    tb = esc.total_bb()
    if tb is None:
        return False, "escena vacía"
    if tipo == "dims_total":
        dx, dy, dz = tb[3] - tb[0], tb[4] - tb[1], tb[5] - tb[2]
        ok = rel(dx, ch["ancho"]) <= 0.15 and rel(dy, ch["fondo"]) <= 0.15 and rel(dz, ch["alto"]) <= 0.2
        return ok, f"total {dx:.1f}x{dy:.1f}x{dz:.1f}"
    if tipo == "huella":
        def en_poligono(x, y, pol):
            dentro_, n = False, len(pol)
            for i in range(n):
                (x1, y1), (x2, y2) = pol[i], pol[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                    dentro_ = not dentro_
            return dentro_

        def dentro(fx, fy):
            x, y = tb[0] + fx * (tb[3] - tb[0]), tb[1] + fy * (tb[4] - tb[1])
            return any(m["bb"][0] <= x <= m["bb"][3] and m["bb"][1] <= y <= m["bb"][4]
                       and any(en_poligono(x, y, p) for p in m.get("hz", [])) for m in esc.meshes)
        oc = all(dentro(*p) for p in ch["ocupados"])
        va = not any(dentro(*p) for p in ch["vacios"])
        return oc and va, f"brazos ocupados={oc}, esquina vacía={va}"
    if tipo == "redondo":
        r = esc.hull_total / max((tb[3] - tb[0]) * (tb[4] - tb[1]), 1e-6)
        return r <= 0.9, f"casco/bbox = {r:.2f}"
    if tipo == "escalonado":
        k, s = ch["niveles"], ch["retiro"]
        hv = (tb[5] - tb[2]) / k
        prev, det = None, []
        for j in range(k):
            z = tb[2] + (j + 0.5) * hv
            ms = [m["bb"] for m in esc.meshes if m["bb"][2] <= z <= m["bb"][5]]
            if not ms:
                return False, f"nivel {j + 1} vacío"
            u = union(ms)
            if prev:
                ret = min(u[0] - prev[0], u[1] - prev[1], prev[3] - u[3], prev[4] - u[4])
                det.append(round(ret, 1))
                if ret < 0.5 * s:
                    return False, f"retiros {det}"
            prev = u
        return True, f"retiros {det}"
    return False, f"chequeo desconocido {tipo}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--tareas", default=os.path.join(HERE, "tareas.jsonl"))
    ap.add_argument("--blender", default="/snap/bin/blender")
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--reusar", action="store_true", help="no re-ejecutar si ya existe .escena.json")
    a = ap.parse_args()
    tareas = {t["id"]: t for t in map(json.loads, open(a.tareas))}
    files = sorted(f for f in glob.glob(os.path.join(a.dir, "esp_*__*.py")))

    def run(f):
        js = f[:-3] + ".escena.json"
        if a.reusar and os.path.exists(js):
            return f, json.load(open(js))
        return f, ejecutar(f, a.blender)

    with ThreadPoolExecutor(a.j) as ex:
        escenas = dict(ex.map(run, files))
    out, tabla = {}, defaultdict(lambda: [0, 0, 0])
    for f in files:
        n = os.path.basename(f)[:-3]
        tid, var = n.split("__")
        t = tareas.get(tid)
        if not t:
            continue
        r = escenas[f]
        esc = Escena(r)
        det = []
        if esc.ok:
            for ch in t["checks"]:
                ok, msg = chequear(ch, esc, t)
                det.append(dict(tipo=ch["tipo"], ok=ok, msg=msg))
        paso = esc.ok and all(d["ok"] for d in det)
        out[n] = dict(categoria=t["categoria"], subtipo=t["subtipo"], variante=var, ejecuta=esc.ok,
                      error=r.get("error"), paso=paso, checks=det)
        for k in (t["categoria"], "TOTAL"):
            tabla[(var, k)][0] += 1
            tabla[(var, k)][1] += esc.ok
            tabla[(var, k)][2] += paso
        print(f"{'PASA' if paso else ('ERR ' if not esc.ok else 'no  ')} {n:28s} "
              + ("; ".join(f"{d['tipo']}:{'✓' if d['ok'] else '✗'} {d['msg']}" for d in det) or str(r.get('error'))[:120]),
              flush=True)
    json.dump(out, open(os.path.join(a.dir, "espacial.json"), "w"), ensure_ascii=False, indent=1)
    vars_ = sorted({v for v, _ in tabla})
    cats = ["cara", "cada_piso", "encima", "rotacion", "separacion", "forma", "edicion", "TOTAL"]
    md = ["| categoría | " + " | ".join(f"{v} ejecuta | {v} pasa" for v in vars_) + " |",
          "|---|" + "---|---|" * len(vars_)]
    for c in cats:
        fila = [c]
        for v in vars_:
            n, e, p = tabla.get((v, c), (0, 0, 0))
            fila += [f"{e}/{n}", f"**{p}/{n}**"]
        md.append("| " + " | ".join(fila) + " |")
    open(os.path.join(a.dir, "espacial.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
