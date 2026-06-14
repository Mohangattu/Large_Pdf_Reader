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
# Prompt Template
# -----------------------------
template = """
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

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# -----------------------------
# Main Function
# -----------------------------
def answer_question(question: str):

    # Retrieve relevant chunks
    docs = retriever.invoke(question)

    # Combine retrieved chunks
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Format prompt
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # Generate response
    response = llm.invoke(final_prompt)

    return response.content