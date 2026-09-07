from config import (
    COLLECTION_KB, COLLECTION_DATASET, EMBEDDING_MODEL,
    VECTOR_STORE_PROVIDER, CHROMA_DIR, PG_CONN_STR,
    TOP_K_KB, TOP_K_DATASET
)
from vector_store import get_vector_store

class Retriever:
    def __init__(self):
        self.vstore = get_vector_store(
            VECTOR_STORE_PROVIDER, 
            str(CHROMA_DIR), 
            EMBEDDING_MODEL, 
            PG_CONN_STR
        )

    def retrieve_context(self, query: str, filters: dict = None) -> dict:
        """
        Recupera documentación y ejemplos relevantes para una consulta.
        """
        # Recuperar conocimiento (API, normas, patrones)
        kb_results = self.vstore.search(
            collection_name=COLLECTION_KB,
            query=query,
            top_k=TOP_K_KB,
            filters=filters
        )
        
        # Recuperar ejemplos few-shot del dataset (train)
        dataset_results = self.vstore.search(
            collection_name=COLLECTION_DATASET,
            query=query,
            top_k=TOP_K_DATASET,
            filters=filters
        )
        
        return {
            "knowledge": kb_results,
            "examples": dataset_results
        }

    def format_prompt_context(self, retrieved: dict) -> str:
        """
        Formatea los resultados de recuperación en un string para el prompt del LLM.
        """
        context_parts = []
        
        if retrieved["knowledge"]:
            context_parts.append("=== DOCUMENTACIÓN Y REFERENCIA API ===")
            for i, doc in enumerate(retrieved["knowledge"], 1):
                source = doc['metadata'].get('source', 'unknown')
                context_parts.append(f"--- Documento {i} ({source}) ---")
                context_parts.append(doc['text'])
                
        if retrieved["examples"]:
            context_parts.append("\n=== EJEMPLOS DE REFERENCIA ===")
            for i, ex in enumerate(retrieved["examples"], 1):
                domain = ex['metadata'].get('domain', 'unknown')
                cat = ex['metadata'].get('category', 'unknown')
                code = ex['metadata'].get('python_code', '# sin código')
                context_parts.append(f"--- Ejemplo {i} ({domain} - {cat}) ---")
                context_parts.append(f"Instrucción: {ex['text']}")
                context_parts.append(f"Código Python:\n```python\n{code}\n```")
                
        return "\n".join(context_parts)

if __name__ == "__main__":
    # Test simple
    retriever = Retriever()
    res = retriever.retrieve_context("Crea una mesa rectangular de madera")
    print(retriever.format_prompt_context(res))
