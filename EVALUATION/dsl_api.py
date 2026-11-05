#!/usr/bin/env python3
"""
dsl_api.py
Conocimiento estático de la API del DSL `blender_arch` (sin importar bpy) para
inferencia aumentada:

  FIRMAS                         nombre -> {firma, doc, params, var_kw}
  validar_estatico(code)         errores de API antes de ejecutar (función inexistente,
                                 argumento inexistente, demasiados posicionales, sintaxis)
  RecuperadorFirmas.buscar(q,k)  RAG: las k firmas más parecidas a un texto (pedido del
                                 usuario o nombre inventado) con embeddings multilingües

Nada de esto toca el entrenamiento: solo usa el código fuente del DSL, que es
la documentación pública de la herramienta.
"""
import ast, os, re, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
DSL_FILE = os.path.join(os.path.dirname(HERE), "DSL", "blender", "blender_arch.py")
EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def _cargar_firmas(path=DSL_FILE):
    t = ast.parse(open(path, encoding="utf-8").read())
    out = {}
    for n in t.body:
        if not isinstance(n, ast.FunctionDef) or n.name.startswith("_"):
            continue
        a = n.args
        params = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
        doc = (ast.get_docstring(n) or "").strip()
        out[n.name] = dict(firma=f"A.{n.name}({ast.unparse(a)})", doc=doc.split("\n")[0].strip(),
                           doc_largo=doc, params=params, n_pos=len(a.posonlyargs + a.args),
                           var_kw=a.kwarg is not None, var_pos=a.vararg is not None)
    return out


FIRMAS = _cargar_firmas()


def alias_dsl(tree):
    """Nombres con los que el código importó blender_arch (normalmente 'A')."""
    al = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            al |= {x.asname or x.name for x in n.names if x.name == "blender_arch"}
    return al or {"A"}


def validar_estatico(code):
    """Lista de errores de API detectables sin ejecutar. [] = sin problemas."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [dict(tipo="sintaxis", msg=f"SyntaxError línea {e.lineno}: {e.msg}")]
    al, errs, vistos = alias_dsl(tree), [], set()
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name) and n.func.value.id in al):
            continue
        f = n.func.attr
        if f not in FIRMAS:
            if ("fn", f) not in vistos:
                errs.append(dict(tipo="funcion", nombre=f, linea=n.lineno,
                                 msg=f"línea {n.lineno}: la función A.{f} no existe en blender_arch"))
                vistos.add(("fn", f))
            continue
        s = FIRMAS[f]
        if not s["var_kw"]:
            for kw in n.keywords:
                if kw.arg and kw.arg not in s["params"] and (f, kw.arg) not in vistos:
                    errs.append(dict(tipo="argumento", nombre=f, arg=kw.arg, linea=n.lineno,
                                     msg=f"línea {n.lineno}: A.{f} no tiene el argumento '{kw.arg}'"))
                    vistos.add((f, kw.arg))
        if not s["var_pos"] and len([a for a in n.args if not isinstance(a, ast.Starred)]) > s["n_pos"]:
            errs.append(dict(tipo="posicionales", nombre=f, linea=n.lineno,
                             msg=f"línea {n.lineno}: A.{f} recibe como máximo {s['n_pos']} argumentos posicionales"))
    return errs


def sanear(code):
    """Corrección determinista (sin modelo): elimina de las llamadas A.f(...) los
    argumentos con nombre que f no acepta y los posicionales sobrantes.
    No inventa nada: solo quita lo que el DSL rechazaría. Devuelve (código, cambios)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code, []
    al, cambios = alias_dsl(tree), []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name) and n.func.value.id in al
                and n.func.attr in FIRMAS):
            continue
        s = FIRMAS[n.func.attr]
        if not s["var_kw"]:
            malos = [k.arg for k in n.keywords if k.arg and k.arg not in s["params"]]
            if malos:
                n.keywords = [k for k in n.keywords if not (k.arg and k.arg not in s["params"])]
                cambios += [f"A.{n.func.attr}: quitado '{m}'" for m in malos]
        pos = [a for a in n.args if not isinstance(a, ast.Starred)]
        if not s["var_pos"] and len(pos) == len(n.args) and len(n.args) > s["n_pos"]:
            cambios.append(f"A.{n.func.attr}: quitados {len(n.args) - s['n_pos']} posicionales sobrantes")
            n.args = n.args[:s["n_pos"]]
        # posicional y nombrado a la vez para el mismo parámetro -> TypeError: se quita el nombrado
        ocupados = set(s["params"][:len(n.args)])
        dup = [k.arg for k in n.keywords if k.arg in ocupados]
        if dup:
            n.keywords = [k for k in n.keywords if k.arg not in ocupados]
            cambios += [f"A.{n.func.attr}: quitado '{d}' duplicado" for d in dup]
    return (ast.unparse(tree) if cambios else code), cambios


def _tokens(t):
    return set(re.findall(r"[a-záéíóúñ]+", t.lower()))


class RecuperadorFirmas:
    """RAG sobre las firmas del DSL. Embeddings MiniLM multilingüe (CPU, ~120 MB);
    si no se puede cargar, cae a similitud léxica (difflib + tokens)."""

    def __init__(self, device="cpu"):
        self.nombres = sorted(FIRMAS)
        # dos vistas por función (nombre+resumen y docstring completo); score = máximo
        self.textos = [f"{n.replace('_', ' ')}: {FIRMAS[n]['doc']}" for n in self.nombres]
        self.textos_largos = [f"{n.replace('_', ' ')}: {FIRMAS[n]['doc_largo'][:400]}" for n in self.nombres]
        self.emb = None
        try:
            import torch
            from transformers import AutoTokenizer, BertModel
            self.torch = torch
            self.tok = AutoTokenizer.from_pretrained(EMB_MODEL)
            self.m = BertModel.from_pretrained(EMB_MODEL).to(device).eval()
            self.device = device
            self.emb = self.torch.stack([self._embed(self.textos), self._embed(self.textos_largos)])
        except Exception as e:  # pragma: no cover
            print(f"[dsl_api] embeddings no disponibles ({e}); uso similitud léxica")

    def _embed(self, textos):
        torch = self.torch
        with torch.no_grad():
            x = self.tok(textos, padding=True, truncation=True, max_length=128, return_tensors="pt").to(self.device)
            h = self.m(**x).last_hidden_state
            m = x["attention_mask"].unsqueeze(-1).float()
            v = (h * m).sum(1) / m.sum(1)
            return torch.nn.functional.normalize(v, dim=-1)

    def buscar(self, consulta, k=5, excluir=()):
        consulta = consulta.replace("_", " ")
        if self.emb is not None:
            s = (self.emb @ self._embed([consulta])[0]).max(0).values.tolist()
        else:
            q = _tokens(consulta)
            s = [len(q & _tokens(t)) / (1 + len(_tokens(t))) for t in self.textos]
        orden = sorted(range(len(self.nombres)), key=lambda i: -s[i])
        return [self.nombres[i] for i in orden if self.nombres[i] not in excluir][:k]

    def para_error(self, err, k=3):
        """Firmas útiles para corregir un error de validación estática o de ejecución."""
        if err.get("tipo") in ("argumento", "posicionales") and err.get("nombre") in FIRMAS:
            return [err["nombre"]]
        nombre = err.get("nombre")
        if not nombre:
            m = re.search(r"has no attribute '(\w+)'|unexpected keyword argument '(\w+)'|(\w+)\(\) ",
                          err.get("msg", ""))
            nombre = next((g for g in (m.groups() if m else ()) if g), None)
            if nombre in FIRMAS:
                return [nombre]
        if not nombre:
            return []
        cercanos = difflib.get_close_matches(nombre, self.nombres, n=2, cutoff=0.6)
        sem = self.buscar(nombre, k)
        return list(dict.fromkeys(cercanos + sem))[:k]


def formatear_firmas(nombres):
    return "\n".join(f"- {FIRMAS[n]['firma']}  # {FIRMAS[n]['doc']}" for n in nombres if n in FIRMAS)


if __name__ == "__main__":
    import sys
    r = RecuperadorFirmas()
    for q in ["crear_pared", "crear_bano", "crear_encimera", "crear_torre_n_pisos", "crear_hueco",
              "Diseña una cocina de 4x3 metros con mesón en L y una ventana"]:
        print(f"{q:60s} -> {r.buscar(q, 4)}")
    print(validar_estatico("import blender_arch as A\nA.crear_pared('x')\nA.crear_muro('m', foo=1)\n"))
