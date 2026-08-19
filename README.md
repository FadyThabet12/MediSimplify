# 🩺 MediSimplify

### AI-Powered Medical Document Simplification & Explanation

MediSimplify is an AI-powered application that helps users understand complex medical information using **OCR, Medical NLP, Fine-Tuned Models, and RAG**.

It accepts **images, PDF reports, and text**, analyzes the medical content, and provides simplified explanations in **Arabic or English**.

---

## 🏗️ Architecture

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
        Fine-Tuned Model               RAG
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

* 📄 Medical PDF processing
* 🖼️ Medical image analysis
* 🔍 OCR for medical reports
* 🧠 Medical text analysis
* 🤖 Fine-Tuned AI models
* 📚 RAG with FAISS
* 📝 Summary generation
* 🔎 Key findings extraction
* 📖 Medical terms explanation
* 🌍 Arabic & English support
* 🖥️ Streamlit interface

---

## 📁 Project Structure

```text
MediSimplify/
│
├── app.py                  # Main Streamlit application
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── README.md
│
├── pages/
│   ├── home.py             # Home page
│   ├── medical_qa.py       # Medical Q&A
│   ├── image_analysis.py   # Image analysis
│   └── ocr_report.py       # OCR reports
│
├── rag/
│   ├── embeddings.py       # Embeddings
│   ├── retrieval.py        # FAISS retrieval
│   └── pipeline.py         # RAG pipeline
│
├── utils/
│   ├── helpers.py
│   └── preprocessing.py
│
└── OCR/
    ├── extractor.py        # OCR extraction
    └── processor.py        # Medical text processing
```

---

## 🛠️ Technologies

* **Python**
* **TensorFlow / Keras**
* **Transformers**
* **Sentence Transformers**
* **FAISS**
* **OCR**
* **PyMuPDF**
* **Pandas / NumPy**
* **Streamlit**

---

## 🔄 Workflow

```text
Input
 ↓
OCR / Text Extraction
 ↓
Text Preprocessing
 ↓
Medical Text Analysis
 ↓
Fine-Tuned Model + RAG
 ↓
AI Explanation
 ↓
Summary + Key Findings + Terms
 ↓
Arabic / English
 ↓
Streamlit
```

---

## 🚀 Run the Project

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 👨‍💻 MediSimplify

**AI-Powered Medical Document Simplification & Explanation**

Built with ❤️ using **AI, NLP, OCR, RAG, and Streamlit**.
