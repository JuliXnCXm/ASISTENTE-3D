"""
ingest.py — Pipeline de indexación del RAG.

Lee tres tipos de fuentes, las trocea en chunks semánticos,
genera embeddings y los guarda en ChromaDB (local).

Fuentes:
  1. Archivos .md en RAG/knowledge_base/   → chunk por sección H2
  2. DSL/blender/blender_arch.py           → chunk por función pública (docstring + firma)
  3. DATASET/dataset.json                  → chunk por ejemplo {prompt, python_code}

Uso:
  python ingest.py                  # indexa todo (incremental)
  python ingest.py --reset          # borra todo y re-indexa
  python ingest.py --reset-kb       # solo reconstruye knowledge_base
  python ingest.py --reset-dataset  # solo reemplaza los ejemplos del dataset
"""

import ast
import argparse
import json
import re
import textwrap
from pathlib import Path

# ── No chromadb en root, se maneja por interface ──

from config import (
    KB_DIR, DSL_FILE, DATASET_FILE, CHROMA_DIR,
    COLLECTION_KB, COLLECTION_DATASET, EMBEDDING_MODEL,
    VECTOR_STORE_PROVIDER, PG_CONN_STR
)
from vector_store import get_vector_store

# ---------------------------------------------------------
#  1. CHUNKING — Archivos Markdown
# ---------------------------------------------------------

def chunk_markdown(path: Path) -> list[dict]:
    """
    Divide un archivo .md en chunks por sección H2 (## Título).
    Cada chunk incluye el título de la sección como primera línea.

    Retorna lista de dicts:
        {id, text, metadata: {source, type, section}}
    """
    text = path.read_text(encoding="utf-8")
    # Separar por headings H2
    partes = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    chunks = []
    source = path.name

    for parte in partes:
        parte = parte.strip()
        if not parte:
            continue

        # Extraer título de la sección (primera línea)
        lineas = parte.splitlines()
        titulo = lineas[0].lstrip("#").strip() if lineas else "intro"

        # Ignorar la cabecera del documento (antes del primer H2)
        if not parte.startswith("## "):
            titulo = "introduccion"

        chunk_id = f"{source}__{titulo.lower().replace(' ', '_')[:50]}"

        chunks.append({
            "id":   chunk_id,
            "text": parte,
            "metadata": {
                "source":  source,
                "type":    "knowledge_base",
                "section": titulo,
            },
        })

    return chunks


# ---------------------------------------------------------
#  2. CHUNKING — DSL (blender_arch.py vía AST)
# ---------------------------------------------------------

def chunk_dsl(path: Path) -> list[dict]:
    """
    Extrae cada función pública de blender_arch.py como un chunk.
    El texto del chunk es: firma de la función + docstring completo.

    Retorna lista de dicts:
        {id, text, metadata: {source, type, function_name}}
    """
    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)
    lines = source_code.splitlines()

    # Leer __all__ para quedarnos solo con funciones públicas
    all_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, ast.List):
                        all_names = {
                            elt.s for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        }

    chunks = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name not in all_names:
            continue

        # Reconstruir la firma a partir del código fuente
        # (de la línea def hasta el cierre del paréntesis)
        firma_lineas = []
        for i in range(node.lineno - 1, min(node.lineno + 20, len(lines))):
            firma_lineas.append(lines[i])
            if lines[i].rstrip().endswith(":"):
                break
        firma = "\n".join(firma_lineas)

        # Docstring
        docstring = ast.get_docstring(node) or "(sin documentación)"
        docstring = textwrap.dedent(docstring)

        texto = f"FUNCIÓN: {node.name}\n\n{firma}\n\n{docstring}"

        chunks.append({
            "id":   f"dsl__{node.name}",
            "text": texto,
            "metadata": {
                "source":        "blender_arch.py",
                "type":          "dsl_function",
                "function_name": node.name,
            },
        })

    print(f"  [DSL] {len(chunks)} funciones públicas extraídas de {path.name}")
    return chunks


# ---------------------------------------------------------
#  3. CHUNKING — Dataset de ejemplos
# ---------------------------------------------------------

def chunk_dataset(path: Path) -> list[dict]:
    """
    Convierte cada ejemplo del dataset en un chunk.

    El texto a embedir es SOLO el PROMPT (en español), porque en retrieval
    el query del usuario también será un prompt, evitando ruido del código.
    El código se guarda en los metadatos para usarlo como few-shot.
    Solo se indexan ejemplos del split 'train'.

    Retorna lista de dicts:
        {id, text, metadata: {source, type, domain, category, complexity}}
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    items: dict = data.get("items", {})

    chunks = []
    for item_id, item in items.items():
        if item.get("split") != "train":
            continue

        prompt      = item.get("prompt", "").strip()
        code        = item.get("python_code", "").strip()
        domain      = item.get("domain", "")
        category    = item.get("category", "")
        complexity  = item.get("complexity", "")

        if not prompt or not code:
            continue

        chunks.append({
            "id":   f"dataset__{item_id}",
            "text": prompt,
            "metadata": {
                "source":     path.name,
                "type":       "dataset_example",
                "domain":     domain,
                "category":   category,
                "complexity": complexity,
                "python_code": code,
            },
        })

    print(f"  [Dataset] {len(chunks)} ejemplos de 'train' cargados desde {path.name}")
    return chunks


# ---------------------------------------------------------
#  5. ENTRY POINT
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="RAG ingest pipeline")
    parser.add_argument("--reset",         action="store_true",
                        help="Borra y re-indexa TODO")
    parser.add_argument("--reset-kb",      action="store_true",
                        help="Borra y re-indexa solo knowledge_base (md + DSL)")
    parser.add_argument("--reset-dataset", action="store_true",
                        help="Borra y re-indexa solo los ejemplos del dataset")
    args = parser.parse_args()

    # ── Conectar al Vector Store ──────────────
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    vstore = get_vector_store(VECTOR_STORE_PROVIDER, str(CHROMA_DIR), EMBEDDING_MODEL, PG_CONN_STR)

    # ── Colección: knowledge_base (md + DSL) ───────────────────────────────
    if args.reset or args.reset_kb:
        print(f"\n[→] Borrando colección '{COLLECTION_KB}'...")
        vstore.delete_collection(COLLECTION_KB)

    if args.reset or args.reset_kb or vstore.count(COLLECTION_KB) == 0:
        print(f"\n[1/2] Indexando knowledge_base...")

        # Archivos .md
        md_chunks = []
        for md_file in sorted(KB_DIR.glob("*.md")):
            chunks = chunk_markdown(md_file)
            md_chunks.extend(chunks)
            print(f"  [MD] {md_file.name}: {len(chunks)} chunks")

        # Funciones DSL
        dsl_chunks = chunk_dsl(DSL_FILE)

        all_kb_chunks = md_chunks + dsl_chunks
        print(f"\n  Total knowledge_base: {len(all_kb_chunks)} chunks")
        vstore.upsert_chunks(COLLECTION_KB, all_kb_chunks)
    else:
        print(f"\n[1/2] knowledge_base ya indexada ({vstore.count(COLLECTION_KB)} chunks). "
              f"Usa --reset-kb para re-indexar.")

    # ── Colección: dataset_examples ────────────────────────────────────────
    if args.reset or args.reset_dataset:
        print(f"\n[→] Borrando colección '{COLLECTION_DATASET}'...")
        vstore.delete_collection(COLLECTION_DATASET)

    if args.reset or args.reset_dataset or vstore.count(COLLECTION_DATASET) == 0:
        print(f"\n[2/2] Indexando dataset de ejemplos...")
        ds_chunks = chunk_dataset(DATASET_FILE)
        vstore.upsert_chunks(COLLECTION_DATASET, ds_chunks)
    else:
        print(f"\n[2/2] Dataset ya indexado ({vstore.count(COLLECTION_DATASET)} ejemplos). "
              f"Usa --reset-dataset para re-indexar.")

    # ── Resumen final ──────────────────────────────────────────────────────
    print(f"""
INGEST COMPLETADO
knowledge_base : {vstore.count(COLLECTION_KB):>5} chunks
dataset_examples: {vstore.count(COLLECTION_DATASET):>4} chunks
Provider       : {VECTOR_STORE_PROVIDER:<22}
""")


if __name__ == "__main__":
    main()
