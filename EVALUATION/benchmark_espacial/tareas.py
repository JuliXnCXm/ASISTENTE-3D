#!/usr/bin/env python3
"""
tareas.py — Benchmark de razonamiento espacial (Fase 1 de v4).

Genera tareas con verificación GEOMÉTRICA automática (no compara código):
cada tarea = pedido en español + lista de chequeos + código oráculo que los cumple
(el oráculo valida que el benchmark sea resoluble y que el verificador no tenga bugs).

Convención de ejes (la del DSL blender_arch):
  frontal / principal / sur  = -Y      trasera / posterior / norte = +Y
  izquierda / oeste          = -X      derecha / este              = +X
  (izquierda/derecha vistas desde el frente)

Categorías:
  cara        elemento adosado a una fachada concreta (balcón, anexo, marquesina, escalera)
  cada_piso   elemento repetido en cada piso de una fachada
  encima      volumen sobre la cubierta
  rotacion    edificio girado un ángulo
  separacion  dos edificios con relación cardinal y distancia borde a borde
  forma       geometría fuera del DSL: techo de una pendiente, planta en L, cilindro, escalonado
  edicion     las anteriores como edición de un código base

Uso:  python3 tareas.py  ->  tareas.jsonl + oraculo/<id>.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
H = 3.0  # altura de piso en todo el benchmark

CARAS = {
    "frontal":   ["la fachada frontal", "la fachada principal", "la fachada sur", "el lado sur"],
    "trasera":   ["la fachada trasera", "la fachada posterior", "la fachada norte", "el lado norte"],
    "izquierda": ["la fachada izquierda", "el costado izquierdo", "la fachada oeste", "el lado oeste"],
    "derecha":   ["la fachada derecha", "el costado derecho", "la fachada este", "el lado este"],
}
OPUESTA = {"frontal": "trasera", "trasera": "frontal", "izquierda": "derecha", "derecha": "izquierda"}
CARDINAL = {"frontal": "sur", "trasera": "norte", "izquierda": "oeste", "derecha": "este"}
ORD = ["planta baja", "primer piso", "segundo piso", "tercer piso", "cuarto piso", "quinto piso"]

CAB = "import blender_arch as A\nimport bpy\nimport bmesh\nimport math\n\nA.limpiar_escena()\n"


def f(x):
    return f"{x:g}"


def edificio_txt(W, D, P):
    return f"un edificio de {P} pisos de {f(W)} x {f(D)} metros con altura de piso de {f(H)} m y techo plano"


def edificio_code(W, D, P, nombre="Edificio", origen=(0, 0, 0), var="ed"):
    return (f"{var} = A.crear_edificio_n_pisos('{nombre}', pisos={P}, ancho={f(W)}, fondo={f(D)}, "
            f"alto_piso={f(H)}, origen=({f(origen[0])}, {f(origen[1])}, {f(origen[2])}))\n")


# ------------------------------------------------------------------ elementos en una cara
def losa_en_cara(cara, W, D, z, a, b, nombre, con_baranda=True, esp=0.2):
    """Losa de a (a lo largo de la fachada) x b (vuelo) centrada en la fachada, a la altura z."""
    if cara == "frontal":
        o, (sx, sy) = (W / 2 - a / 2, -b, z), (a, b)
    elif cara == "trasera":
        o, (sx, sy) = (W / 2 - a / 2, D, z), (a, b)
    elif cara == "izquierda":
        o, (sx, sy) = (-b, D / 2 - a / 2, z), (b, a)
    else:
        o, (sx, sy) = (W, D / 2 - a / 2, z), (b, a)
    c = (f"A.crear_losa_rectangular('{nombre}', ancho={f(sx)}, fondo={f(sy)}, espesor={esp}, "
         f"origen=({f(o[0])}, {f(o[1])}, {f(z)}))\n")
    if con_baranda:  # baranda en el borde exterior (la baranda del DSL corre a lo largo de +X)
        zt = z + esp
        if cara == "frontal":
            c += f"A.crear_baranda_lineal('{nombre}_Baranda', largo={f(a)}, altura=1.1, origen=({f(o[0])}, {f(-b)}, {f(zt)}))\n"
        elif cara == "trasera":
            c += f"A.crear_baranda_lineal('{nombre}_Baranda', largo={f(a)}, altura=1.1, origen=({f(o[0])}, {f(D + b - 0.08)}, {f(zt)}))\n"
        else:
            x = -b if cara == "izquierda" else W + b - 0.08
            c += (f"_b = A.crear_baranda_lineal('{nombre}_Baranda', largo={f(a)}, altura=1.1, "
                  f"origen=({f(x + 0.08)}, {f(o[1])}, {f(zt)}))\n_b.rotation_euler.z = math.pi / 2\n")
    return c


def anexo_en_cara(cara, W, D, a, b, P=1):
    if cara == "frontal":
        o = (W / 2 - a / 2, -b)
        sx, sy = a, b
    elif cara == "trasera":
        o = (W / 2 - a / 2, D)
        sx, sy = a, b
    elif cara == "izquierda":
        o = (-b, D / 2 - a / 2)
        sx, sy = b, a
    else:
        o = (W, D / 2 - a / 2)
        sx, sy = b, a
    return edificio_code(sx, sy, P, "Anexo", (o[0], o[1], 0), var="anexo")


def escalera_en_cara(cara, W, D, n=17):
    """Escalera exterior de planta baja al primer piso, pegada a la fachada (vuelo 1.3 m)."""
    huella, cont = 0.28, H / n
    largo = n * huella
    if cara in ("frontal", "trasera"):
        y = -1.3 if cara == "frontal" else D + 0.1
        return (f"A.crear_escalera_recta('EscaleraExterior', huella={huella}, contrahuella={cont:.4f}, ancho=1.1, "
                f"num_peldanos={n}, origen=({f(W / 2 - largo / 2)}, {f(y)}, 0))\n")
    x = -1.3 if cara == "izquierda" else W + 0.1
    return (f"_e = A.crear_escalera_recta('EscaleraExterior', huella={huella}, contrahuella={cont:.4f}, ancho=1.1, "
            f"num_peldanos={n}, origen=({f(x + 1.2)}, {f(D / 2 - largo / 2)}, 0))\n_e.rotation_euler.z = math.pi / 2\n")


# ------------------------------------------------------------------ generador
class Gen:
    def __init__(self, seed=7):
        self.r = random.Random(seed)
        self.tareas = []

    def dims(self):
        r = self.r
        return r.choice([10, 12, 14, 16, 18, 20]), r.choice([8, 10, 12, 14]), r.randint(3, 6)

    def add(self, cat, sub, prompt, checks, oraculo, base=None, edificio=None, neg=None):
        tid = f"esp_{len(self.tareas) + 1:03d}"
        t = dict(id=tid, categoria=cat, subtipo=sub, prompt=prompt, checks=checks, edificio=edificio)
        if base:
            t["codigo_base"] = base
            t["prompt"] = f"Código base:\n```python\n{base.strip()}\n```\nInstrucción: {prompt}"
            t["instruccion"] = prompt
        t["oraculo"] = oraculo
        t["negativo"] = neg
        self.tareas.append(t)

    # ---- cara
    def cara(self, n=40):
        r = self.r
        elems = ["balcon", "anexo", "marquesina", "escalera"]
        for i in range(n):
            W, D, P = self.dims()
            el, cara = elems[i % 4], list(CARAS)[(i // 4) % 4]
            ct = r.choice(CARAS[cara])
            ed = edificio_txt(W, D, P)
            spec = dict(ancho=W, fondo=D, alto=P * H)
            if el == "balcon":
                k = r.randint(1, P - 1)
                prompt = (f"Crea {ed}. Agrega un balcón en voladizo de 3 metros de ancho y 1.5 metros de vuelo "
                          f"con baranda en {ct}, a la altura del {ORD[k]}.")
                ck = [dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6),
                      dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6)]
                code = CAB + edificio_code(W, D, P) + losa_en_cara(cara, W, D, k * H, 3, 1.5, "Balcon")
                neg = CAB + edificio_code(W, D, P) + losa_en_cara(OPUESTA[cara], W, D, k * H, 3, 1.5, "Balcon")
            elif el == "anexo":
                a, b = r.choice([4, 5, 6]), r.choice([3, 4])
                prompt = (f"Crea {ed}. Adosa en {ct} un anexo de un piso de {a} metros de largo "
                          f"(a lo largo de la fachada) por {b} metros de profundidad.")
                ck = [dict(tipo="cara", cara=cara, vuelo_min=b * 0.6, z_min=-0.3, z_max=0.6),
                      dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=1.0, z_min=-0.3, z_max=0.6)]
                code = CAB + edificio_code(W, D, P) + anexo_en_cara(cara, W, D, a, b)
                neg = CAB + edificio_code(W, D, P) + anexo_en_cara(OPUESTA[cara], W, D, a, b)
            elif el == "marquesina":
                prompt = (f"Crea {ed}. Sobre la entrada de {ct} coloca una marquesina en voladizo de "
                          f"4 metros de ancho y 1.5 metros de vuelo a 3 metros de altura.")
                ck = [dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=2.3, z_max=3.7),
                      dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=0.8, z_min=2.3, z_max=3.7)]
                code = CAB + edificio_code(W, D, P) + losa_en_cara(cara, W, D, 3.0, 4, 1.5, "Marquesina",
                                                                     con_baranda=False, esp=0.15)
                neg = CAB + edificio_code(W, D, P) + losa_en_cara(OPUESTA[cara], W, D, 3.0, 4, 1.5, "Marquesina", con_baranda=False, esp=0.15)
            else:
                prompt = (f"Crea {ed}. Agrega una escalera exterior recta de 1.1 metros de ancho pegada a "
                          f"{ct}, que suba desde el suelo hasta el {ORD[1]}.")
                ck = [dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=-0.3, z_max=0.5),
                      dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=0.8, z_min=-0.3, z_max=0.5)]
                code = CAB + edificio_code(W, D, P) + escalera_en_cara(cara, W, D)
                neg = CAB + edificio_code(W, D, P) + escalera_en_cara(OPUESTA[cara], W, D)
            self.add("cara", el, prompt, [dict(tipo="dims", **spec)] + ck, code, edificio=spec, neg=neg)

    # ---- cada piso
    def cada_piso(self, n=15):
        r = self.r
        for i in range(n):
            W, D, P = self.dims()
            cara = list(CARAS)[i % 4]
            ct = r.choice(CARAS[cara])
            spec = dict(ancho=W, fondo=D, alto=P * H)
            prompt = (f"Crea {edificio_txt(W, D, P)}. En {ct}, agrega en cada piso desde el primero hasta el "
                      f"último un balcón en voladizo de 3 x 1.5 metros con baranda.")
            code = CAB + edificio_code(W, D, P) + "".join(
                losa_en_cara(cara, W, D, k * H, 3, 1.5, f"Balcon_{k}") for k in range(1, P))
            ck = [dict(tipo="dims", **spec),
                  dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=H - 0.6, z_max=P * H, niveles_min=P - 1),
                  dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=0.8, z_min=H - 0.6, z_max=P * H)]
            neg = CAB + edificio_code(W, D, P) + losa_en_cara(cara, W, D, H, 3, 1.5, "Balcon_1")
            self.add("cada_piso", "balcones", prompt, ck, code, edificio=spec, neg=neg)

    # ---- encima
    def encima(self, n=15):
        r = self.r
        for i in range(n):
            W, D, P = self.dims()
            a, b, c = r.choice([3, 4, 5]), r.choice([3, 4]), r.choice([2.5, 3])
            que = r.choice(["un volumen", "una sala de máquinas", "un cuarto técnico", "un ático"])
            spec = dict(ancho=W, fondo=D, alto=P * H)
            prompt = (f"Crea {edificio_txt(W, D, P)}. Sobre la cubierta, centrado, coloca {que} de "
                      f"{f(a)} x {f(b)} metros y {f(c)} metros de alto con techo plano.")
            code = CAB + edificio_code(W, D, P) + \
                edificio_code(a, b, 1, "Atico", (W / 2 - a / 2, D / 2 - b / 2, 0), var="atico") + \
                f"atico.location.z = {P * H + 0.2:g}\n"
            ck = [dict(tipo="dims", **spec), dict(tipo="encima", ancho=a, fondo=b, alto=c)]
            self.add("encima", "volumen", prompt, ck, code, edificio=spec, neg=CAB + edificio_code(W, D, P))

    # ---- rotación
    def rotacion(self, n=15):
        r = self.r
        angs = [15, 20, 25, 30, 35, 40, 50, 55, 60, 65, 70, 75, 20, 30, 60]
        for i in range(n):
            W, D, P = self.dims()
            while W == D:
                W, D, P = self.dims()
            th = angs[i]
            horario = i % 3 == 2
            sentido = "en sentido horario" if horario else r.choice(["en sentido antihorario", ""])
            prompt = (f"Crea {edificio_txt(W, D, P)}, girado {th} grados {sentido} alrededor del eje vertical "
                      f"respecto a los ejes X/Y.").replace("  ", " ")
            ang = -th if horario else th
            code = CAB + edificio_code(W, D, P) + f"ed.rotation_euler.z = math.radians({ang})\n"
            spec = dict(ancho=W, fondo=D, alto=P * H)
            self.add("rotacion", "edificio", prompt,
                     [dict(tipo="dims", **spec), dict(tipo="rotacion", grados=ang, tol=5)], code, edificio=spec,
                     neg=CAB + edificio_code(W, D, P))

    # ---- separación
    def separacion(self, n=15):
        r = self.r
        for i in range(n):
            W, D, P = self.dims()
            W2, D2, P2 = r.choice([6, 8, 9]), r.choice([6, 7]), r.randint(1, 3)
            g = r.choice([5, 6, 8, 10, 12, 15])
            cara = list(CARAS)[i % 4]
            card = CARDINAL[cara]
            prompt = (f"Crea {edificio_txt(W, D, P)} y un segundo edificio de {P2} pisos de {f(W2)} x {f(D2)} "
                      f"metros ubicado al {card} del primero, separados {f(g)} metros entre sus fachadas "
                      f"enfrentadas y alineados por el centro.")
            o = {"derecha": (W + g, D / 2 - D2 / 2), "izquierda": (-g - W2, D / 2 - D2 / 2),
                 "trasera": (W / 2 - W2 / 2, D + g), "frontal": (W / 2 - W2 / 2, -g - D2)}[cara]
            code = CAB + edificio_code(W, D, P) + edificio_code(W2, D2, P2, "Edificio2", (o[0], o[1], 0), "ed2")
            o2 = {"derecha": (W + 2 * g, D / 2 - D2 / 2), "izquierda": (-2 * g - W2, D / 2 - D2 / 2),
                  "trasera": (W / 2 - W2 / 2, D + 2 * g), "frontal": (W / 2 - W2 / 2, -2 * g - D2)}[cara]
            neg = CAB + edificio_code(W, D, P) + edificio_code(W2, D2, P2, "Edificio2", (o2[0], o2[1], 0), "ed2")
            spec = dict(ancho=W, fondo=D, alto=P * H)
            spec2 = dict(ancho=W2, fondo=D2, alto=P2 * H)
            self.add("separacion", card, prompt,
                     [dict(tipo="dims", **spec), dict(tipo="separacion", otro=spec2, cara=cara, gap=g)],
                     code, edificio=spec, neg=neg)

    # ---- formas fuera del DSL
    def formas(self):
        r = self.r
        # techo de una pendiente (8)
        for i in range(8):
            W, D = r.choice([8, 10, 12]), r.choice([8, 10])
            P = r.randint(1, 2)
            ang = r.choice([10, 15, 20, 25])
            cara = list(CARAS)[i % 4]
            prompt = (f"Crea una casa de {P} piso{'s' if P > 1 else ''} de {f(W)} x {f(D)} metros con altura de piso "
                      f"de {f(H)} m y un techo de una sola pendiente (mono-pendiente) de {ang} grados que cae hacia "
                      f"el {CARDINAL[cara]}.")
            z0 = P * H
            # cae hacia 'cara' = el lado bajo está en esa cara
            rise = (D if cara in ("frontal", "trasera") else W) * math_tan(ang)
            code = CAB + f"casa = A.crear_casa_n_pisos('Casa', pisos={P}, ancho={f(W)}, fondo={f(D)}, alto_piso={f(H)}, con_tejado=False)\n"
            neg = code + mono_pendiente_code(W, D, z0, rise, OPUESTA[cara])
            code += mono_pendiente_code(W, D, z0, rise, cara)
            spec = dict(ancho=W, fondo=D, alto=None)
            self.add("forma", "mono_pendiente", prompt,
                     [dict(tipo="dims", **spec), dict(tipo="pendiente", aguas=1, grados=ang, tol=6, cae=cara)],
                     code, edificio=spec, neg=neg)
        # planta en L (7)
        esquinas = {"noreste": (1, 1), "noroeste": (0, 1), "sureste": (1, 0), "suroeste": (0, 0)}
        for i in range(7):
            W, D, P = r.choice([16, 18, 20]), r.choice([14, 16]), r.randint(2, 4)
            a, b = r.choice([6, 7, 8]), r.choice([6, 7])  # ancho de cada brazo
            esq = list(esquinas)[i % 4]
            ex, ey = esquinas[esq]
            prompt = (f"Crea un edificio de {P} pisos con planta en forma de L, de {f(W)} metros en X por {f(D)} "
                      f"metros en Y en total; los brazos miden {f(b)} metros de ancho (el brazo en X) y {f(a)} metros "
                      f"(el brazo en Y). La esquina vacía de la L es la {esq}. Altura de piso {f(H)} m.")
            # brazo X (ancho total W, fondo b) en la franja opuesta a la esquina vacía en Y;
            # brazo Y (ancho a) en la franja opuesta en X, cubriendo el resto del fondo.
            yX = 0 if ey == 1 else D - b
            xY = 0 if ex == 1 else W - a
            yY = b if ey == 1 else 0
            code = CAB + edificio_code(W, b, P, "BrazoX", (0, yX, 0), "bx") + \
                edificio_code(a, D - b, P, "BrazoY", (xY, yY, 0), "by")
            # puntos como fracciones del bbox total (x/W, y/D)
            vac = ((a + W) / 2 / W if ex == 1 else (W - a) / 2 / W,
                   (b + D) / 2 / D if ey == 1 else (D - b) / 2 / D)
            occ = [(0.5, (yX + b / 2) / D), ((xY + a / 2) / W, (yY + (D - b) / 2) / D)]
            self.add("forma", "planta_L", prompt,
                     [dict(tipo="dims_total", ancho=W, fondo=D, alto=P * H),
                      dict(tipo="huella", ocupados=occ, vacios=[vac])], code, neg=CAB + edificio_code(W, D, P))
        # torre cilíndrica (5)
        for i in range(5):
            Dm, P = r.choice([10, 12, 14, 16, 20]), r.randint(4, 10)
            prompt = (f"Crea una torre cilíndrica de {f(Dm)} metros de diámetro y {P} pisos de {f(H)} m, "
                      f"con losas circulares en cada piso.")
            code = CAB + f"for i in range({P + 1}):\n    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius={Dm / 2}, depth=0.25, location=(0, 0, i*{f(H)}))\n" \
                f"bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius={Dm / 2 - 0.3}, depth={P * H}, location=(0, 0, {P * H / 2}))\n"
            self.add("forma", "cilindro", prompt,
                     [dict(tipo="dims_total", ancho=Dm, fondo=Dm, alto=P * H), dict(tipo="redondo")], code,
                     neg=CAB + edificio_code(Dm, Dm, P))
        # escalonado (5)
        for i in range(5):
            W, D = r.choice([20, 24]), r.choice([16, 20])
            k, s, Pv = r.choice([3, 4]), r.choice([2, 3]), r.choice([2, 3])
            prompt = (f"Crea un edificio escalonado de {k} volúmenes apilados de {Pv} pisos cada uno (altura de piso "
                      f"{f(H)} m). El volumen inferior mide {f(W)} x {f(D)} metros y cada volumen superior se retranquea "
                      f"{f(s)} metros por todos sus lados respecto al de abajo.")
            code = CAB
            for j in range(k):
                code += edificio_code(W - 2 * s * j, D - 2 * s * j, Pv, f"Volumen_{j + 1}", (s * j, s * j, 0), f"v{j}")
                code += f"v{j}.location.z = {j * (Pv * H + 0.2):g}\n"
            neg = CAB + edificio_code(W, D, k * Pv)
            self.add("forma", "escalonado", prompt,
                     [dict(tipo="dims_total", ancho=W, fondo=D, alto=k * Pv * H),
                      dict(tipo="escalonado", niveles=k, retiro=s)], code, neg=neg)

    # ---- edición
    def edicion(self, n=25):
        r = self.r
        for i in range(n):
            W, D, P = self.dims()
            spec = dict(ancho=W, fondo=D, alto=P * H)
            base = CAB + edificio_code(W, D, P)
            kind = i % 5
            cara = list(CARAS)[(i // 5) % 4]
            ct = r.choice(CARAS[cara])
            if kind == 0:
                k = r.randint(1, P - 1)
                ins = f"Agrega un balcón en voladizo de 3 x 1.5 metros con baranda en {ct}, a la altura del {ORD[k]}."
                ck = [dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6),
                      dict(tipo="no_cara", cara=OPUESTA[cara], vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6)]
                code = base + losa_en_cara(cara, W, D, k * H, 3, 1.5, "Balcon")
                neg = base + losa_en_cara(OPUESTA[cara], W, D, k * H, 3, 1.5, "Balcon")
                sub = "agregar_cara"
            elif kind == 1:
                th = r.choice([20, 30, 45, 60])
                ins = f"Gira el edificio {th} grados en sentido antihorario alrededor del eje vertical."
                ck = [dict(tipo="rotacion", grados=th, tol=5)]
                code = base + f"ed.rotation_euler.z = math.radians({th})\n"
                sub = "rotar"
                neg = base
            elif kind == 2:
                origen = "frontal" if cara != "frontal" else "trasera"
                k = r.randint(1, P - 1)
                base = base + losa_en_cara(origen, W, D, k * H, 3, 1.5, "Balcon")
                ins = f"Mueve el balcón (losa y baranda) a {ct}, a la misma altura."
                ck = [dict(tipo="cara", cara=cara, vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6),
                      dict(tipo="no_cara", cara=origen, vuelo_min=0.8, z_min=k * H - 0.6, z_max=k * H + 0.6)]
                code = CAB + edificio_code(W, D, P) + losa_en_cara(cara, W, D, k * H, 3, 1.5, "Balcon")
                sub = "mover_cara"
                neg = base
            elif kind == 3:
                a, b = r.choice([3, 4]), r.choice([3, 4])
                ins = f"Agrega sobre la cubierta, centrado, un volumen de {a} x {b} metros y 3 metros de alto."
                ck = [dict(tipo="encima", ancho=a, fondo=b, alto=3)]
                code = base + edificio_code(a, b, 1, "Atico", (W / 2 - a / 2, D / 2 - b / 2, 0), var="atico") + \
                    f"atico.location.z = {P * H + 0.2:g}\n"
                sub = "encima"
                neg = base
            else:
                g = r.choice([6, 8, 10])
                ins = (f"Agrega un segundo edificio de 2 pisos de 8 x 6 metros al {CARDINAL[cara]} del existente, "
                       f"separado {g} metros entre fachadas y alineado por el centro.")
                o = {"derecha": (W + g, D / 2 - 3), "izquierda": (-g - 8, D / 2 - 3),
                     "trasera": (W / 2 - 4, D + g), "frontal": (W / 2 - 4, -g - 6)}[cara]
                ck = [dict(tipo="separacion", otro=dict(ancho=8, fondo=6, alto=6), cara=cara, gap=g)]
                code = base + edificio_code(8, 6, 2, "Edificio2", (o[0], o[1], 0), "ed2")
                o2 = {"derecha": (W + 2 * g, D / 2 - 3), "izquierda": (-2 * g - 8, D / 2 - 3),
                      "trasera": (W / 2 - 4, D + 2 * g), "frontal": (W / 2 - 4, -2 * g - 6)}[cara]
                neg = base + edificio_code(8, 6, 2, "Edificio2", (o2[0], o2[1], 0), "ed2")
                sub = "agregar_edificio"
            self.add("edicion", sub, ins, [dict(tipo="dims", **spec)] + ck, code, base=base, edificio=spec, neg=neg)


def math_tan(g):
    import math
    return math.tan(math.radians(g))


def mono_pendiente_code(W, D, z0, rise, cara):
    """Techo de una pendiente con bmesh: prisma cuya cara superior baja hacia 'cara'."""
    # alturas en las 4 esquinas (x0y0, x1y0, x1y1, x0y1)
    zl, zh = z0 + 0.2, z0 + 0.2 + rise
    hz = {"frontal": (zl, zl, zh, zh), "trasera": (zh, zh, zl, zl),
          "izquierda": (zl, zh, zh, zl), "derecha": (zh, zl, zl, zh)}[cara]
    return f"""
me = bpy.data.meshes.new('TechoMono')
bm = bmesh.new()
pts = [(-0.3, -0.3), ({W + 0.3}, -0.3), ({W + 0.3}, {D + 0.3}), (-0.3, {D + 0.3})]
hz = {hz}
bot = [bm.verts.new((x, y, {z0})) for x, y in pts]
top = [bm.verts.new((x, y, z)) for (x, y), z in zip(pts, hz)]
bm.faces.new(bot[::-1]); bm.faces.new(top)
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new((bot[i], bot[j], top[j], top[i]))
bm.normal_update(); bm.to_mesh(me); bm.free()
techo = bpy.data.objects.new('TechoMono', me)
bpy.context.collection.objects.link(techo)
"""


def main():
    g = Gen()
    g.cara(); g.cada_piso(); g.encima(); g.rotacion(); g.separacion(); g.formas(); g.edicion()
    od = os.path.join(HERE, "oraculo")
    os.makedirs(od, exist_ok=True)
    with open(os.path.join(HERE, "tareas.jsonl"), "w") as fo:
        for t in g.tareas:
            with open(os.path.join(od, f"{t['id']}__oraculo.py"), "w") as fc:
                fc.write(t["oraculo"])
            if t["negativo"]:
                with open(os.path.join(od, f"{t['id']}__negativo.py"), "w") as fc:
                    fc.write(t["negativo"])
            fo.write(json.dumps({k: v for k, v in t.items() if k not in ("oraculo", "negativo")}, ensure_ascii=False) + "\n")
    from collections import Counter
    print(len(g.tareas), "tareas", dict(Counter(t["categoria"] for t in g.tareas)))


if __name__ == "__main__":
    main()
