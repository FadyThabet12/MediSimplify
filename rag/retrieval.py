# import pickle
# import faiss
# import numpy as np
# from pathlib import Path
# from config import MODEL_PATHS
# from rag.embeddings import QueryEncoder

# class MedicalRetriever:
#     def __init__(self):
#         self.encoder = QueryEncoder()
        
#         # Load FAISS index
#         index_path = Path(MODEL_PATHS['rag_index'])
#         self.index = faiss.read_index(str(index_path))
#         # Load documents
#         metadata_path = Path(MODEL_PATHS['rag_metadata'])
#         with open(metadata_path, 'rb') as f:
#             self.documents = pickle.load(f)
    
#     def retrieve(self, query, k=5):
#         """Retrieve relevant medical documents"""
#         query_embedding = self.encoder.encode_query(query)
        
#         scores, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
#         results = []
#         for score, idx in zip(scores[0], indices[0]):
#             doc = self.documents[int(idx)]
#             results.append({
#                 "score": float(score),
#                 "id": doc["id"],
#                 "title": doc["title"],
#                 "text": doc["text"],
#                 "source": doc["source"],
#                 "category": doc["category"]
#             })
        
#         return results
import pickle
import faiss
import re
from pathlib import Path
from config import MODEL_PATHS
from rag.embeddings import QueryEncoder

# Stopwords for lexical matching
STOPWORDS = {
    "what", "are", "the", "a", "an", "of", "is", "for", "and", "what's",
    "common", "symptoms", "symptom", "sign", "signs", "with", "to", "in",
    "does", "do", "can", "cause", "causes", "how", "why", "which", "please",
    "ما", "هي", "هو", "من", "ل", "ال", "ماهي", "اعراض", "أعراض", "ماهي"
}

# Intent terms for reranking
INTENT_TERMS = {
    "symptoms": [
        "symptom", "symptoms", "sign", "signs", "presentation", "manifestation",
        "feature", "features", "sensitivity", "nausea", "vomiting", "aura",
        "throbbing", "pulsing", "pain", "photophobia", "phonophobia", "visual",
        "light", "sound", "movement", "headache", "weakness", "fever", "rash"
    ],
    "causes": ["cause", "causes", "etiology", "due to", "caused by", "risk factor", "risk factors"],
    "diagnosis": ["diagnosis", "diagnostic", "diagnose", "test", "tests", "imaging", "criteria"],
    "treatment": ["treatment", "treat", "therapy", "management", "managed", "medication", "drug", "drugs"],
    "complications": ["complication", "complications", "sequela", "sequelae", "adverse"],
    "prevention": ["prevent", "prevention", "avoid", "prophylaxis", "prophylactic"],
    "general": []
}

QUESTION_INTENT_PATTERNS = {
    "symptoms": [
        r"\bwhat\s+(?:are|is)\s+(?:the\s+)?(?:common\s+)?symptoms?\b",
        r"\b(?:symptoms?|signs?|clinical features?|manifestations?)\b",
        r"\bwhat\s+does\s+.+\s+(?:feel|look)\s+like\b",
        r"(?:ما|ايه|إيه).*?(?:اعراض|أعراض|علامات|علاماته|علاماتها)"
    ],
    "causes": [r"\bwhat\s+(?:causes?|is the cause of)\b", r"\bcauses?\b", r"\betiology\b", r"(?:سبب|أسباب|مسببات)"],
    "diagnosis": [r"\bhow\s+is\s+.+\s+diagnos", r"\bdiagnos(?:is|tic|e)\b", r"(?:تشخيص|كيف يتم التشخيص)"],
    "treatment": [r"\bhow\s+is\s+.+\s+treat", r"\btreatment\b", r"\btherapy\b", r"(?:علاج|العلاج)"],
    "complications": [r"\bcomplications?\b", r"(?:مضاعفات)"],
    "prevention": [r"\bprevention\b", r"\bprevent\b", r"(?:الوقاية|يمنع|منع)"],
}

class MedicalRetriever:
    def __init__(self):
        self.encoder = QueryEncoder()
        
        # Load FAISS index
        index_path = Path(MODEL_PATHS['rag_index'])
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        self.index = faiss.read_index(str(index_path))
        
        # Load documents
        metadata_path = Path(MODEL_PATHS['rag_metadata'])
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")
        with open(metadata_path, 'rb') as f:
            self.documents = pickle.load(f)
        
        print(f"✅ Loaded {len(self.documents)} documents")
        print(f"✅ FAISS index loaded with {self.index.ntotal} vectors")
    
    def clean_document_text(self, text):
        """Keep the medical answer/context and remove MCQ question/title noise."""
        text = str(text or "").strip()
        # If an explicit medical-context marker exists, use only what follows it.
        for marker in ["Medical context:", "medical context:", "Context:", "context:"]:
            if marker in text:
                text = text.split(marker, 1)[1].strip()
                break
        # Remove leading MCQ Q: ... A: prefix, but preserve the answer after A:.
        if re.search(r"\bQ\s*:", text, flags=re.I) and re.search(r"\bA\s*:", text, flags=re.I):
            m = re.search(r"\bA\s*:\s*", text, flags=re.I)
            if m:
                text = text[m.end():].strip()
        return text
    
    def lexical_tokens(self, text):
        tokens = re.findall(r"[a-zA-Z][a-zA-Z'-]+", str(text).lower())
        return {t for t in tokens if len(t) > 2 and t not in STOPWORDS}
    
    def question_intent(self, question):
        q = str(question).strip().lower()
        for intent, patterns in QUESTION_INTENT_PATTERNS.items():
            if any(re.search(p, q) for p in patterns):
                return intent
        return "general"
    
    def rerank_results(self, query, candidates, final_k=5):
        """Re-rank results using intent and lexical matching"""
        intent = self.question_intent(query)
        q_tokens = self.lexical_tokens(query)
        dense_scores = [r["score"] for r in candidates]
        lo, hi = min(dense_scores), max(dense_scores)
        
        for r in candidates:
            text = self.clean_document_text(r["text"])
            low = text.lower()
            dense_norm = (r["score"] - lo) / (hi - lo + 1e-8)
            doc_tokens = self.lexical_tokens(text)
            lexical = len(q_tokens & doc_tokens) / max(1, len(q_tokens))
            intent_hits = sum(1 for term in INTENT_TERMS.get(intent, []) if term in low)
            intent_score = min(intent_hits / (4 if intent == "symptoms" else 3), 1.0)
            
            # Penalize obvious generic/non-answer MCQ metadata for intent questions
            penalty = 0.0
            if intent == "symptoms" and any(x in low for x in ["most common", "second most common", "vascular", "benign", "triggers", "activators"]):
                penalty += 0.08
            
            r["rerank_score"] = 0.55 * dense_norm + 0.20 * lexical + 0.25 * intent_score - penalty
            r["clean_text"] = text
            r["intent"] = intent
        
        return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:final_k]
    
    def retrieve(self, query, k=5):
        """Retrieve and re-rank relevant medical documents"""
        query_embedding = self.encoder.encode_query(query)
        
        candidate_k = min(20, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, candidate_k)
        
        candidates = []
        for score, idx in zip(scores[0], indices[0]):
            doc = self.documents[int(idx)]
            candidates.append({
                "score": float(score),
                "id": doc.get("id", idx),
                "title": doc.get("title", ""),
                "text": doc.get("text", ""),
                "source": doc.get("source", ""),
                "category": doc.get("category", "")
            })
        
        # Apply re-ranking
        results = self.rerank_results(query, candidates, final_k=min(k, len(candidates)))
        
        # Convert back to clean format
        final_results = []
        for r in results:
            final_results.append({
                "score": r["score"],
                "rerank_score": r["rerank_score"],
                "id": r["id"],
                "title": r["title"],
                "text": r.get("clean_text", r["text"]),
                "source": r["source"],
                "category": r["category"]
            })
        
        return final_results
    