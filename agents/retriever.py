# File: agents/retriever.py
"""Hybrid Retriever: Graph + Chroma vector search for relevant marketing insights."""

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "blogs/chroma_index"
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def search_graph_concepts(question: str, limit: int = 5) -> list[str]:
    """Run Cypher to fetch blog-related tags from KG linked to past campaigns."""
    cypher = (
        """
        MATCH (c:Campaign)-[:HAS_CREATIVE]->(cr)-[:MENTIONED_IN]->(b:BlogChunk)
        WHERE b.chunk_id IS NOT NULL
        RETURN DISTINCT b.chunk_id LIMIT $limit
        """
    )
    with driver.session() as session:
        result = session.run(cypher, {"limit": limit})
        return [r["b.chunk_id"] for r in result if r.get("b.chunk_id")]


def semantic_retrieve(question: str, k: int = 3) -> list[Document]:
    """Retrieve top-k blog passages from Chroma based on semantic similarity."""
    return vector_store.similarity_search(question, k=k)


def hybrid_retrieve(question: str, use_graph: bool = True) -> list[str]:
    """Combine graph-based concept filtering with semantic blog retrieval."""
    if use_graph:
        concept_ids = search_graph_concepts(question)
        if concept_ids:
            print("🔎 Graph-guided concept match:", concept_ids)
    return [doc.page_content for doc in semantic_retrieve(question)]