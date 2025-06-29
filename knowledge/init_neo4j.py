# File: knowledge/init_neo4j.py
"""Bootstrap the Neo4j knowledge graph schema and indexes."""

from neo4j import GraphDatabase
from apps.config import settings


def init_neo4j_schema():
    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
    with driver.session() as session:
        session.run("""
        CREATE CONSTRAINT campaign_id IF NOT EXISTS ON (c:Campaign) ASSERT c.id IS UNIQUE;
        CREATE INDEX IF NOT EXISTS FOR (m:Metric) ON (m.date);
        CREATE INDEX IF NOT EXISTS FOR (b:BlogChunk) ON (b.chunk_id);
        """)
    print("✅ Neo4j schema initialized.")


if __name__ == "__main__":
    init_neo4j_schema()
