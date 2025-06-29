# File: app/deps.py
"""Dependency loading: Neo4j driver, Gemini LLM, Chroma vector store."""

from neo4j import GraphDatabase
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings

# Neo4j driver
neo4j_driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

# Gemini LLM and embedding
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_output_tokens=2048,
)

embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Chroma vector DB
vector_store = Chroma(
    persist_directory=settings.CHROMA_DIR,
    embedding_function=embedding_model
)