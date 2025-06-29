# File: blogs/index_blogs.py
"""Chunk and embed blog content using Gemini embeddings, then store in ChromaDB."""

import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "blogs/chroma_index"
BLOG_FOLDER = "blogs/data"

# Load Gemini embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def load_blog_docs(folder: str) -> list[Document]:
    """Read .txt blog files and return LangChain Document objects."""
    docs = []
    for file in Path(folder).glob("*.txt"):
        content = file.read_text(encoding="utf-8")
        docs.append(Document(page_content=content, metadata={"source": str(file)}))
    return docs


def build_blog_vectorstore():
    print("📥 Loading blog posts...")
    docs = load_blog_docs(BLOG_FOLDER)

    print("🔪 Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = splitter.split_documents(docs)

    print("🔎 Embedding and saving to Chroma...")
    Chroma.from_documents(split_docs, embedding=embedding_model, persist_directory=CHROMA_DIR)
    print("✅ Blog vectorstore built and persisted to:", CHROMA_DIR)


if __name__ == "__main__":
    build_blog_vectorstore()
