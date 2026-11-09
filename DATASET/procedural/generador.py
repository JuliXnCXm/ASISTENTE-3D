#!/usr/bin/env python3
"""
generador.py — Generador procedural de ejemplos (pedido, código) con diversidad espacial (v4, Fase 2).

Cada escena se arma desde parámetros aleatorios y produce:
  - código Python HÍBRIDO legible: DSL blender_arch para lo estándar y bpy/bmesh para la geometría
    que el DSL no tiene. Las posiciones se expresan con variables (x0, y0, ancho, fondo...) y
    comentarios que explicitan la convención de ejes ("fachada norte = +Y, y = y0 + fondo"),
    para que el modelo aprenda a RAZONAR la posición y no a copiar números.
  - un pedido en español (plantillas con sinónimos; redacciones distintas a las del benchmark)
  - chequeos geométricos (mismo formato que EVALUATION/benchmark_espacial) para verificar
  - opcionalmente, una tarea de edición (código base + instrucción -> código nuevo)

Convención (la del DSL): frontal/sur = -Y, trasera/norte = +Y, izquierda/oeste = -X, derecha/este = +X.

Uso:
  python3 generador.py --n 500 --seed 1 --out muestras_v1      # escribe <out>/candidatos.jsonl + py/
  python3 verificar.py muestras_v1 -j 6                          # ejecuta en Blender y filtra
"""
import argparse, difflib, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BENCH = os.path.join(ROOT, "EVALUATION", "benchmark_espacial", "tareas.jsonl")

SYSTEM = ("Eres un experto en desarrollo arquitectónico CAD procedural-paramétrico.\n"
          "Tu tarea es generar código Python ejecutable en Blender usando el DSL 'blender_arch' y la API 'bpy'.\n"
          "Escribe únicamente código Python autocontenido, sin markdown adicional ni explicaciones.")

CARAS = ["frontal", "trasera", "izquierda", "derecha"]
OPUESTA = {"frontal": "trasera", "trasera": "frontal", "izquierda": "derecha", "derecha": "izquierda"}
CARDINAL = {"frontal": "sur", "trasera": "norte", "izquierda": "oeste", "derecha": "este"}
EJE = {"frontal": "-Y, y = y0", "trasera": "+Y, y = y0 + fondo",
       "izquierda": "-X, x = x0", "derecha": "+X, x = x0 + ancho"}
# redacciones del generador (el benchmark usa otras: 'la fachada frontal', 'el costado izquierdo', ...)
NOMBRE_CARA = {
    "frontal": ["el frente", "la fachada de la entrada", "la cara sur", "la fachada que da al sur", "la fachada delantera"],
    "trasera": ["la parte trasera", "la cara norte", "la fachada que da al norte", "la fachada de atrás", "el lado posterior"],
    "izquierda": ["el lado izquierdo", "la cara oeste", "la fachada que da al oeste", "el flanco izquierdo", "el costado oeste"],
    "derecha": ["el lado derecho", "la cara este", "la fachada que da al este", "el flanco derecho", "el costado este"],
}
VERBOS = ["Diseña", "Modela", "Genera", "Construye", "Haz", "Quiero", "Necesito"]
ORD = ["planta baja", "primer piso", "segundo piso", "tercer piso", "cuarto piso", "quinto piso",
       "sexto piso", "séptimo piso", "octavo piso"]
CAB = "import blender_arch as A\nimport bpy\nimport bmesh\nimport math\n\nA.limpiar_escena()\n"


def g(x):
    return f"{round(x, 3):g}"


class Escena:
    """Acumula secciones de código, cláusulas del pedido y chequeos."""

    def __init__(self, r: random.Random):
        self.r = r
        self.secciones, self.clausulas, self.checks = [], [], []
        self.edificio = None   # spec del edificio principal para los chequeos
        self.rotada = False
        self.meta = {}

    def codigo(self):
        return CAB + "\n" + "\n".join(s.rstrip() + "\n" for s in self.secciones)

    def pedido(self):
        r = self.r
        verbo = r.choice(VERBOS)
        cuerpo = self.clausulas[0]
        resto = " ".join(self.clausulas[1:])
        return gramatica(f"{verbo} {cuerpo}. {resto}".strip())


# ====================================================================== edificio principal
def edificio_principal(e: Escena, estilo):
    r = e.r
    W = r.choice([8, 9, 10, 11, 12, 13, 15, 16, 18, 22, 24])
    D = r.choice([7, 8, 9, 10, 11, 13, 15, 16])
    Hp = r.choice([2.8, 3.0, 3.2, 3.5])
    x0, y0 = r.choice([(0, 0), (0, 0), (-W / 2, -D / 2), (r.randint(-10, 10), r.randint(-10, 10))])
    e.meta.update(W=W, D=D, Hp=Hp, x0=x0, y0=y0, estilo=estilo)
    if estilo == "casa":
        P = r.randint(1, 2)
        tej = r.random() < 0.6
        e.secciones.append(
            f"# --- Casa principal: esquina suroeste en (x0, y0); fachada frontal = sur (-Y) ---\n"
            f"ancho, fondo, alto_piso, pisos = {g(W)}, {g(D)}, {g(Hp)}, {P}\n"
            f"x0, y0 = {g(x0)}, {g(y0)}\n"
            f"casa = A.crear_casa_n_pisos('Casa', pisos=pisos, ancho=ancho, fondo=fondo, alto_piso=alto_piso, "
            f"con_tejado={tej}, origen=(x0, y0, 0))\n")
        e.clausulas.append(r.choice([
            f"una casa de {P} piso{'s' if P > 1 else ''} de {g(W)} m de ancho por {g(D)} m de fondo",
            f"una vivienda de {P} planta{'s' if P > 1 else ''} con planta de {g(W)} x {g(D)} m"]) +
            (f", altura libre por piso de {g(Hp)} m" if r.random() < 0.7 else f" (pisos de {g(Hp)} m)") +
            (" y tejado a dos aguas" if tej else " y cubierta plana"))
        e.edificio = dict(ancho=W, fondo=D, alto=None)
        e.meta["P"], e.meta["var"] = P, "casa"
    elif estilo == "bpy":
        P = r.randint(2, 8)
        e.secciones.append(
            f"# --- Volumen principal en bpy: masa + losas de entrepiso salientes ---\n"
            f"ancho, fondo, alto_piso, pisos = {g(W)}, {g(D)}, {g(Hp)}, {P}\n"
            f"x0, y0 = {g(x0)}, {g(y0)}  # esquina suroeste\n"
            f"alto = pisos * alto_piso\n"
            f"bpy.ops.mesh.primitive_cube_add(size=1, location=(x0 + ancho / 2, y0 + fondo / 2, alto / 2))\n"
            f"masa = bpy.context.active_object\n"
            f"masa.name = 'Masa'\n"
            f"masa.scale = (ancho, fondo, alto)\n"
            f"bpy.ops.object.transform_apply(scale=True)\n"
            f"for p in range(1, pisos + 1):\n"
            f"    bpy.ops.mesh.primitive_cube_add(size=1, location=(x0 + ancho / 2, y0 + fondo / 2, p * alto_piso))\n"
            f"    losa = bpy.context.active_object\n"
            f"    losa.name = f'Cornisa_{{p}}'\n"
            f"    losa.scale = (ancho + 0.3, fondo + 0.3, 0.2)\n"
            f"    losa.parent = masa\n")
        e.clausulas.append(r.choice([
            f"un bloque de {P} pisos de {g(W)} x {g(D)} m con cornisas marcando cada piso",
            f"un edificio de {P} niveles, {g(W)} m de frente y {g(D)} m de fondo, con losas que sobresalen un poco en cada piso"]) +
            f", altura de piso {g(Hp)} m")
        e.edificio = dict(ancho=W + 0.3, fondo=D + 0.3, alto=P * Hp)
        e.meta["P"], e.meta["var"] = P, "masa"
    else:
        P = r.randint(2, 9)
        e.secciones.append(
            f"# --- Edificio principal: esquina suroeste en (x0, y0); fachada frontal = sur (-Y) ---\n"
            f"ancho, fondo, alto_piso, pisos = {g(W)}, {g(D)}, {g(Hp)}, {P}\n"
            f"x0, y0 = {g(x0)}, {g(y0)}\n"
            f"edificio = A.crear_edificio_n_pisos('Edificio', pisos=pisos, ancho=ancho, fondo=fondo, "
            f"alto_piso=alto_piso, origen=(x0, y0, 0))\n")
        e.clausulas.append(r.choice([
            f"un edificio de {P} pisos de {g(W)} x {g(D)} metros",
            f"un bloque residencial de {P} plantas, {g(W)} m de ancho y {g(D)} m de profundidad",
            f"un edificio de oficinas de {P} niveles con planta de {g(W)} por {g(D)} m"]) +
            f" y altura de piso de {g(Hp)} m")
        e.edificio = dict(ancho=W, fondo=D, alto=P * Hp)
        e.meta["P"], e.meta["var"] = P, "edificio"
    if (x0, y0) != (0, 0) and r.random() < 0.5:
        e.clausulas[-1] += f", con la esquina suroeste en ({g(x0)}, {g(y0)})"
    elif (x0, y0) == (-W / 2, -D / 2) and r.random() < 0.7:
        e.clausulas[-1] += ", centrado en el origen"


# ====================================================================== geometría por cara
def pos_cara(cara, u, a, b):
    """Expresiones (origen_x, origen_y, tam_x, tam_y) de un rectángulo de largo a (a lo largo de la
    fachada, centrado en la fracción u) y vuelo b, pegado por fuera a 'cara'."""
    if cara == "frontal":
        return f"x0 + {g(u)} * ancho - {g(a)} / 2", f"y0 - {g(b)}", g(a), g(b)
    if cara == "trasera":
        return f"x0 + {g(u)} * ancho - {g(a)} / 2", "y0 + fondo", g(a), g(b)
    if cara == "izquierda":
        return f"x0 - {g(b)}", f"y0 + {g(u)} * fondo - {g(a)} / 2", g(b), g(a)
    return "x0 + ancho", f"y0 + {g(u)} * fondo - {g(a)} / 2", g(b), g(a)


def baranda_cara(cara, nombre, ox, oy, a, b, z):
    """Baranda en el borde exterior de una losa en voladizo (la baranda del DSL corre en +X)."""
    if cara == "frontal":
        return f"A.crear_baranda_lineal('{nombre}', largo={g(a)}, altura=1.1, origen=({ox}, {oy}, {z} + 0.2))\n"
    if cara == "trasera":
        return f"A.crear_baranda_lineal('{nombre}', largo={g(a)}, altura=1.1, origen=({ox}, {oy} + {g(b)} - 0.08, {z} + 0.2))\n"
    x = f"{ox} + 0.08" if cara == "izquierda" else f"{ox} + {g(b)}"
    return (f"bar = A.crear_baranda_lineal('{nombre}', largo={g(a)}, altura=1.1, origen=({x}, {oy}, {z} + 0.2))\n"
            f"bar.rotation_euler.z = math.pi / 2  # girar 90° para que corra a lo largo de Y\n")


def balcones(e: Escena, cara, modo):
    r, P, Hp = e.r, e.meta["P"], e.meta["Hp"]
    if P < 2:
        return False
    a, b = r.choice([2.5, 3, 3.5, 4]), r.choice([1.2, 1.5, 1.8, 2])
    nc = r.choice(NOMBRE_CARA[cara])
    if modo == "uno":
        k = r.randint(1, P - 1)
        pisos_txt, rango = f"en el {ORD[k]}", f"[{k}]"
        niveles = 1
        zs = (k * Hp - 0.6, k * Hp + 0.6)
    elif modo == "todos":
        pisos_txt, rango = "en todos los pisos superiores", "range(1, pisos)"
        niveles = P - 1
        zs = (Hp - 0.6, P * Hp)
    else:  # alternos
        if P < 4:
            return False
        pisos_txt, rango = "en los pisos pares (2.º, 4.º, ...)", "range(2, pisos, 2)"
        niveles = len(range(2, P, 2))
        zs = (2 * Hp - 0.6, P * Hp)
    u = r.choice([0.5, 0.5, 0.3, 0.7])
    ox, oy, sx, sy = pos_cara(cara, u, a, b)
    pos_txt = "" if u == 0.5 else (" hacia la esquina izquierda" if (u < 0.5) == (cara in ("frontal", "izquierda")) else " hacia la esquina derecha")
    e.secciones.append(
        f"# --- Balcones en la fachada {CARDINAL[cara]} ({EJE[cara]}); vuelo hacia afuera ---\n"
        f"largo_b, vuelo_b = {g(a)}, {g(b)}\n"
        f"for p in {rango}:\n"
        f"    z = p * alto_piso\n"
        f"    A.crear_losa_rectangular(f'Balcon_{CARDINAL[cara]}_{{p}}', ancho={sx}, fondo={sy}, espesor=0.2, "
        f"origen=({ox}, {oy}, z))\n" +
        "    " + baranda_cara(cara, f"Baranda_{CARDINAL[cara]}_{{p}}", ox, oy, a, b, "z")
        .replace("('Baranda", "(f'Baranda").replace("\nbar.", "\n    bar."))
    e.clausulas.append(r.choice([
        (f"Agrega un balcón en voladizo de {g(a)} x {g(b)} m con baranda en {nc}{pos_txt}, {pisos_txt}." if modo == "uno" else
         f"Agrega balcones en voladizo de {g(a)} x {g(b)} m con baranda en {nc}{pos_txt}, {pisos_txt}."),
        f"{pisos_txt.capitalize()}, pon un balcón de {g(a)} m de largo y {g(b)} m de vuelo con baranda en {nc}{pos_txt}.",
    ]))
    e.checks.append(dict(tipo="cara", cara=cara, vuelo_min=0.6 * b, z_min=zs[0], z_max=zs[1], niveles_min=niveles))
    return True


def anexo(e: Escena, cara):
    r = e.r
    a, b, Pa = r.choice([3, 4, 5, 6]), r.choice([2.5, 3, 4]), 1
    ox, oy, sx, sy = pos_cara(cara, 0.5, a, b)
    nc = r.choice(NOMBRE_CARA[cara])
    e.secciones.append(
        f"# --- Anexo de un piso adosado a la fachada {CARDINAL[cara]} ({EJE[cara]}) ---\n"
        f"anexo = A.crear_edificio_n_pisos('Anexo', pisos=1, ancho={sx}, fondo={sy}, alto_piso=alto_piso, "
        f"origen=({ox}, {oy}, 0))\n")
    e.clausulas.append(r.choice([
        f"Adosa a {nc} un anexo de una planta de {g(a)} m de largo por {g(b)} m de profundidad.",
        f"Añade en {nc} un volumen bajo de un piso ({g(a)} x {g(b)} m) pegado a la fachada."]))
    e.checks.append(dict(tipo="cara", cara=cara, vuelo_min=0.6 * b, z_min=-0.3, z_max=0.6))
    return True


def marquesina(e: Escena, cara):
    r = e.r
    a, b, z = r.choice([3, 4, 5]), r.choice([1.2, 1.5, 2]), r.choice([2.6, 3.0])
    z = min(z, e.meta["Hp"])
    ox, oy, sx, sy = pos_cara(cara, 0.5, a, b)
    nc = r.choice(NOMBRE_CARA[cara])
    e.secciones.append(
        f"# --- Marquesina sobre la entrada de la fachada {CARDINAL[cara]} ({EJE[cara]}) ---\n"
        f"A.crear_losa_rectangular('Marquesina', ancho={sx}, fondo={sy}, espesor=0.15, origen=({ox}, {oy}, {g(z)}))\n")
    e.clausulas.append(f"Sobre el acceso de {nc}, una marquesina de {g(a)} m de ancho que vuele {g(b)} m, a {g(z)} m de altura.")
    e.checks.append(dict(tipo="cara", cara=cara, vuelo_min=0.6 * b, z_min=z - 0.6, z_max=z + 0.6))
    return True


def escalera(e: Escena, cara):
    r, Hp = e.r, e.meta["Hp"]
    n = round(Hp / 0.175)
    cont, huella = Hp / n, 0.28
    largo = n * huella
    nc = r.choice(NOMBRE_CARA[cara])
    if cara in ("frontal", "trasera"):
        if largo > e.meta["W"]:
            return False
        y = "y0 - 1.3" if cara == "frontal" else "y0 + fondo + 0.1"
        cod = (f"A.crear_escalera_recta('EscaleraExterior', huella={huella}, contrahuella={cont:.4f}, ancho=1.1, "
               f"num_peldanos={n}, origen=(x0 + ancho / 2 - {g(largo)} / 2, {y}, 0))  # sube en +X\n")
    else:
        if largo > e.meta["D"]:
            return False
        x = "x0 - 0.1" if cara == "izquierda" else "x0 + ancho + 1.3"
        cod = (f"esc = A.crear_escalera_recta('EscaleraExterior', huella={huella}, contrahuella={cont:.4f}, ancho=1.1, "
               f"num_peldanos={n}, origen=({x}, y0 + fondo / 2 - {g(largo)} / 2, 0))\n"
               f"esc.rotation_euler.z = math.pi / 2  # la escalera del DSL sube en +X; girada sube en +Y\n")
    e.secciones.append(f"# --- Escalera exterior pegada a la fachada {CARDINAL[cara]} ({EJE[cara]}) ---\n"
                       f"# {n} peldaños de {cont:.3f} m = altura de un piso\n" + cod)
    e.clausulas.append(f"Agrega una escalera exterior recta de 1.1 m de ancho junto a {nc}, desde el suelo hasta el {ORD[1]}.")
    e.checks.append(dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=-0.3, z_max=0.5))
    return True


def atico(e: Escena):
    r = e.r
    if e.meta["var"] == "casa" or e.meta["P"] < 2:
        return False
    a = min(r.choice([3, 4, 5, 6]), e.meta["W"] - 2)
    b = min(r.choice([3, 4, 5]), e.meta["D"] - 2)
    h = r.choice([2.5, 3.0])
    techo = "pisos * alto_piso + 0.2" if e.meta["var"] == "edificio" else "pisos * alto_piso + 0.1"
    e.secciones.append(
        f"# --- Volumen sobre la cubierta, centrado en planta ---\n"
        f"a_at, b_at, h_at = {g(a)}, {g(b)}, {g(h)}\n"
        f"atico = A.crear_edificio_n_pisos('Atico', pisos=1, ancho=a_at, fondo=b_at, alto_piso=h_at, "
        f"origen=(x0 + ancho / 2 - a_at / 2, y0 + fondo / 2 - b_at / 2, 0))\n"
        f"atico.location.z = {techo}  # apoyado sobre el techo\n")
    e.clausulas.append(r.choice([
        f"En la azotea, centrado, un volumen de {g(a)} x {g(b)} m y {g(h)} m de alto.",
        f"Corona el techo con un cuarto de {g(a)} por {g(b)} m ({g(h)} m de altura) en el centro."]))
    e.checks.append(dict(tipo="encima", ancho=a, fondo=b, alto=h))
    return True


def arboles(e: Escena, cara):
    r = e.r
    n, sep = r.randint(2, 5), r.choice([3, 4])
    nc = r.choice(NOMBRE_CARA[cara])
    if cara in ("frontal", "trasera"):
        y = f"y0 - {sep}" if cara == "frontal" else f"y0 + fondo + {sep}"
        cod = (f"for i in range({n}):\n    x = x0 + (i + 0.5) * ancho / {n}\n"
               f"    A.crear_arbol_simple(f'Arbol_{{i}}', origen=(x, {y}, 0))\n")
    else:
        x = f"x0 - {sep}" if cara == "izquierda" else f"x0 + ancho + {sep}"
        cod = (f"for i in range({n}):\n    y = y0 + (i + 0.5) * fondo / {n}\n"
               f"    A.crear_arbol_simple(f'Arbol_{{i}}', origen=({x}, y, 0))\n")
    e.secciones.append(f"# --- Fila de {n} árboles a {sep} m de la fachada {CARDINAL[cara]} ({EJE[cara]}) ---\n" + cod)
    e.clausulas.append(f"Planta una fila de {n} árboles a {sep} m de {nc}, repartidos a lo largo de la fachada.")
    return True


def vecino(e: Escena, cara):
    r = e.r
    W2, D2, P2 = r.choice([5, 6, 7, 8]), r.choice([5, 6, 7]), r.randint(1, 4)
    gap = r.choice([4, 5, 6, 8, 10, 12])
    Hp = e.meta["Hp"]
    if cara == "derecha":
        o = (f"x0 + ancho + sep", f"y0 + fondo / 2 - {g(D2)} / 2")
    elif cara == "izquierda":
        o = (f"x0 - sep - {g(W2)}", f"y0 + fondo / 2 - {g(D2)} / 2")
    elif cara == "trasera":
        o = (f"x0 + ancho / 2 - {g(W2)} / 2", f"y0 + fondo + sep")
    else:
        o = (f"x0 + ancho / 2 - {g(W2)} / 2", f"y0 - sep - {g(D2)}")
    e.secciones.append(
        f"# --- Segundo edificio al {CARDINAL[cara]} ({EJE[cara].split(',')[0]}), separado 'sep' m de fachada a fachada ---\n"
        f"sep = {g(gap)}\n"
        f"edificio2 = A.crear_edificio_n_pisos('Edificio2', pisos={P2}, ancho={g(W2)}, fondo={g(D2)}, "
        f"alto_piso=alto_piso, origen=({o[0]}, {o[1]}, 0))\n")
    e.clausulas.append(r.choice([
        f"Al {CARDINAL[cara]} del principal, a {g(gap)} m de distancia libre, coloca otro edificio de {P2} pisos de {g(W2)} x {g(D2)} m centrado respecto al primero.",
        f"Suma un segundo bloque ({g(W2)} x {g(D2)} m, {P2} plantas) hacia el {CARDINAL[cara]}, dejando {g(gap)} m entre ambas fachadas, alineado al centro."]))
    e.checks.append(dict(tipo="separacion", otro=dict(ancho=W2, fondo=D2, alto=P2 * Hp), cara=cara, gap=gap))
    return True


def rotar_todo(e: Escena):
    r = e.r
    th = r.choice([10, 15, 20, 25, 30, 35, 40, 50, 55, 60, 70, 80])
    horario = r.random() < 0.35
    ang = -th if horario else th
    e.secciones.append(
        f"# --- Girar todo el conjunto {th}° {'en sentido horario' if horario else 'antihorario'} alrededor de su centro ---\n"
        f"pivote = bpy.data.objects.new('Conjunto', None)\n"
        f"bpy.context.collection.objects.link(pivote)\n"
        f"pivote.location = (x0 + ancho / 2, y0 + fondo / 2, 0)\n"
        f"for o in list(bpy.context.scene.objects):\n"
        f"    if o.parent is None and o is not pivote:\n"
        f"        o.parent = pivote\n"
        f"        o.matrix_parent_inverse = pivote.matrix_world.inverted()\n"
        f"pivote.rotation_euler.z = math.radians({ang})\n")
    e.clausulas.append(r.choice([
        f"Gira todo el conjunto {th}° {'en sentido horario' if horario else 'en sentido antihorario'} respecto al norte.",
        f"El conjunto debe quedar rotado {th} grados {'a la derecha (horario)' if horario else 'a la izquierda (antihorario)'} sobre su centro."]))
    e.rotada = True
    e.meta["rot"] = ang
    return True


# ====================================================================== formas fuera del DSL
def forma_mono(e: Escena):
    r = e.r
    W, D, Hp = r.choice([7, 8, 10, 12]), r.choice([6, 8, 9, 10]), r.choice([2.8, 3.0])
    P, ang, cara = r.randint(1, 2), r.choice([8, 12, 15, 20, 25, 30]), r.choice(CARAS)
    e.meta.update(W=W, D=D, Hp=Hp, P=P, x0=0, y0=0, var="casa", estilo="forma")
    hz = {"frontal": "(zb, zb, za, za)", "trasera": "(za, za, zb, zb)",
          "izquierda": "(zb, za, za, zb)", "derecha": "(za, zb, zb, za)"}[cara]
    luz = "fondo" if cara in ("frontal", "trasera") else "ancho"
    e.secciones.append(
        f"# --- Casa sin tejado (el DSL solo trae dos aguas) ---\n"
        f"ancho, fondo, alto_piso, pisos = {g(W)}, {g(D)}, {g(Hp)}, {P}\n"
        f"x0, y0 = 0, 0\n"
        f"casa = A.crear_casa_n_pisos('Casa', pisos=pisos, ancho=ancho, fondo=fondo, alto_piso=alto_piso, con_tejado=False)\n\n"
        f"# --- Techo de una pendiente con bmesh: el lado bajo está en la fachada {CARDINAL[cara]} ({EJE[cara]}) ---\n"
        f"pendiente = math.radians({ang})\n"
        f"z0 = pisos * alto_piso + 0.2\n"
        f"zb, za = z0, z0 + {luz} * math.tan(pendiente)  # subida = luz * tan(pendiente)\n"
        f"v = 0.3  # alero\n"
        f"esquinas = [(x0 - v, y0 - v), (x0 + ancho + v, y0 - v), (x0 + ancho + v, y0 + fondo + v), (x0 - v, y0 + fondo + v)]\n"
        f"alturas = {hz}  # SO, SE, NE, NO\n"
        f"bm = bmesh.new()\n"
        f"abajo = [bm.verts.new((x, y, z0 - 0.15)) for x, y in esquinas]\n"
        f"arriba = [bm.verts.new((x, y, z)) for (x, y), z in zip(esquinas, alturas)]\n"
        f"bm.faces.new(abajo[::-1])\n"
        f"bm.faces.new(arriba)\n"
        f"for i in range(4):\n"
        f"    j = (i + 1) % 4\n"
        f"    bm.faces.new((abajo[i], abajo[j], arriba[j], arriba[i]))\n"
        f"bm.normal_update()\n"
        f"malla = bpy.data.meshes.new('TechoUnaAgua')\n"
        f"bm.to_mesh(malla)\n"
        f"bm.free()\n"
        f"techo = bpy.data.objects.new('TechoUnaAgua', malla)\n"
        f"bpy.context.collection.objects.link(techo)\n")
    e.clausulas.append(r.choice([
        f"una casa de {P} piso{'s' if P > 1 else ''} de {g(W)} x {g(D)} m (pisos de {g(Hp)} m) con cubierta a un agua de {ang}° que desagua hacia el {CARDINAL[cara]}",
        f"una vivienda de {g(W)} por {g(D)} m y {P} planta{'s' if P > 1 else ''} de {g(Hp)} m, techada con una sola pendiente de {ang} grados cuyo lado bajo mira al {CARDINAL[cara]}"]))
    e.edificio = dict(ancho=W, fondo=D, alto=None)
    e.checks.append(dict(tipo="pendiente", aguas=1, grados=ang, tol=4, cae=cara))


def forma_L(e: Escena):
    r = e.r
    W, D, Hp, P = r.choice([14, 16, 18, 20, 24]), r.choice([12, 14, 16, 18]), r.choice([3.0, 3.2]), r.randint(1, 5)
    a, b = r.choice([5, 6, 7, 8]), r.choice([5, 6, 7])
    esq = r.choice(["noreste", "noroeste", "sureste", "suroeste"])
    ex, ey = esq in ("noreste", "sureste"), esq in ("noreste", "noroeste")
    # perfil de la L recorriendo el contorno (sentido antihorario)
    vx = (a, W) if ex else (0, W - a)    # rango X de la esquina vacía
    vy = (b, D) if ey else (0, D - b)    # rango Y de la esquina vacía
    pts = [(0, 0), (W, 0), (W, D), (0, D)]
    cut = {"noreste": [(0, 0), (W, 0), (W, b), (a, b), (a, D), (0, D)],
           "noroeste": [(0, 0), (W, 0), (W, D), (W - a, D), (W - a, b), (0, b)],
           "sureste": [(0, 0), (a, 0), (a, D - b), (W, D - b), (W, D), (0, D)],
           "suroeste": [(W - a, 0), (W, 0), (W, D), (0, D), (0, D - b), (W - a, D - b)]}[esq]
    e.meta.update(W=W, D=D, Hp=Hp, P=P, x0=0, y0=0, var="L", estilo="forma")
    e.secciones.append(
        f"# --- Planta en L: rectángulo de {g(W)} x {g(D)} m sin la esquina {esq} ---\n"
        f"# brazo en X de {g(b)} m de ancho, brazo en Y de {g(a)} m de ancho\n"
        f"alto_piso, pisos = {g(Hp)}, {P}\n"
        f"perfil = {[(g(x), g(y)) for x, y in cut]}\n".replace("'", "") +
        f"for p in range(pisos):\n"
        f"    nivel = A.extruir_perfil(f'Nivel_{{p}}', puntos_2d=perfil, altura=alto_piso - 0.2, material='Muro_Pintura')\n"
        f"    nivel.location.z = p * alto_piso\n"
        f"    losa = A.extruir_perfil(f'Losa_{{p}}', puntos_2d=perfil, altura=0.2, material='Hormigon')\n"
        f"    losa.location.z = (p + 1) * alto_piso - 0.2\n")
    e.clausulas.append(r.choice([
        f"un edificio de {P} planta{'s' if P > 1 else ''} con planta en L que ocupa {g(W)} m en X y {g(D)} m en Y; el brazo horizontal tiene {g(b)} m de ancho, el vertical {g(a)} m, y la esquina {esq} queda libre",
        f"un bloque en forma de L de {P} piso{'s' if P > 1 else ''} (pisos de {g(Hp)} m) dentro de un rectángulo de {g(W)} x {g(D)} m, con brazos de {g(b)} y {g(a)} m y el patio abierto hacia el {esq}"]))
    occ = [(0.5, (b / 2 if ey else D - b / 2) / D),
           ((a / 2 if ex else W - a / 2) / W, ((b + D) / 2 if ey else (D - b) / 2) / D)]
    vac = (((vx[0] + vx[1]) / 2) / W, ((vy[0] + vy[1]) / 2) / D)
    e.checks += [dict(tipo="dims_total", ancho=W, fondo=D, alto=P * Hp), dict(tipo="huella", ocupados=occ, vacios=[vac])]


def forma_cilindro(e: Escena):
    r = e.r
    Dm, P, Hp = r.choice([8, 10, 12, 14, 18, 22]), r.randint(3, 15), r.choice([3.0, 3.2, 3.5])
    nv = r.choice([32, 48, 64])
    e.meta.update(var="cil", estilo="forma")
    e.secciones.append(
        f"# --- Torre cilíndrica con bpy: núcleo + losas circulares que sobresalen 0.3 m ---\n"
        f"diametro, pisos, alto_piso = {g(Dm)}, {P}, {g(Hp)}\n"
        f"bpy.ops.mesh.primitive_cylinder_add(vertices={nv}, radius=diametro / 2 - 0.3, depth=pisos * alto_piso, "
        f"location=(0, 0, pisos * alto_piso / 2))\n"
        f"bpy.context.active_object.name = 'Fuste'\n"
        f"for p in range(pisos + 1):\n"
        f"    bpy.ops.mesh.primitive_cylinder_add(vertices={nv}, radius=diametro / 2, depth=0.25, location=(0, 0, p * alto_piso))\n"
        f"    bpy.context.active_object.name = f'Losa_{{p}}'\n")
    e.clausulas.append(r.choice([
        f"una torre de planta circular de {g(Dm)} m de diámetro con {P} pisos de {g(Hp)} m",
        f"un edificio cilíndrico de {P} niveles ({g(Hp)} m cada uno) y {g(Dm)} m de diámetro, con losas circulares"]))
    e.checks += [dict(tipo="dims_total", ancho=Dm, fondo=Dm, alto=P * Hp), dict(tipo="redondo")]


def forma_escalonado(e: Escena):
    r = e.r
    W, D = r.choice([16, 20, 24, 28]), r.choice([14, 16, 20])
    k, s, Pv, Hp = r.choice([2, 3, 4]), r.choice([1.5, 2, 3]), r.randint(1, 4), r.choice([3.0, 3.2])
    if W - 2 * s * (k - 1) < 4 or D - 2 * s * (k - 1) < 4:
        k = 2
    e.meta.update(var="esc", estilo="forma")
    e.secciones.append(
        f"# --- Volúmenes apilados: cada uno se retranquea 'retiro' m por los cuatro lados ---\n"
        f"ancho, fondo, retiro = {g(W)}, {g(D)}, {g(s)}\n"
        f"pisos_vol, alto_piso = {Pv}, {g(Hp)}\n"
        f"z = 0.0\n"
        f"for i in range({k}):\n"
        f"    v = A.crear_edificio_n_pisos(f'Volumen_{{i + 1}}', pisos=pisos_vol, ancho=ancho - 2 * retiro * i, "
        f"fondo=fondo - 2 * retiro * i, alto_piso=alto_piso, origen=(retiro * i, retiro * i, 0))\n"
        f"    v.location.z = z\n"
        f"    z += pisos_vol * alto_piso + 0.2  # el siguiente apoya sobre el techo de este\n")
    e.clausulas.append(r.choice([
        f"un edificio aterrazado de {k} cuerpos de {Pv} piso{'s' if Pv > 1 else ''} cada uno; la base mide {g(W)} x {g(D)} m y cada cuerpo superior se retira {g(s)} m en todo su perímetro",
        f"una pirámide escalonada de {k} volúmenes ({Pv} plantas de {g(Hp)} m por volumen), base de {g(W)} por {g(D)} m y retranqueos de {g(s)} m por lado"]))
    e.checks += [dict(tipo="dims_total", ancho=W, fondo=D, alto=k * (Pv * Hp + 0.2) - 0.2),
                 dict(tipo="escalonado", niveles=k, retiro=s)]


# ====================================================================== escenas
def escena_compuesta(r):
    e = Escena(r)
    estilo = r.choices(["edificio", "casa", "bpy"], [0.6, 0.2, 0.2])[0]
    edificio_principal(e, estilo)
    mods = r.choices(["balcon", "anexo", "marquesina", "escalera", "atico", "arboles", "vecino"],
                     [0.3, 0.12, 0.1, 0.1, 0.12, 0.1, 0.16], k=r.choice([1, 1, 2, 2, 3]))
    libres = CARAS[:]  # una cara por modificador, para que no se pisen entre sí
    r.shuffle(libres)
    for m in dict.fromkeys(mods):  # sin repetir modificador
        if not libres:
            break
        cara = libres.pop() if m != "atico" else None
        ok = {"balcon": lambda: balcones(e, cara, r.choice(["uno", "todos", "alternos"])),
              "anexo": lambda: anexo(e, cara), "marquesina": lambda: marquesina(e, cara),
              "escalera": lambda: escalera(e, cara), "atico": lambda: atico(e),
              "arboles": lambda: arboles(e, cara), "vecino": lambda: vecino(e, cara)}[m]()
    # las relaciones por cara se verifican en ejes globales: si se rota, solo se comprueba el giro
    if r.random() < 0.15 and e.edificio["alto"] is not None:
        rotar_todo(e)
        e.checks = [dict(tipo="rotacion", grados=e.meta["rot"], tol=5)]
    if e.edificio and e.edificio.get("alto"):
        e.checks.insert(0, dict(tipo="dims", **e.edificio))
    return e


def escena_forma(r):
    e = Escena(r)
    r.choice([forma_mono, forma_L, forma_cilindro, forma_escalonado])(e)
    return e


# ====================================================================== salida
def mensajes(pedido, codigo):
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": pedido},
            {"role": "assistant", "content": codigo}]


def ejemplo_creacion(r, i):
    e = escena_compuesta(r) if r.random() < 0.75 else escena_forma(r)
    return dict(id=f"proc_{i:06d}", task_type="creation", fuente="procedural", meta=e.meta,
                pedido=e.pedido(), codigo=e.codigo(), checks=e.checks, edificio=e.edificio)


def ejemplo_edicion(r, i):
    """Base = edificio (+0..1 modificador); instrucción = un modificador espacial más."""
    while True:
        e = Escena(r)
        edificio_principal(e, r.choices(["edificio", "casa", "bpy"], [0.7, 0.15, 0.15])[0])
        if r.random() < 0.5:
            c0 = r.choice(CARAS)
            r.choice([lambda: anexo(e, c0), lambda: marquesina(e, c0), lambda: arboles(e, c0)])()
        base = e.codigo()
        n_cl, n_ch = len(e.clausulas), len(e.checks)
        cara = r.choice(CARAS)
        m = r.choice(["balcon", "anexo", "escalera", "atico", "vecino", "rotar"])
        ok = {"balcon": lambda: balcones(e, cara, r.choice(["uno", "todos"])), "anexo": lambda: anexo(e, cara),
              "escalera": lambda: escalera(e, cara), "atico": lambda: atico(e), "vecino": lambda: vecino(e, cara),
              "rotar": lambda: e.edificio["alto"] is not None and rotar_todo(e)}[m]()
        if ok:
            break
    instr = gramatica(" ".join(e.clausulas[n_cl:]))
    checks = [dict(tipo="rotacion", grados=e.meta["rot"], tol=5)] if e.rotada else e.checks[n_ch:]
    if e.edificio.get("alto"):
        checks.insert(0, dict(tipo="dims", **e.edificio))
    pedido = f"Código base:\n```python\n{base.strip()}\n```\nInstrucción: {instr}"
    return dict(id=f"proc_{i:06d}", task_type="edit_single", fuente="procedural", meta=e.meta,
                pedido=pedido, codigo=e.codigo(), checks=checks, edificio=e.edificio)


def gramatica(t):
    t = re.sub(r"\ba el\b", "al", t)
    t = re.sub(r"\bde el\b", "del", t)
    return re.sub(r"\bA el\b", "Al", t)


def norm(t):
    return re.sub(r"[^a-záéíóúñ0-9 ]", " ", t.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--frac_edicion", type=float, default=0.3)
    ap.add_argument("--out", default=os.path.join(HERE, "muestras"))
    a = ap.parse_args()
    r = random.Random(a.seed)
    bench = [norm(json.loads(l)["prompt"]) for l in open(BENCH)] if os.path.exists(BENCH) else []
    os.makedirs(os.path.join(a.out, "py"), exist_ok=True)
    n_desc = 0
    with open(os.path.join(a.out, "candidatos.jsonl"), "w") as fo:
        i = 0
        while i < a.n:
            ej = ejemplo_edicion(r, i) if r.random() < a.frac_edicion else ejemplo_creacion(r, i)
            # anti-contaminación: descartar pedidos casi idénticos a alguno del benchmark
            p = norm(ej["pedido"])
            if any(difflib.SequenceMatcher(None, p, b).quick_ratio() > 0.9 and
                   difflib.SequenceMatcher(None, p, b).ratio() > 0.8 for b in bench):
                n_desc += 1
                continue
            with open(os.path.join(a.out, "py", ej["id"] + ".py"), "w") as fc:
                fc.write(ej["codigo"])
            fo.write(json.dumps(ej, ensure_ascii=False) + "\n")
            i += 1
    print(f"{a.n} candidatos en {a.out} (descartados por parecido al benchmark: {n_desc})")


if __name__ == "__main__":
    main()
