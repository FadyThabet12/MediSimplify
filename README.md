# MediSimplify
@"
# 🏥 MediSimplify

An AI-powered medical assistant that simplifies complex medical information for patients and healthcare professionals.



---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Medical Q&A** | Ask medical questions and get patient-friendly answers using RAG (Retrieval-Augmented Generation) |
| 🩻 **X-Ray Analysis** | Upload chest X-rays for AI-powered diagnosis support with CheXpert model |
| 📄 **OCR Report Analysis** | Extract and understand medical reports from images (Arabic & English) |
| 🔥 **Grad-CAM Visualization** | See what the AI focuses on in X-rays with heatmap visualization |
| 🌍 **Bilingual Support** | Ask questions in Arabic or English, get answers in your language |
| 🏥 **Patient-Friendly** | Complex medical terms explained in simple language |

---
#📁 Project Structure
MediSimplify/
│
├── app.py                  # Main Streamlit application
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
│
├── pages/                  # Streamlit pages
│   ├── home.py            # Home page
│   ├── medical_qa.py      # Medical Q&A page
│   ├── image_analysis.py  # X-Ray analysis page
│   └── ocr_report.py      # Medical report OCR page
│
├── rag/                    # RAG pipeline
│   ├── embeddings.py      # Query embedding generation
│   ├── retrieval.py       # Document retrieval with FAISS
│   └── pipeline.py        # Complete RAG pipeline
│
├── utils/                  # Utilities
│   ├── helpers.py         # Helper functions
│   └── preprocessing.py   # Data preprocessing
│
└── OCR/                    # Medical report OCR
    ├── extractor.py       # Text extraction from images
    └── processor.py       # Medical information extraction
## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Tesseract OCR (for medical report extraction)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/FadyThabet12/MediSimplify.git
cd MediSimplify

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki

# Install Tesseract OCR (Linux/Mac)
# sudo apt-get install tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng
# brew install tesseract tesseract-lang
