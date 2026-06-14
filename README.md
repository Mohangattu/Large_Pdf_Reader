# Large PDF Reader

A powerful Streamlit app for analyzing large PDFs using embeddings, ChromaDB, and Groq LLM. Ask questions, generate summaries, and extract key points from your PDF documents.

## Features

- **Ask Questions** — Ask any question about your PDF and get answers with source page references
- **Generate Summary** — Create a comprehensive summary of the entire PDF
- **Extract Key Points** — Identify and extract key points and main insights from the document
- **RAG-Based Retrieval** — Uses Retrieval-Augmented Generation for accurate, context-aware responses
- **Source Tracking** — All answers include source page information

## Files

- `app.py` — Streamlit user interface with tabbed navigation
- `chains.py` — Core chains with three main functions: `ask_pdf()`, `generate_summary()`, `extract_keypoints()`
- `ingest.py` — Loads PDF, splits text, and creates the Chroma vector store
- `prompt.py` — currently unused
- `config.py` — currently unused

## Requirements

- Python 3.8+
- `GROQ_API_KEY` environment variable
- A PDF file to ingest

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

4. Update `PDF_PATH` in `ingest.py` to point to your PDF file if needed.

5. Run ingestion once to build the vector store:

```bash
python ingest.py
```

6. Start the Streamlit app:

```bash
streamlit run app.py
```

## Main Functions (chains.py)

You can also use the PDF reader programmatically:

```python
from chains import ask_pdf, generate_summary, extract_keypoints

# Ask a question about the PDF
answer = ask_pdf("What is this document about?")
print(answer)

# Generate a summary
summary = generate_summary()
print(summary)

# Extract key points
keypoints = extract_keypoints()
print(keypoints)
```

## Usage

The Streamlit app features three main tabs:

### 1. Ask Questions
- Enter your question about the PDF
- The app retrieves relevant chunks from ChromaDB
- Groq LLM generates an answer with source page reference
- If the answer is not found, the model will indicate it could not find the answer in the PDF

### 2. Summary
- Click "Generate Summary" to create a comprehensive summary of the entire PDF
- The app uses multiple retrieved chunks to generate an accurate overview

### 3. Key Points
- Click "Extract Key Points" to identify main concepts and insights
- Results are organized in a structured format for easy reference

## Notes

- The main runtime files are `app.py`, `chains.py`, and `ingest.py`.
- `prompt.py` and `config.py` are not used in the current workflow.
- If you want to refresh the database, delete `data/chroma_db` and rerun `python ingest.py`.
