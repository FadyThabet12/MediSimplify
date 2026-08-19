import torch
# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Model Paths
MODEL_PATHS = {
    'text': 'Models/text_model/model.keras',
    'image': 'Models/image_model/model.keras',
    'rag_index': 'Models/rag_model/faiss.index',
    'rag_metadata': 'Models/rag_model/metadata.pkl'
}

# Image Labels
LABELS = [
    "No Finding",
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity",
    "Lung Lesion",
    "Edema",
    "Consolidation",
    "Pneumonia",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
    "Pleural Other",
    "Fracture",
    "Support Devices"
]

# Translation Model
TRANSLATION_MODEL = "facebook/nllb-200-distilled-600M"

# RAG Model
QUERY_MODEL = "ncbi/MedCPT-Query-Encoder"
LLM_MODEL = "google/flan-t5-base"