
# 📚 CampusLens AI

### A Source-Grounded Academic Document Assistant

CampusLens AI is a Python-based project designed to help students find relevant information in academic documents and trace answers back to their source pages.

The project currently includes PDF text extraction, text chunking, TF-IDF-based retrieval, a basic answer-generation pipeline, a FastAPI endpoint, and an initial Streamlit interface.

## 🎯 Problem Statement

Students often need to search lengthy academic documents to find information relevant to a specific question. CampusLens AI aims to make that process easier by retrieving relevant passages and identifying their page numbers.

## ✨ Current Features

- **PDF Text Extraction:** Extracts text from PDF pages using PyMuPDF.
- **Text Chunking:** Splits extracted text into smaller, overlapping chunks.
- **Relevant Passage Retrieval:** Uses TF-IDF and cosine similarity to rank passages against a query.
- **Source References:** Includes page numbers with retrieved passages.
- **Answer Generation:** Builds a response from relevant document passages.
- **FastAPI Backend:** Provides an initial API health-check endpoint.
- **Streamlit Interface:** Provides an initial web interface.
- **SQLite Foundation:** Includes initial database setup for document records.

## 🛠️ Technology Stack

- Python
- PyMuPDF
- Scikit-learn
- FastAPI
- Streamlit
- SQLite
- Git and GitHub

## 📂 Project Structure

```text
CampusLensAI/
├── app/
│   ├── answerer.py
│   ├── api.py
│   ├── chunker.py
│   ├── database.py
│   ├── document_parser.py
│   ├── retrieval.py
│   └── ui.py
├── tests/
├── sample_documents/    # Local sample documents; not published
├── .gitignore
├── DEVELOPMENT_LOG.md
└── test_parser.py
```

## 🚧 Development Status

CampusLens AI is under active development.

The current implementation provides the initial document-processing and retrieval pipeline. PDF upload through the interface, complete end-to-end integration, and further testing and evaluation remain planned improvements.

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/CampusLensAI.git
cd CampusLensAI
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install fastapi uvicorn streamlit pymupdf scikit-learn pytest python-multipart
```

### 4. Run the Streamlit interface

```bash
python -m streamlit run app/ui.py
```

### 5. Run the FastAPI backend

In a separate terminal, with the virtual environment activated:

```bash
python -m uvicorn app.api:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API documentation.

### 6. Test the document-processing pipeline

Add your own permitted test PDF to the local `sample_documents/` folder, then run:

```bash
python test_parser.py
```

The test script currently expects a PDF named `AJAX_MidSem_Answers.pdf` in that folder. Use only documents you have permission to process.

## 🗺️ Roadmap

- [ ] Connect PDF upload to the Streamlit interface
- [ ] Integrate uploading, processing, and retrieval into one workflow
- [ ] Improve document management and persistence
- [ ] Strengthen answer grounding and source references
- [ ] Expand automated tests and retrieval evaluation
- [ ] Add interface screenshots and a project demonstration

## 📈 Development Log

Development milestones and actual time invested are tracked in [`DEVELOPMENT_LOG.md`](DEVELOPMENT_LOG.md).

## 👨‍💻 Author

Developed as an independent project to explore document processing, information retrieval, and Python application development.

---

*CampusLens AI — Making academic document search more accessible.*
