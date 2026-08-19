# 🩺 MediSimplify
### AI-Powered Medical Document Simplification & Explanation

MediSimplify is an AI-powered medical assistant designed to simplify complex medical information and provide understandable explanations in **Arabic and English**.

The system accepts **medical images, PDF documents, and text**, extracts and preprocesses the medical information, analyzes it using AI models, and combines **Fine-Tuned Models** with **Retrieval-Augmented Generation (RAG)** to generate clear explanations.

> ⚠️ **Disclaimer:** MediSimplify is an educational and informational tool. It is not a substitute for professional medical advice, diagnosis, or treatment.

---

## 🚀 Project Overview

Medical reports often contain complex terminology that can be difficult for non-specialists to understand.

MediSimplify aims to bridge this gap by transforming medical documents into simple and understandable information.

The system follows this pipeline:

```text
                         USER
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
            Image         PDF          Text
              │            │            │
              └────────────┼────────────┘
                           ↓
                          OCR
                           ↓
                  Text Preprocessing
                           ↓
                 Medical Text Analysis
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
        Fine-Tuned Model                RAG
              │                         │
              │                  Medical Knowledge
              │                         │
              └────────────┬────────────┘
                           ↓
                    AI Explanation
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Summary    Key Findings     Terms
              │            │            │
              └────────────┼────────────┘
                           ↓
                    Arabic / English
                           ↓
                       Streamlit
```

---

## ✨ Features

* 📄 **PDF Processing**

  * Extract medical information from PDF documents.
  * Process PDF pages as images when necessary.
  * Support OCR for scanned medical documents.

* 🖼️ **Medical Image Processing**

  * Upload medical images.
  * Extract text using OCR.
  * Prepare extracted information for medical analysis.

* 📝 **Text Input**

  * Directly enter medical text or reports.
  * Preprocess the text before analysis.

* 🔍 **OCR**

  * Convert text from medical images and scanned PDFs into machine-readable text.

* 🧹 **Text Preprocessing**

  * Clean and normalize extracted medical text.
  * Prepare text for downstream AI models.

* 🧠 **Medical Text Analysis**

  * Analyze extracted medical information.
  * Identify important medical concepts and findings.

* 🤖 **Fine-Tuned Models**

  * Use specialized models trained/fine-tuned for medical text analysis.

* 📚 **RAG — Retrieval-Augmented Generation**

  * Retrieve relevant information from a medical knowledge base.
  * Combine retrieved knowledge with the AI model to improve explanations.

* 💡 **AI Explanation**

  * Generate simplified explanations of complex medical information.

* 📊 **Structured Results**

  * Generate:

    * Summary
    * Key Findings
    * Medical Terms
    * Simplified Explanations

* 🌍 **Bilingual Support**

  * 🇬🇧 English
  * 🇪🇬 Arabic

* 🖥️ **Streamlit Interface**

  * Simple and interactive web interface.

---

## 🏗️ System Architecture

The system consists of several main components:

### 1. Input Layer

The user can provide:

```text
Image
PDF
Text
```

These inputs are processed according to their type.

### 2. OCR Layer

Images and scanned PDFs are passed through OCR to extract readable text.

```text
Image / Scanned PDF
        ↓
       OCR
        ↓
   Extracted Text
```

### 3. Text Preprocessing

The extracted text is cleaned and prepared for analysis.

Typical preprocessing may include:

* Removing unnecessary characters
* Normalization
* Cleaning whitespace
* Text segmentation
* Medical terminology preparation

### 4. Medical Text Analysis

The processed text is passed to the medical NLP pipeline to identify relevant medical information.

### 5. Fine-Tuned Model

A fine-tuned model is used for specialized medical text understanding and generation.

```text
Medical Text
     ↓
Fine-Tuned Model
     ↓
Medical Understanding
```

### 6. RAG Pipeline

The RAG component retrieves relevant medical information from the knowledge base.

```text
User Query
    ↓
Embedding
    ↓
Vector Search
    ↓
Medical Knowledge Base
    ↓
Relevant Context
    ↓
AI Model
```

### 7. AI Explanation

The Fine-Tuned Model and retrieved RAG context are combined to produce a more informative explanation.

### 8. Output Layer

The system generates:

```text
Summary
Key Findings
Medical Terms
Explanation
```

The user can select:

```text
Arabic
English
```

---

## 📁 Project Structure

```text
MediSimplify/
│
├── Models/
│   ├── text_model/
│   ├── image_model/
│   └── rag_model/
│
├── notebooks/
│   ├── text_model.ipynb
│   ├── image_model.ipynb
│   └── rag_model.ipynb
│
├── pages/
│   ├── home.py
│   ├── medical_qa.py
│   └── ...
│
├── rag/
│   ├── retrieval.py
│   ├── embeddings.py
│   └── pipeline.py
│
├── utils/
│   ├── preprocessing.py
│   └── helpers.py
│
├── app.py
├── .gitignore
└── requirements.txt
```

### Notebooks

The `notebooks/` directory contains the experiments and training notebooks used to develop the models.

The trained models should be exported into the `Models/` directory for use by the Streamlit application.

For example:

```text
notebooks/
└── transformer_training.ipynb

        ↓

Models/
└── transformer/
    ├── model.keras
    ├── model_config.json
    └── tokenizer.pkl
```

---

## 🧰 Technologies Used

### Programming

* Python
* Jupyter Notebook

### Machine Learning & Deep Learning

* TensorFlow / Keras
* Scikit-learn
* Transformers
* Sentence Transformers

### NLP

* Natural Language Processing
* Text Embeddings
* Medical Text Classification
* Text Generation
* Fine-Tuning

### RAG

* FAISS
* Vector Embeddings
* Semantic Search
* Retrieval-Augmented Generation

### Document Processing

* PyMuPDF
* PIL
* OCR

### Application

* Streamlit

### Data Processing

* NumPy
* Pandas

---

## 🔄 End-to-End Workflow

```text
1. User uploads Image / PDF or enters Text
                    ↓
2. Input Processing
                    ↓
3. OCR (if required)
                    ↓
4. Text Extraction
                    ↓
5. Text Preprocessing
                    ↓
6. Medical Text Analysis
                    ↓
       ┌────────────┴────────────┐
       ↓                         ↓
 Fine-Tuned Model               RAG
       │                         │
       │                  Medical Knowledge
       │                         │
       └────────────┬────────────┘
                    ↓
             AI Explanation
                    ↓
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    Summary    Key Findings     Terms
                    ↓
             Language Selection
                    ↓
             Arabic / English
                    ↓
               Streamlit
```

---

## 📚 RAG Knowledge Base

The RAG component uses a medical knowledge base to retrieve relevant information.

The general process is:

```text
Medical Documents
       ↓
Document Processing
       ↓
Text Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
FAISS
```

When a user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
FAISS Similarity Search
   ↓
Relevant Medical Context
   ↓
AI Model
   ↓
Final Explanation
```

This allows the system to provide explanations based on retrieved medical knowledge instead of relying only on the model's internal knowledge.

---

## 🌐 Supported Languages

MediSimplify is designed to support:

| Language     | Support |
| ------------ | ------- |
| 🇬🇧 English | ✅       |
| 🇪🇬 Arabic  | ✅       |

The output can be generated and presented in the language selected by the user.

---

## 🖥️ Running the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MediSimplify
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
streamlit run app.py
```

The application will then open in your browser.

---

## 🤖 Models

The project uses multiple AI components depending on the task:

```text
Input
  │
  ├── OCR Model / Engine
  │
  ├── Medical NLP Model
  │
  ├── Fine-Tuned Model
  │
  └── RAG Pipeline
          │
          ├── Embedding Model
          └── FAISS Vector Store
```

> Model files can be stored separately from the source code when they are large. Configuration files, tokenizer files, indexes, and model weights should be included or referenced according to the deployment requirements.

---

## 📌 Future Improvements

* [ ] Improve Arabic medical terminology support.
* [ ] Add more medical document formats.
* [ ] Improve OCR accuracy for Arabic medical reports.
* [ ] Add more medical knowledge sources.
* [ ] Improve RAG retrieval quality.
* [ ] Add citation/reference support for retrieved information.
* [ ] Add medical report comparison.
* [ ] Add multilingual medical terminology extraction.
* [ ] Deploy the application online.
* [ ] Optimize models for faster inference.

---

## ⚠️ Medical Disclaimer

MediSimplify is intended for **educational and informational purposes only**.

The generated explanations should not be considered professional medical advice, diagnosis, or treatment recommendations.

Users should always consult a qualified healthcare professional for medical decisions.

---

## 👨‍💻 Project

**MediSimplify**
AI-Powered Medical Document Simplification & Explanation

Built with ❤️ using Python, NLP, Deep Learning, RAG, OCR, and Streamlit.
