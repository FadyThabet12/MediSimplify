import pickle
import faiss
import numpy as np
from pathlib import Path
from config import MODEL_PATHS
from rag.embeddings import QueryEncoder

class MedicalRetriever:
    def __init__(self):
        self.encoder = QueryEncoder()
        
        # Load FAISS index
        index_path = Path(MODEL_PATHS['rag_index'])
        self.index = faiss.read_index(str(index_path))
        # Load documents
        metadata_path = Path(MODEL_PATHS['rag_metadata'])
        with open(metadata_path, 'rb') as f:
            self.documents = pickle.load(f)
    
    def retrieve(self, query, k=5):
        """Retrieve relevant medical documents"""
        query_embedding = self.encoder.encode_query(query)
        
        scores, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            doc = self.documents[int(idx)]
            results.append({
                "score": float(score),
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "source": doc["source"],
                "category": doc["category"]
            })
        
        return results