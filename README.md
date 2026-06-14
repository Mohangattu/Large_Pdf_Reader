# Large PDF Reader

A simple Streamlit app for asking questions to a PDF using embeddings, ChromaDB, and Groq LLM.

## Files

- `app.py` — Streamlit user interface
- `chains.py` — retriever, prompt template, and LLM answer flow
- `ingest.py` — loads PDF, splits text, and creates the Chroma vector store
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

## Usage

- Enter a question in the Streamlit app.
- The app loads relevant chunks from ChromaDB and asks the LLM.
- If the answer is not in the PDF, the prompt instructs the model to say it could not find the answer.

## Notes

- The main runtime files are `app.py`, `chains.py`, and `ingest.py`.
- `prompt.py` and `config.py` are not used in the current workflow.
- If you want to refresh the database, delete `data/chroma_db` and rerun `python ingest.py`.
