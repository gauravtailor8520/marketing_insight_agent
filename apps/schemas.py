# File: app/schemas.py
"""Pydantic schemas for request and response models."""

from pydantic import BaseModel
from typing import Optional

class InsightRequest(BaseModel):
    question: str
    csv_data: str  # CSV content passed as string

class InsightResponse(BaseModel):
    answer: str
    evidence: Optional[str] = None
