import torch
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
from config import QUERY_MODEL, DEVICE

class QueryEncoder:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(QUERY_MODEL)
        self.model = AutoModel.from_pretrained(QUERY_MODEL).to(DEVICE)
        self.model.eval()
    
    def encode_query(self, query):
        """Encode query using MedCPT Query Encoder"""
        encoded = self.tokenizer(
            [query],
            truncation=True,
            padding=True,
            return_tensors="pt",
            max_length=64
        )
        
        encoded = {key: value.to(DEVICE) for key, value in encoded.items()}
        
        with torch.no_grad():
            output = self.model(**encoded)
        
        query_embedding = output.last_hidden_state[:, 0, :]
        query_embedding = query_embedding.detach().cpu().numpy().astype("float32")
        faiss.normalize_L2(query_embedding)
        
        return query_embedding