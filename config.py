# import torch
# # Device
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # Model Paths
# MODEL_PATHS = {
#     'text': 'Models/text_model/model.keras',
#     'image': 'Models/image_model/model.keras',
#     'rag_index': 'Models/rag_model/faiss.index',
#     'rag_metadata': 'Models/rag_model/metadata.pkl'
# }

# # Image Labels
# LABELS = [
#     "No Finding",
#     "Enlarged Cardiomediastinum",
#     "Cardiomegaly",
#     "Lung Opacity",
#     "Lung Lesion",
#     "Edema",
#     "Consolidation",
#     "Pneumonia",
#     "Atelectasis",
#     "Pneumothorax",
#     "Pleural Effusion",
#     "Pleural Other",
#     "Fracture",
#     "Support Devices"
# ]

# # Translation Model
# # TRANSLATION_MODEL = "facebook/nllb-200-distilled-600M"
# TRANSLATION_MODEL = "facebook/m2m100_418M"
# # RAG Model
# QUERY_MODEL = "ncbi/MedCPT-Query-Encoder"
# LLM_MODEL = "google/flan-t5-small"
# ______________________________________________________________________________________
# import torch
# # Device
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Model Paths
# MODEL_PATHS = {
#     'text': 'Models/text_model/model.keras',
#     'text_tokenizer': 'Models/text_model/tokenizer.pkl',
#     'image': 'Models/image_model/pytorch_model.safetensors',
#     'rag_index': 'Models/rag_model/faiss.index',
#     'rag_metadata': 'Models/rag_model/metadata.pkl'
# }

# # Image Labels
# LABELS = [
#     "No Finding",
#     "Enlarged Cardiomediastinum",
#     "Cardiomegaly",
#     "Lung Opacity",
#     "Lung Lesion",
#     "Edema",
#     "Consolidation",
#     "Pneumonia",
#     "Atelectasis",
#     "Pneumothorax",
#     "Pleural Effusion",
#     "Pleural Other",
#     "Fracture",
#     "Support Devices"
# ]

# # Translation Model - استخدم m2m100
# TRANSLATION_MODEL = "facebook/m2m100_418M"

# # RAG Model
# QUERY_MODEL = "ncbi/MedCPT-Query-Encoder"
# LLM_MODEL = "google/flan-t5-small"

# # OCR Settings
# OCR_LANGUAGE = "ara+eng"
#______________________________________________________
import torch

# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model Paths
MODEL_PATHS = {
    'text': 'Models/text_model/model.keras',
    'chest': 'Models/image_model/chest_model.pth',
    'bone': 'Models/image_model/bone_model.pth',
    'rag_index': 'Models/rag_model/faiss.index',
    'rag_metadata': 'Models/rag_model/metadata.pkl'
}

# Chest X-Ray Labels (14 classes)
CHEST_LABELS = [
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

# Bone X-Ray Labels
BONE_LABELS = [
    "No Finding",
    "Fracture",
    "Dislocation",
    "Arthritis",
    "Osteoporosis",
    "Bone Tumor",
    "Infection",
    "Deformity",
    "Joint Effusion",
    "Soft Tissue Swelling",
    "Foreign Body",
    "Normal Variant"
]

# ⚠️ IMPORTANT: Keep LABELS for compatibility
LABELS = CHEST_LABELS

# Translation Model
TRANSLATION_MODEL = "facebook/m2m100_418M"

# RAG Model
QUERY_MODEL = "ncbi/MedCPT-Query-Encoder"
LLM_MODEL = "google/flan-t5-small"

# OCR Settings
OCR_LANGUAGE = "ara+eng"