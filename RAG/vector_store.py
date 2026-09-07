import abc
import os

class VectorStore(abc.ABC):
    @abc.abstractmethod
    def upsert_chunks(self, collection_name: str, chunks: list[dict], batch_size: int = 64):
        pass

    @abc.abstractmethod
    def search(self, collection_name: str, query: str, top_k: int, filters: dict = None) -> list[dict]:
        pass

    @abc.abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abc.abstractmethod
    def count(self, collection_name: str) -> int:
        pass


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: str, embedding_model: str):
        import chromadb
        from chromadb.utils import embedding_functions
        self.client = chromadb.PersistentClient(path=persist_directory)
        self._ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

    def _get_collection(self, name: str):
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert_chunks(self, collection_name: str, chunks: list[dict], batch_size: int = 64):
        col = self._get_collection(collection_name)
        total = len(chunks)
        for i in range(0, total, batch_size):
            batch = chunks[i: i + batch_size]
            col.upsert(
                ids=[c["id"] for c in batch],
                documents=[c["text"] for c in batch],
                metadatas=[c["metadata"] for c in batch],
            )
            print(f"    {min(i + batch_size, total)}/{total} chunks indexados en {collection_name}...")

    def search(self, collection_name: str, query: str, top_k: int, filters: dict = None) -> list[dict]:
        col = self._get_collection(collection_name)
        res = col.query(
            query_texts=[query],
            n_results=top_k,
            where=filters
        )
        out = []
        if res["ids"]:
            for i in range(len(res["ids"][0])):
                out.append({
                    "id": res["ids"][0][i],
                    "text": res["documents"][0][i],
                    "metadata": res["metadatas"][0][i],
                    "score": res["distances"][0][i]
                })
        return out

    def delete_collection(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass

    def count(self, collection_name: str) -> int:
        try:
            return self._get_collection(collection_name).count()
        except Exception:
            return 0


class PgVectorStore(VectorStore):
    def __init__(self, connection_string: str, embedding_model: str):
        self.connection_string = connection_string
        self.embedding_model = embedding_model
        # Here we would initialize the psycopg2 connection and the sentence-transformers model
        # For now, it's a stub to demonstrate the interface.
        pass

    def upsert_chunks(self, collection_name: str, chunks: list[dict], batch_size: int = 64):
        raise NotImplementedError("PgVectorStore not fully implemented yet")

    def search(self, collection_name: str, query: str, top_k: int, filters: dict = None) -> list[dict]:
        raise NotImplementedError("PgVectorStore not fully implemented yet")

    def delete_collection(self, collection_name: str):
        raise NotImplementedError("PgVectorStore not fully implemented yet")

    def count(self, collection_name: str) -> int:
        raise NotImplementedError("PgVectorStore not fully implemented yet")


def get_vector_store(provider: str, persist_directory: str, embedding_model: str, pg_conn_str: str = "") -> VectorStore:
    if provider.lower() == "chroma":
        return ChromaVectorStore(persist_directory, embedding_model)
    elif provider.lower() == "pgvector":
        return PgVectorStore(pg_conn_str, embedding_model)
    else:
        raise ValueError(f"Unknown vector store provider: {provider}")
