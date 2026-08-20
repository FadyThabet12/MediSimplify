# # 
# """
# embeddings.py
# Handles loading of MedCPT models and embedding generation
# """

# import torch
# import faiss
# import numpy as np
# from transformers import AutoTokenizer, AutoModel


# class MedicalEmbeddings:
#     """Handles MedCPT query encoding and embedding operations"""
    
#     def __init__(self, device=None):
#         self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.query_model_name = "ncbi/MedCPT-Query-Encoder"
#         self.query_tokenizer = None
#         self.query_encoder = None
#         self._load_query_encoder()
    
#     def _load_query_encoder(self):
#         """Load the MedCPT Query Encoder model"""
#         print("Loading MedCPT Query Encoder...")
#         self.query_tokenizer = AutoTokenizer.from_pretrained(self.query_model_name)
#         self.query_encoder = AutoModel.from_pretrained(self.query_model_name).to(self.device)
#         self.query_encoder.eval()
#         print("MedCPT Query Encoder loaded.")
    
#     def encode_query(self, query, max_length=64):
#         """
#         Encode a text query into an embedding vector
        
#         Args:
#             query (str): The query text to encode
#             max_length (int): Maximum token length
            
#         Returns:
#             numpy.ndarray: The query embedding (L2 normalized)
#         """
#         encoded = self.query_tokenizer(
#             [query],
#             truncation=True,
#             padding=True,
#             return_tensors="pt",
#             max_length=max_length
#         )
        
#         encoded = {key: value.to(self.device) for key, value in encoded.items()}
        
#         with torch.no_grad():
#             output = self.query_encoder(**encoded)
        
#         query_embedding = output.last_hidden_state[:, 0, :]
#         query_embedding = query_embedding.detach().cpu().numpy().astype("float32")
#         faiss.normalize_L2(query_embedding)
        
#         return query_embedding
    
#     def load_embeddings(self, embeddings_path):
#         """
#         Load pre-computed embeddings from file
        
#         Args:
#             embeddings_path (str): Path to the embeddings file (.pt)
            
#         Returns:
#             torch.Tensor: The loaded embeddings tensor
#         """
#         embeddings = torch.load(embeddings_path, map_location="cpu")
#         return embeddings
    
#     def extract_embedding_tensor(self, obj):
#         """
#         Extract embedding tensor from various object types
        
#         Args:
#             obj: The object containing embeddings
            
#         Returns:
#             torch.Tensor: The extracted tensor
#         """
#         if torch.is_tensor(obj):
#             return obj
        
#         if isinstance(obj, dict):
#             for key in ["embeddings", "dense_embeddings", "embedding", "embeds"]:
#                 if key in obj and torch.is_tensor(obj[key]):
#                     return obj[key]
            
#             for value in obj.values():
#                 if torch.is_tensor(value):
#                     return value
        
#         if isinstance(obj, (list, tuple)):
#             return torch.tensor(obj)
        
#         raise TypeError(f"Could not extract tensor from {type(obj)}")
    
#     def build_faiss_index(self, embedding_matrix):
#         """
#         Build a FAISS index from embedding matrix
        
#         Args:
#             embedding_matrix (numpy.ndarray): The embedding matrix
            
#         Returns:
#             faiss.Index: The FAISS index
#         """
#         dimension = embedding_matrix.shape[1]
#         index = faiss.IndexFlatIP(dimension)
#         index.add(embedding_matrix)
#         return index
    
#     def create_embedding_matrix(self, embeddings_obj):
#         """
#         Convert embeddings object to numpy matrix
        
#         Args:
#             embeddings_obj: The embeddings object
            
#         Returns:
#             numpy.ndarray: The embedding matrix
#         """
#         embedding_tensor = self.extract_embedding_tensor(embeddings_obj)
#         embedding_matrix = embedding_tensor.detach().cpu().numpy().astype("float32")
#         return embedding_matrix
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