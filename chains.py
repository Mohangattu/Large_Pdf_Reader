import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# -----------------------------
# Embedding Model
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Load ChromaDB
# -----------------------------
vectorstore = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings
)

# -----------------------------
# Retriever
# -----------------------------
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# -----------------------------
# LLM
# -----------------------------
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# -----------------------------
# Prompt Templates
# -----------------------------
qa_template = """
You are a helpful PDF assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context, say:

"I could not find the answer in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_template
)

summary_template = """
You are a PDF summarization expert.

Based on the provided content, generate a concise and comprehensive summary.

Context:
{context}

Summary:
"""

summary_prompt = PromptTemplate(
    input_variables=["context"],
    template=summary_template
)

keypoints_template = """
You are a PDF analysis expert.

Based on the provided content, extract and list the key points in a structured format.

Context:
{context}

Key Points:
"""

keypoints_prompt = PromptTemplate(
    input_variables=["context"],
    template=keypoints_template
)

# -----------------------------
# Helper Function: Extract Page Numbers
# -----------------------------
def _extract_page_numbers(docs):
    """Extract unique page numbers from retrieved documents."""
    page_numbers = []
    for doc in docs:
        metadata = getattr(doc, "metadata", {}) or {}
        if metadata.get("page_label") is not None:
            page_numbers.append(str(metadata["page_label"]))
        elif metadata.get("page") is not None:
            try:
                page_numbers.append(str(int(metadata["page"]) + 1))
            except (ValueError, TypeError):
                page_numbers.append(str(metadata["page"]))

    unique_pages = []
    for page in page_numbers:
        if page not in unique_pages:
            unique_pages.append(page)

    return unique_pages

# -----------------------------
# Main Functions
# -----------------------------
def ask_pdf(question: str):
    """
    Answer a question about the PDF using RAG.

    Args:
        question (str): The question to ask about the PDF

    Returns:
        str: The answer with source page information
    """
    # Retrieve relevant chunks
    docs = retriever.invoke(question)

    # Combine retrieved chunks
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Extract page numbers
    unique_pages = _extract_page_numbers(docs)
    source_page_text = f"Page {unique_pages[0]}" if unique_pages else "Page unknown"

    # Format prompt
    final_prompt = qa_prompt.format(
        context=context,
        question=question
    )

    # Generate response
    response = llm.invoke(final_prompt)
    answer_text = response.content.strip()

    return f"Answer: {answer_text}\n\nSource: {source_page_text}"


def generate_summary():
    """
    Generate a comprehensive summary of the entire PDF.

    Returns:
        str: A summary of the PDF content
    """
    # Retrieve a broader set of documents for context
    docs = retriever.invoke("overall summary content main topics")

    # Combine retrieved chunks
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Format prompt
    final_prompt = summary_prompt.format(
        context=context
    )

    # Generate response
    response = llm.invoke(final_prompt)
    summary_text = response.content.strip()

    return f"Summary:\n\n{summary_text}"


def extract_keypoints():
    """
    Extract key points and main insights from the PDF.

    Returns:
        str: Key points extracted from the PDF
    """
    # Retrieve relevant chunks
    docs = retriever.invoke("main concepts important points key findings highlights")

    # Combine retrieved chunks
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Format prompt
    final_prompt = keypoints_prompt.format(
        context=context
    )

    # Generate response
    response = llm.invoke(final_prompt)
    keypoints_text = response.content.strip()

    return f"Key Points:\n\n{keypoints_text}"