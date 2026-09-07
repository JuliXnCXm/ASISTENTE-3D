"""
config.py — Rutas y parámetros centralizados del sistema RAG.
Todos los demás módulos importan desde aquí.
"""
from pathlib import Path
import os

# ── Raíz del proyecto ─────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent   # TESIS_1/

# ── Fuentes de conocimiento ───────────────────────────────────────────────────
KB_DIR        = ROOT / "RAG" / "knowledge_base"     # archivos .md
DSL_FILE      = ROOT / "DSL" / "blender" / "blender_arch.py"
DATASET_FILE  = ROOT / "DATASET" / "dataset_creation_v1.json"

# ── Vector store (ChromaDB o pgvector) ────────────────────────────────────────
VECTOR_STORE_PROVIDER = os.environ.get("VECTOR_STORE_PROVIDER", "chroma")
CHROMA_DIR    = ROOT / "RAG" / "vector_store"       # persistencia local en disco
PG_CONN_STR   = os.environ.get("PG_CONN_STR", "")

# Nombres de colecciones dentro del vector store
COLLECTION_KB       = "knowledge_base"    # docs .md + funciones DSL
COLLECTION_DATASET  = "dataset_examples"  # ejemplos {prompt → code}

# ── Modelo de embeddings ──────────────────────────────────────────────────────
# Multilingüe (español + inglés) — 384 dimensiones — ~120 MB
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ── Parámetros de retrieval ───────────────────────────────────────────────────
TOP_K_KB       = 3   # chunks de conocimiento a recuperar
TOP_K_DATASET  = 2   # ejemplos del dataset a recuperar como few-shot
