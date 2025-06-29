# File: agents/kg_ingest.py
"""Push cleaned marketing data into Neo4j KG."""

from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def ingest_to_neo4j(df: pd.DataFrame):
    """Insert campaigns and metrics into Neo4j."""
    with driver.session() as session:
        for _, row in df.iterrows():
            session.write_transaction(_create_campaign_metric_nodes, row)

def _create_campaign_metric_nodes(tx, row):
    tx.run(
        """
        MERGE (c:Campaign {id: $id})
          ON CREATE SET c.company = $company,
                        c.type = $type,
                        c.target = $target,
                        c.channel = $channel,
                        c.location = $location,
                        c.language = $language,
                        c.segment = $segment
        MERGE (m:Metric {date: $date, ctr: $ctr})
          ON CREATE SET m.cost = $cost,
                        m.roi = $roi,
                        m.clicks = $clicks,
                        m.impressions = $impressions,
                        m.engagement = $engagement
        MERGE (m)-[:BELONGS_TO]->(c)
        """,
        {
            "id": str(row.get("campaign_id")),
            "company": row.get("company"),
            "type": row.get("campaign_type"),
            "target": row.get("target_audience"),
            "channel": row.get("channel_used"),
            "location": row.get("location"),
            "language": row.get("language"),
            "segment": row.get("customer_segment"),
            "date": row.get("date").strftime("%Y-%m-%d") if pd.notnull(row.get("date")) else None,
            "ctr": row.get("ctr"),
            "cost": row.get("acquisition_cost"),
            "roi": row.get("roi"),
            "clicks": row.get("clicks"),
            "impressions": row.get("impressions"),
            "engagement": row.get("engagement_score"),
        },
    )
