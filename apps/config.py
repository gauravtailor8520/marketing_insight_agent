# File: app/config.py
"""Centralized config management."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI")
    NEO4J_USER: str = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")
    GEMINI_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    CHROMA_DIR: str = "blogs/chroma_index"

settings = Settings()