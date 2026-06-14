import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PDF_PATH = r"D:\deep learning\langchain\long_pdf_reader\data\AI-ML - Course Brochure- 2026.pdf"
CHROMA_PATH = r"D:\deep learning\langchain\long_pdf_reader\data\chroma_db"


def load_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks


def create_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


def create_vector_store(chunks, embeddings):

    if os.path.exists(CHROMA_PATH):
        print("Existing ChromaDB found.")
        print("Delete the folder manually if you want a fresh database.")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print("ChromaDB created successfully!")

    return vectorstore


def main():

    print("Loading PDF...")

    documents = load_pdf(PDF_PATH)

    print("Splitting document...")

    chunks = split_documents(documents)

    print("Loading embedding model...")

    embeddings = create_embeddings()

    print("Creating ChromaDB...")

    create_vector_store(
        chunks,
        embeddings
    )

    print("Ingestion completed successfully!")


if __name__ == "__main__":
    main()